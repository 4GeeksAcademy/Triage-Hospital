"""Cola de triaje con menú de terminal.

DISEÑO
------
Se utiliza un heap con entradas:
(triage_level, arrived_at, insertion_order, patient).

El nivel 1 tiene prioridad sobre el 2 y el 3. Dentro del mismo
nivel se respeta arrived_at. Si coinciden los timestamps, se
respeta el orden de inserción.

heapq permite insertar y extraer en O(log n), y consultar el
siguiente en O(1). Una deque única no ordena por prioridad.
Una lista ordenada requiere inserciones O(n). Tres deques serían
una buena alternativa si las llegadas se insertaran siempre en
orden cronológico; el heap también admite fechas fuera de orden.

CONCURRENCIA (diseño, no implementada)
------------------------------------
Para varios hilos, proteger las consultas y modificaciones con
un mismo threading.Lock. Al atender: adquirir el bloqueo,
seleccionar y retirar al paciente de forma atómica y, si existe
un registro de pacientes en atención, actualizarlo dentro del
mismo bloqueo. Después liberar el bloqueo y realizar la atención.

No utilizar peek() seguido de dequeue() como operaciones
independientes para reservar un paciente.

Si un paciente crítico se inserta antes de la extracción atómica,
tendrá prioridad. Si llega después, será el siguiente: no
interrumpe a un paciente ya retirado para su atención.

Para varios procesos o servidores, un Lock de hilos no basta:
haría falta una cola compartida con operaciones atómicas o una
transacción en base de datos.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import heapq
from itertools import count


class EmptyQueueError(IndexError):
    """Se intentó consultar o extraer de una cola vacía."""


@dataclass(frozen=True)
class Patient:
    name: str
    triage_level: int
    arrived_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def __post_init__(self):
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("El nombre no puede estar vacío.")

        if (
            type(self.triage_level) is not int
            or self.triage_level not in (1, 2, 3)
        ):
            raise ValueError("El nivel debe ser un entero entre 1 y 3.")

        if not isinstance(self.arrived_at, datetime):
            raise ValueError("La llegada debe ser un datetime.")

        if (
            self.arrived_at.tzinfo is None
            or self.arrived_at.utcoffset() is None
        ):
            raise ValueError("La llegada debe incluir zona horaria.")

        object.__setattr__(self, "name", self.name.strip())
        object.__setattr__(
            self,
            "arrived_at",
            self.arrived_at.astimezone(timezone.utc),
        )


class TriageQueue:
    def __init__(self):
        self._heap = []
        self._sequence = count()

    def enqueue(self, patient: Patient) -> None:
        if not isinstance(patient, Patient):
            raise TypeError("Debes proporcionar un Patient.")

        heapq.heappush(
            self._heap,
            (
                patient.triage_level,
                patient.arrived_at,
                next(self._sequence),
                patient,
            ),
        )

    def dequeue(self) -> Patient:
        if not self._heap:
            raise EmptyQueueError("No hay pacientes en espera.")
        return heapq.heappop(self._heap)[3]

    def peek(self) -> Patient:
        if not self._heap:
            raise EmptyQueueError("No hay pacientes en espera.")
        return self._heap[0][3]

    def list_queue(self) -> list[Patient]:
        # sorted devuelve una copia; no modifica el heap.
        return [entry[3] for entry in sorted(self._heap)]

    def stats(self) -> dict[int, int]:
        result = {1: 0, 2: 0, 3: 0}
        for entry in self._heap:
            result[entry[3].triage_level] += 1
        return result


def show_patient(patient: Patient) -> str:
    arrival = patient.arrived_at.strftime("%Y-%m-%d %H:%M:%S UTC")
    return (
        f"{patient.name} | Nivel {patient.triage_level}"
        f" | Llegada: {arrival}"
    )


def main() -> None:
    queue = TriageQueue()

    menu = """
--- Cola de triaje ---
1. Añadir paciente
2. Llamar al siguiente paciente
3. Ver cola
4. Ver estadísticas
5. Consultar siguiente sin retirarlo
0. Salir
"""

    while True:
        try:
            print(menu)
            option = input("Elige una opción: ").strip()

            if option == "1":
                name = input("Nombre: ")
                level = int(input("Nivel (1 crítico, 2 medio, 3 bajo): "))
                patient = Patient(name, level)
                queue.enqueue(patient)
                print(f"Añadido: {show_patient(patient)}")

            elif option == "2":
                print(f"Llamando a: {show_patient(queue.dequeue())}")

            elif option == "3":
                patients = queue.list_queue()
                if not patients:
                    print("No hay pacientes en espera.")
                for position, patient in enumerate(patients, start=1):
                    print(f"{position}. {show_patient(patient)}")

            elif option == "4":
                stats = queue.stats()
                for level, total in stats.items():
                    print(f"Nivel {level}: {total}")
                print(f"Total: {sum(stats.values())}")

            elif option == "5":
                print(f"Siguiente: {show_patient(queue.peek())}")

            elif option == "0":
                print("Programa finalizado.")
                break

            else:
                print("Opción no válida.")

        except EmptyQueueError as error:
            print(error)
        except ValueError as error:
            print(f"Entrada no válida: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nPrograma finalizado.")
            break


if __name__ == "__main__":
    main()
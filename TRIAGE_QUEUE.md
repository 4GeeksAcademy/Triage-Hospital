# Sistema de Cola de Triaje Hospitalario

## Descripción

**Sistema de gestión de cola de triaje para hospitales** implementado en Python usando una estructura de datos heap (montículo) para garantizar una atención eficiente de pacientes según su nivel de criticidad.

Este proyecto implementa un **algoritmo de cola de prioridad** que ordena automáticamente a los pacientes según:
1. **Nivel de triaje** (crítico, medio, bajo) → máxima prioridad
2. **Tiempo de llegada** → desempate por FIFO dentro del mismo nivel
3. **Orden de inserción** → desempate adicional si las llegadas coinciden exactamente

## Características

- ✅ **Estructura de datos optimizada**: Heap binario para inserción/extracción O(log n)
- ✅ **Validación de datos**: Dataclasses inmutables con validación en tiempo de construcción
- ✅ **Interfaz interactiva**: Menú de terminal fácil de usar
- ✅ **Sin dependencias externas**: Usa solo la stdlib de Python 3.7+
- ✅ **Documentación de concurrencia**: Notas de diseño para implementación multi-thread

## Requisitos

- Python 3.7 o superior
- Sin dependencias externas

## Instalación y Uso

### Ejecución

```bash
python main.py
```

### Menú Interactivo

```
--- Cola de triaje ---
1. Añadir paciente
2. Llamar al siguiente paciente
3. Ver cola
4. Ver estadísticas
5. Consultar siguiente sin retirarlo
0. Salir
```

**Opciones:**

| Opción | Función | Ejemplo |
|--------|---------|---------|
| **1** | Añadir un nuevo paciente | Nombre: "Juan García", Nivel: 2 |
| **2** | Atender al siguiente paciente (lo retira de la cola) | Muestra quién se atiende |
| **3** | Ver todos los pacientes en espera ordenados | Lista completa de la cola |
| **4** | Estadísticas de pacientes por nivel | Totales por criticidad |
| **5** | Consultar quién es el siguiente sin retirarlo | Peek sin modificar la cola |
| **0** | Salir del programa | Cierra la aplicación |

### Ejemplo de Sesión

```
--- Cola de triaje ---
1. Añadir paciente
...
Elige una opción: 1
Nombre: María López
Nivel (1 crítico, 2 medio, 3 bajo): 1
Añadido: María López | Nivel 1 | Llegada: 2026-11-16 23:09:45 UTC

Elige una opción: 1
Nombre: Carlos Ruiz
Nivel (1 crítico, 2 medio, 3 bajo): 2
Añadido: Carlos Ruiz | Nivel 2 | Llegada: 2026-11-16 23:10:12 UTC

Elige una opción: 2
Llamando a: María López | Nivel 1 | Llegada: 2026-11-16 23:09:45 UTC
```

## Arquitectura

### Estructura de Datos: Heap

La cola utiliza un **min-heap** (montículo mínimo) con tuplas de 4 elementos:

```python
(triage_level, arrived_at, insertion_order, patient)
```

**Ventajas:**
- Inserción: O(log n)
- Extracción: O(log n)
- Consulta del siguiente: O(1)
- Respeta prioridad, FIFO y orden de inserción simultáneamente

**Alternativas consideradas:**
- 3 Deques (una por nivel): Más rápido pero requiere timestamps ordenados
- Lista ordenada: Más simple pero inserción O(n)
- Heap es el mejor balance entre eficiencia y flexibilidad

### Clase `Patient`

```python
@dataclass(frozen=True)
class Patient:
    name: str
    triage_level: int
    arrived_at: datetime
```

**Propiedades:**
- **Inmutable** (frozen=True): Garantiza integridad de datos
- **Validación automática**: Verificación en `__post_init__`
- **Timestamps con zona horaria**: Siempre en UTC para consistencia

### Clase `TriageQueue`

**Métodos principales:**

- `enqueue(patient)`: Añade un paciente O(log n)
- `dequeue()`: Retira y retorna el siguiente O(log n)
- `peek()`: Consulta el siguiente sin remover O(1)
- `list_queue()`: Retorna la cola ordenada O(n log n)
- `stats()`: Estadísticas por nivel O(n)

**Excepciones:**
- `EmptyQueueError`: Cuando se intenta operar en una cola vacía
- `TypeError`: Si no se proporciona un Patient
- `ValueError`: Validación de entrada inválida

## Notas de Diseño: Concurrencia

### Para Multi-Threading

```python
lock = threading.Lock()

with lock:
    patient = queue.dequeue()  # Atómico
    update_treatment_record(patient)
```

**Reglas:**
1. Proteger consultas y modificaciones con un mismo `threading.Lock`
2. **Nunca** hacer `peek()` seguido de `dequeue()` sin el lock
3. Si un paciente crítico llega antes de la extracción, tendrá prioridad
4. No interrumpe a pacientes ya retirados

### Para Múltiples Procesos/Servidores

Se necesitaría:
- Base de datos con transacciones atómicas
- Sistema de colas distribuidas (RabbitMQ, Redis, etc.)
- API REST con operaciones atómicas

## Validaciones Implementadas

✅ **Patient:**
- Nombre no vacío y normalizado (strip)
- Nivel entre 1-3 (entero exacto)
- Timestamp con zona horaria (UTC)

✅ **TriageQueue:**
- Solo acepta objetos Patient
- Lanza EmptyQueueError si la cola está vacía

✅ **Input de usuario:**
- Manejo de EOFError y KeyboardInterrupt
- Validación de entrada numérica
- Mensajes de error descriptivos

## Complejidad Algorítmica

| Operación | Complejidad | Notas |
|-----------|-------------|-------|
| Enqueue | O(log n) | Inserción en heap |
| Dequeue | O(log n) | Extracción de raíz + heapify |
| Peek | O(1) | Acceso directo a raíz |
| List | O(n log n) | Sorted del heap |
| Stats | O(n) | Iteración simple |

## Código Limpio

✅ **Principios aplicados:**
- **DRY**: No repetición de lógica
- **SOLID**: Single Responsibility, encapsulación
- **Type Hints**: Tipado explícito (Python 3.7+)
- **Docstrings**: Documentación clara
- **Excepciones personalizadas**: EmptyQueueError
- **Inmutabilidad**: Patient es frozen dataclass

## Posibles Mejoras Futuras

1. **Persistencia**: SQLite o PostgreSQL para pacientes
2. **API REST**: FastAPI o Flask para integración hospitalaria
3. **UI Web**: Flask/React para interfaz gráfica
4. **Notificaciones**: Email/SMS cuando se llama a un paciente
5. **Métricas**: Tiempo medio de espera, throughput
6. **Re-priorización**: Permitir cambiar nivel mientras está en espera
7. **Multi-ubicación**: Varias colas por servicio (Urgencias, Cirugía, etc.)

## Autores

Proyecto educativo de **4Geeks Academy**

## Licencia

Consultar [LICENSE.md](LICENSE.md)

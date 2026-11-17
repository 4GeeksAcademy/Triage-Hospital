# Triage Hospital - Patient Queue Management System

> A terminal-based hospital triage queue management system built in Python

## Overview

**Triage Hospital** is a command-line application that implements a priority-based patient queue system for hospital triage. It efficiently manages patients arriving at a hospital using a heap-based data structure, ensuring critical patients are always seen first.

### Purpose

This system prioritizes patients based on medical urgency levels:
- **Level 1 (Critical)**: Life-threatening conditions requiring immediate attention
- **Level 2 (Medium)**: Serious conditions requiring prompt care
- **Level 3 (Low)**: Non-urgent conditions

Patients are served based on triage level first, then by arrival time within the same level.

### Key Features

- **Efficient Priority Queue**: Uses a min-heap for O(log n) insertions and removals
- **Thread-Safe Design**: Designed with concurrency support (ready for multi-threaded environments)
- **Validation**: Strict validation of patient data and input
- **Real-time Statistics**: Track patients by triage level
- **Queue Inspection**: View all patients in queue without removing them

## How to Run

Start the application from the command line:

```bash
python main.py
```

This launches an interactive terminal menu with the following options:

1. **Add Patient**: Enter patient name and triage level (1-3)
2. **Call Next Patient**: Dequeue and display the highest priority patient
3. **View Queue**: Display all patients currently in queue, sorted by priority
4. **View Statistics**: Show patient counts by triage level
5. **Peek Next**: View the next patient without removing them from queue
6. **Exit**: Close the application

## Technical Details

### Data Structure
- **Heap-based queue**: `(triage_level, arrived_at, insertion_order, patient)` tuples
- **Thread-safe by design**: Ready for `threading.Lock` protection
- **Efficient operations**: Insert and remove in O(log n), peek in O(1)

### Patient Class
Immutable dataclass with validation for:
- Non-empty patient names
- Valid triage levels (1, 2, or 3)
- Timezone-aware arrival timestamps (UTC)

### Error Handling
- `EmptyQueueError`: Raised when trying to access an empty queue
- `ValueError`: Raised for invalid patient data
- `TypeError`: Raised for incorrect argument types

# Mini Database Engine

A lightweight, file-based database engine in pure Python that mimics basic SQL operations.

## Features

- **CREATE TABLE** - Create new tables with column definitions
- **INSERT INTO** - Add records to tables
- **SELECT** - Query data with column selection and WHERE filtering
- **DELETE FROM** - Remove records with WHERE conditions
- **UPDATE** - Modify existing records
- File-based storage (each table is a .db file in /data directory)
- Interactive REPL interface
- No external dependencies

## Quick Start

### 1. Load Sample Data (Optional)

```bash
python load_sample_data.py
```

This creates sample tables (employees, products, customers) with data.

### 2. Launch the GUI (Recommended)

**Windows:**
```bash
run_gui.bat
```

**All platforms:**
```bash
python gui.py
```

### 3. Or Use Command Line Mode

```bash
python main.py
```

## GUI Features - Professional Edition

### Three-Panel Layout
- **LEFT**: Database browser with search, table list, and 9 quick action buttons
- **CENTER**: SQL editor with templates + large data grid for viewing results
- **RIGHT**: Interactive console with command history (↑/↓ arrows)

### Key Features
- ✅ **Accessible colors** - High contrast, easy to read
- ✅ **Double-click to edit** - Click any row in data view to edit
- ✅ **Form-based entry** - Easy wizards for insert/edit operations
- ✅ **Interactive console** - Type SQL directly with command history
- ✅ **Quick actions** - 9 buttons for common tasks
- ✅ **Search wizard** - Find specific records easily
- ✅ **Right-click menu** - Copy, edit, delete rows
- ✅ **F5 to execute** - Keyboard shortcut for running queries
- ✅ **Auto-fill templates** - Select table, click template, it auto-fills table name

## Example Commands

```sql
-- Create a table
CREATE TABLE students (id, name, age);

-- Insert records
INSERT INTO students VALUES (1, 'Alice', 20);
INSERT INTO students VALUES (2, 'Bob', 22);
INSERT INTO students VALUES (3, 'Charlie', 19);

-- Select all columns
SELECT * FROM students;

-- Select specific columns
SELECT name, age FROM students;

-- Select with WHERE clause
SELECT * FROM students WHERE age = 20;

-- Update records
UPDATE students SET age = 21 WHERE name = Alice;

-- Delete records
DELETE FROM students WHERE id = 2;

-- Exit
EXIT
```

## Project Structure

- **main.py** - Entry point with interactive REPL
- **parser.py** - SQL command parser and tokenizer
- **storage.py** - File I/O operations for table persistence
- **engine.py** - Query execution engine
- **data/** - Directory containing .db table files (auto-created)

## Data Storage Format

Each table is stored as a CSV-like file:
- First line: column headers (comma-separated)
- Subsequent lines: data rows (comma-separated)

Example `students.db`:
```
id,name,age
1,Alice,20
2,Bob,22
```

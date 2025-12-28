# GUI User Guide

## Starting the GUI

**Windows:**
- Double-click `run_gui.bat`
- Or run: `python gui.py`

**Other platforms:**
```bash
python gui.py
```

## GUI Layout

The interface is divided into 4 main sections:

### 1. Tables Panel (Left Side)
- Lists all available database tables
- Click on any table to view its data
- Use "Refresh Tables" button to update the list

### 2. SQL Command Panel (Top Right)
- Enter your SQL commands here
- Multi-line support for complex queries
- **Execute** button runs the command
- **Clear** button clears the input

### 3. Quick Command Buttons
- **CREATE TABLE** - Inserts a CREATE TABLE template
- **INSERT** - Inserts an INSERT template (auto-fills if table selected)
- **SELECT *** - Inserts a SELECT template for the selected table

### 4. Output Panel (Middle Right)
- Shows execution status and messages
- Displays success/error messages
- Shows row counts for operations

### 5. Query Results Panel (Bottom Right)
- Displays SELECT query results in a table format
- Scrollable for large datasets
- Columns are automatically sized

## Example Workflow

### Creating a New Table

1. Click the **CREATE TABLE** quick button
2. Modify the template:
   ```sql
   CREATE TABLE employees (id, name, department, salary)
   ```
3. Click **Execute**
4. The table appears in the Tables list

### Inserting Data

1. Select your table from the Tables list
2. Click the **INSERT** quick button
3. Fill in the values:
   ```sql
   INSERT INTO employees VALUES (1, 'John Doe', 'Engineering', 75000)
   ```
4. Click **Execute**
5. Repeat for more records

### Viewing Data

1. Click on a table name in the Tables list
   - OR -
2. Click **SELECT *** quick button and execute
3. Results appear in the Query Results table

### Filtering Data

Enter a WHERE clause:
```sql
SELECT * FROM employees WHERE department = Engineering
```

### Updating Records

```sql
UPDATE employees SET salary = 80000 WHERE id = 1
```

### Deleting Records

```sql
DELETE FROM employees WHERE id = 1
```

## Tips

- The GUI automatically refreshes the tables list after CREATE/DROP operations
- Click on any table to quickly view its contents
- Use the quick buttons to avoid typing common commands
- The output panel shows helpful messages about row counts
- All data is saved to .db files in the /data directory

## Keyboard Shortcuts

- **Ctrl+A** in SQL input - Select all text
- **Ctrl+C** - Copy
- **Ctrl+V** - Paste
- **Ctrl+X** - Cut

## Troubleshooting

**GUI doesn't start:**
- Make sure tkinter is installed (comes with Python by default)
- Check Python version (3.6+ recommended)

**Table doesn't appear:**
- Click "Refresh Tables" button
- Check the /data directory for .db files

**Error messages:**
- Read the Output panel for detailed error information
- Check SQL syntax
- Verify table and column names exist

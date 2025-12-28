
from parser import SQLParser
from storage import Storage


class DatabaseEngine:
    
    def __init__(self):
        self.storage = Storage()
        self.parser = SQLParser()
    
    def execute(self, command):
        """Execute a SQL command"""
        parsed = self.parser.parse(command)
        
        if parsed['type'] == 'CREATE':
            return self._execute_create(parsed)
        elif parsed['type'] == 'DROP':
            return self._execute_drop(parsed)
        elif parsed['type'] == 'SHOW_TABLES':
            return self._execute_show_tables()
        elif parsed['type'] == 'DESCRIBE':
            return self._execute_describe(parsed)
        elif parsed['type'] == 'INSERT':
            return self._execute_insert(parsed)
        elif parsed['type'] == 'SELECT':
            return self._execute_select(parsed)
        elif parsed['type'] == 'DELETE':
            return self._execute_delete(parsed)
        elif parsed['type'] == 'UPDATE':
            return self._execute_update(parsed)
        elif parsed['type'] == 'TRUNCATE':
            return self._execute_truncate(parsed)
    
    def _execute_create(self, parsed):
        """Execute CREATE TABLE"""
        self.storage.create_table(parsed['table'], parsed['columns'])
        return f"Table '{parsed['table']}' created successfully."
    
    def _execute_drop(self, parsed):
        """Execute DROP TABLE"""
        import os
        if not self.storage.table_exists(parsed['table']):
            raise ValueError(f"Table '{parsed['table']}' does not exist")
        
        path = self.storage._get_table_path(parsed['table'])
        os.remove(path)
        return f"Table '{parsed['table']}' dropped successfully."
    
    def _execute_show_tables(self):
        """Execute SHOW TABLES"""
        import os
        tables = []
        if os.path.exists(self.storage.data_dir):
            for file in sorted(os.listdir(self.storage.data_dir)):
                if file.endswith('.db'):
                    tables.append(file[:-3])
        
        if not tables:
            return "No tables found."
        
        # Format as table
        lines = ["Tables in database:", "-" * 30]
        for table in tables:
            lines.append(f"  • {table}")
        lines.append(f"\nTotal: {len(tables)} table(s)")
        return '\n'.join(lines)
    
    def _execute_describe(self, parsed):
        """Execute DESCRIBE"""
        columns, rows = self.storage.read_table(parsed['table'])
        
        lines = [f"Table: {parsed['table']}", "=" * 40]
        lines.append(f"Columns: {len(columns)}")
        lines.append(f"Rows: {len(rows)}")
        lines.append("\nColumn Names:")
        lines.append("-" * 40)
        for i, col in enumerate(columns, 1):
            lines.append(f"  {i}. {col}")
        
        return '\n'.join(lines)
    
    def _execute_truncate(self, parsed):
        """Execute TRUNCATE TABLE"""
        columns, _ = self.storage.read_table(parsed['table'])
        self.storage.write_table(parsed['table'], columns, [])
        return f"Table '{parsed['table']}' truncated successfully."
    
    def _execute_insert(self, parsed):
        """Execute INSERT INTO"""
        columns, rows = self.storage.read_table(parsed['table'])
        
        if len(parsed['values']) != len(columns):
            raise ValueError(f"Column count mismatch. Expected {len(columns)}, got {len(parsed['values'])}")
        
        self.storage.append_row(parsed['table'], parsed['values'])
        return "1 row inserted."
    
    def _execute_select(self, parsed):
        """Execute SELECT"""
        columns, rows = self.storage.read_table(parsed['table'])
        
        # Determine which columns to display
        if parsed['columns'] == ['*']:
            display_columns = columns
            col_indices = list(range(len(columns)))
        else:
            display_columns = parsed['columns']
            col_indices = []
            for col in display_columns:
                if col not in columns:
                    raise ValueError(f"Column '{col}' does not exist")
                col_indices.append(columns.index(col))
        
        # Filter rows based on WHERE clause
        filtered_rows = rows
        if parsed['where']:
            filtered_rows = self._filter_rows(columns, rows, parsed['where'])
        
        # Format output
        return self._format_table(display_columns, filtered_rows, col_indices)
    
    def _execute_delete(self, parsed):
        """Execute DELETE FROM"""
        columns, rows = self.storage.read_table(parsed['table'])
        
        if parsed['where']:
            remaining_rows = [row for row in rows if not self._matches_where(columns, row, parsed['where'])]
            deleted_count = len(rows) - len(remaining_rows)
        else:
            remaining_rows = []
            deleted_count = len(rows)
        
        self.storage.write_table(parsed['table'], columns, remaining_rows)
        return f"{deleted_count} row(s) deleted."
    
    def _execute_update(self, parsed):
        """Execute UPDATE"""
        columns, rows = self.storage.read_table(parsed['table'])
        
        # Validate columns in SET clause
        for col in parsed['updates'].keys():
            if col not in columns:
                raise ValueError(f"Column '{col}' does not exist")
        
        updated_count = 0
        updated_rows = []
        
        for row in rows:
            if parsed['where'] is None or self._matches_where(columns, row, parsed['where']):
                # Update this row
                new_row = row.copy()
                for col, val in parsed['updates'].items():
                    col_idx = columns.index(col)
                    new_row[col_idx] = val
                updated_rows.append(new_row)
                updated_count += 1
            else:
                updated_rows.append(row)
        
        self.storage.write_table(parsed['table'], columns, updated_rows)
        return f"{updated_count} row(s) updated."
    
    def _filter_rows(self, columns, rows, where_clause):
        """Filter rows based on WHERE clause"""
        return [row for row in rows if self._matches_where(columns, row, where_clause)]
    
    def _matches_where(self, columns, row, where_clause):
        """Check if a row matches WHERE condition"""
        col = where_clause['column']
        if col not in columns:
            raise ValueError(f"Column '{col}' does not exist")
        
        col_idx = columns.index(col)
        row_value = row[col_idx]
        
        if where_clause['operator'] == '=':
            return row_value == where_clause['value']
        
        return False
    
    def _format_table(self, columns, rows, col_indices):
        """Format query results as a table"""
        if not rows:
            return "0 rows returned."
        
        # Extract relevant columns from rows
        display_rows = []
        for row in rows:
            display_rows.append([row[i] for i in col_indices])
        
        # Calculate column widths
        col_widths = [len(col) for col in columns]
        for row in display_rows:
            for i, val in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(val)))
        
        # Build table
        lines = []
        
        # Header
        header = ' | '.join(col.ljust(col_widths[i]) for i, col in enumerate(columns))
        lines.append(header)
        lines.append('-' * len(header))
        
        # Rows
        for row in display_rows:
            line = ' | '.join(str(val).ljust(col_widths[i]) for i, val in enumerate(row))
            lines.append(line)
        
        lines.append(f"\n{len(display_rows)} row(s) returned.")
        
        return '\n'.join(lines)

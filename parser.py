
import re


class SQLParser:
    
    @staticmethod
    def parse(command):
        """Parse SQL command and return operation type and parameters"""
        command = command.strip().rstrip(';')
        
        # CREATE TABLE
        if command.upper().startswith('CREATE TABLE'):
            return SQLParser._parse_create(command)
        
        # DROP TABLE
        elif command.upper().startswith('DROP TABLE'):
            return SQLParser._parse_drop(command)
        
        # SHOW TABLES
        elif command.upper().startswith('SHOW TABLES'):
            return {'type': 'SHOW_TABLES'}
        
        # DESCRIBE TABLE
        elif command.upper().startswith('DESCRIBE'):
            return SQLParser._parse_describe(command)
        
        # INSERT INTO
        elif command.upper().startswith('INSERT INTO'):
            return SQLParser._parse_insert(command)
        
        # SELECT
        elif command.upper().startswith('SELECT'):
            return SQLParser._parse_select(command)
        
        # DELETE
        elif command.upper().startswith('DELETE FROM'):
            return SQLParser._parse_delete(command)
        
        # UPDATE
        elif command.upper().startswith('UPDATE'):
            return SQLParser._parse_update(command)
        
        # TRUNCATE
        elif command.upper().startswith('TRUNCATE TABLE'):
            return SQLParser._parse_truncate(command)
        
        else:
            raise ValueError(f"Unknown command: {command}")
    
    @staticmethod
    def _parse_create(command):
        """Parse CREATE TABLE command"""
        pattern = r'CREATE TABLE\s+(\w+)\s*\(([^)]+)\)'
        match = re.search(pattern, command, re.IGNORECASE)
        
        if not match:
            raise ValueError("Invalid CREATE TABLE syntax")
        
        table_name = match.group(1)
        columns_str = match.group(2)
        columns = [col.strip() for col in columns_str.split(',')]
        
        return {
            'type': 'CREATE',
            'table': table_name,
            'columns': columns
        }
    
    @staticmethod
    def _parse_insert(command):
        """Parse INSERT INTO command"""
        pattern = r'INSERT INTO\s+(\w+)\s+VALUES\s*\(([^)]+)\)'
        match = re.search(pattern, command, re.IGNORECASE)
        
        if not match:
            raise ValueError("Invalid INSERT syntax")
        
        table_name = match.group(1)
        values_str = match.group(2)
        
        # Parse values, handling quoted strings
        values = []
        current = ''
        in_quotes = False
        quote_char = None
        
        for char in values_str:
            if char in ('"', "'") and not in_quotes:
                in_quotes = True
                quote_char = char
            elif char == quote_char and in_quotes:
                in_quotes = False
                quote_char = None
            elif char == ',' and not in_quotes:
                values.append(current.strip().strip('"').strip("'"))
                current = ''
            else:
                current += char
        
        if current:
            values.append(current.strip().strip('"').strip("'"))
        
        return {
            'type': 'INSERT',
            'table': table_name,
            'values': values
        }
    
    @staticmethod
    def _parse_select(command):
        """Parse SELECT command"""
        # Extract columns
        select_pattern = r'SELECT\s+(.+?)\s+FROM\s+(\w+)'
        match = re.search(select_pattern, command, re.IGNORECASE)
        
        if not match:
            raise ValueError("Invalid SELECT syntax")
        
        columns_str = match.group(1).strip()
        table_name = match.group(2)
        
        if columns_str == '*':
            columns = ['*']
        else:
            columns = [col.strip() for col in columns_str.split(',')]
        
        # Extract WHERE clause if present
        where_clause = None
        where_pattern = r'WHERE\s+(.+)'
        where_match = re.search(where_pattern, command, re.IGNORECASE)
        
        if where_match:
            where_clause = SQLParser._parse_where(where_match.group(1))
        
        return {
            'type': 'SELECT',
            'table': table_name,
            'columns': columns,
            'where': where_clause
        }
    
    @staticmethod
    def _parse_delete(command):
        """Parse DELETE FROM command"""
        pattern = r'DELETE FROM\s+(\w+)'
        match = re.search(pattern, command, re.IGNORECASE)
        
        if not match:
            raise ValueError("Invalid DELETE syntax")
        
        table_name = match.group(1)
        
        # Extract WHERE clause
        where_clause = None
        where_pattern = r'WHERE\s+(.+)'
        where_match = re.search(where_pattern, command, re.IGNORECASE)
        
        if where_match:
            where_clause = SQLParser._parse_where(where_match.group(1))
        
        return {
            'type': 'DELETE',
            'table': table_name,
            'where': where_clause
        }
    
    @staticmethod
    def _parse_update(command):
        """Parse UPDATE command"""
        pattern = r'UPDATE\s+(\w+)\s+SET\s+(.+?)(?:\s+WHERE\s+(.+))?$'
        match = re.search(pattern, command, re.IGNORECASE)
        
        if not match:
            raise ValueError("Invalid UPDATE syntax")
        
        table_name = match.group(1)
        set_clause = match.group(2)
        where_str = match.group(3)
        
        # Parse SET clause
        updates = {}
        for assignment in set_clause.split(','):
            parts = assignment.split('=')
            if len(parts) != 2:
                raise ValueError("Invalid SET clause")
            col = parts[0].strip()
            val = parts[1].strip().strip('"').strip("'")
            updates[col] = val
        
        where_clause = None
        if where_str:
            where_clause = SQLParser._parse_where(where_str)
        
        return {
            'type': 'UPDATE',
            'table': table_name,
            'updates': updates,
            'where': where_clause
        }
    
    @staticmethod
    def _parse_drop(command):
        """Parse DROP TABLE command"""
        pattern = r'DROP TABLE\s+(\w+)'
        match = re.search(pattern, command, re.IGNORECASE)
        
        if not match:
            raise ValueError("Invalid DROP TABLE syntax")
        
        return {
            'type': 'DROP',
            'table': match.group(1)
        }
    
    @staticmethod
    def _parse_describe(command):
        """Parse DESCRIBE command"""
        pattern = r'DESCRIBE\s+(\w+)'
        match = re.search(pattern, command, re.IGNORECASE)
        
        if not match:
            raise ValueError("Invalid DESCRIBE syntax")
        
        return {
            'type': 'DESCRIBE',
            'table': match.group(1)
        }
    
    @staticmethod
    def _parse_truncate(command):
        """Parse TRUNCATE TABLE command"""
        pattern = r'TRUNCATE TABLE\s+(\w+)'
        match = re.search(pattern, command, re.IGNORECASE)
        
        if not match:
            raise ValueError("Invalid TRUNCATE syntax")
        
        return {
            'type': 'TRUNCATE',
            'table': match.group(1)
        }
    
    @staticmethod
    def _parse_where(where_str):
        """Parse WHERE clause"""
        # Simple equality check: column = value
        pattern = r'(\w+)\s*=\s*(.+)'
        match = re.search(pattern, where_str.strip())
        
        if not match:
            raise ValueError("Invalid WHERE clause")
        
        column = match.group(1)
        value = match.group(2).strip().strip('"').strip("'")
        
        return {
            'column': column,
            'operator': '=',
            'value': value
        }

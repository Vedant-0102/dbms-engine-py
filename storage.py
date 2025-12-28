
import os


class Storage:
    
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def _get_table_path(self, table_name):
        """Get file path for a table"""
        return os.path.join(self.data_dir, f"{table_name}.db")
    
    def table_exists(self, table_name):
        """Check if table exists"""
        return os.path.exists(self._get_table_path(table_name))
    
    def create_table(self, table_name, columns):
        """Create a new table file with column headers"""
        if self.table_exists(table_name):
            raise ValueError(f"Table '{table_name}' already exists")
        
        path = self._get_table_path(table_name)
        with open(path, 'w') as f:
            f.write(','.join(columns) + '\n')
    
    def read_table(self, table_name):
        """Read table data and return columns and rows"""
        if not self.table_exists(table_name):
            raise ValueError(f"Table '{table_name}' does not exist")
        
        path = self._get_table_path(table_name)
        with open(path, 'r') as f:
            lines = f.readlines()
        
        if not lines:
            raise ValueError(f"Table '{table_name}' is corrupted")
        
        columns = lines[0].strip().split(',')
        rows = []
        
        for line in lines[1:]:
            if line.strip():
                rows.append(line.strip().split(','))
        
        return columns, rows
    
    def write_table(self, table_name, columns, rows):
        """Write table data to file"""
        path = self._get_table_path(table_name)
        with open(path, 'w') as f:
            f.write(','.join(columns) + '\n')
            for row in rows:
                f.write(','.join(row) + '\n')
    
    def append_row(self, table_name, row):
        """Append a row to table"""
        if not self.table_exists(table_name):
            raise ValueError(f"Table '{table_name}' does not exist")
        
        path = self._get_table_path(table_name)
        with open(path, 'a') as f:
            f.write(','.join(row) + '\n')

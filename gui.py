
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from engine import DatabaseEngine
import os


class DatabaseGUI:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Database Engine - Professional Edition")
        self.root.geometry("1400x800")
        self.root.configure(bg='#f5f5f5')
        self.engine = DatabaseEngine()
        self.current_table = None
        self.command_history = []
        self.history_index = -1
        
        self.setup_styles()
        self.setup_ui()
        self.refresh_tables()
        self.show_welcome()
    
    def setup_styles(self):
        """Setup accessible color scheme"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Accessible colors - good contrast
        style.configure('TFrame', background='#f5f5f5')
        style.configure('TLabel', background='#f5f5f5', foreground='#333333', font=('Segoe UI', 9))
        style.configure('Title.TLabel', font=('Segoe UI', 12, 'bold'), 
                       background='#f5f5f5', foreground='#0066cc')
        style.configure('TButton', font=('Segoe UI', 9), padding=6)
        style.configure('Action.TButton', font=('Segoe UI', 9, 'bold'), padding=8)
        style.configure('Treeview', rowheight=26, font=('Segoe UI', 9))
        style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'))
    
    def setup_ui(self):
        """Setup the main GUI layout"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=2)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # === LEFT PANEL - Tables & Actions ===
        left_frame = ttk.LabelFrame(main_frame, text="📊 Database Tables", padding="10")
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        left_frame.rowconfigure(1, weight=1)
        
        # Search box
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(search_frame, text="🔍 Search:").pack(side=tk.LEFT, padx=(0, 5))
        self.table_search = ttk.Entry(search_frame, font=('Segoe UI', 10))
        self.table_search.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.table_search.bind('<KeyRelease>', self.filter_tables)
        
        # Tables listbox
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tables_listbox = tk.Listbox(list_frame, width=25, 
                                         font=('Segoe UI', 10),
                                         yscrollcommand=scrollbar.set,
                                         selectmode=tk.SINGLE,
                                         bg='white', fg='#333',
                                         selectbackground='#0066cc',
                                         selectforeground='white',
                                         relief=tk.SOLID, borderwidth=1)
        self.tables_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tables_listbox.yview)
        self.tables_listbox.bind('<<ListboxSelect>>', self.on_table_select)
        self.tables_listbox.bind('<Double-Button-1>', self.view_all_data)
        
        # Table info
        self.table_info = ttk.Label(left_frame, text="No table selected", 
                                    font=('Segoe UI', 9), foreground='#666')
        self.table_info.pack(fill=tk.X, pady=(0, 10))
        
        # Action buttons
        ttk.Label(left_frame, text="⚡ Quick Actions", 
                 font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W, pady=(5, 10))
        
        actions = [
            ("🔄 Refresh Tables", self.refresh_tables),
            ("➕ Create Table", self.create_table_wizard),
            ("📝 Insert Row", self.insert_row_wizard),
            ("✏️ Edit Row", self.edit_row_wizard),
            ("🗑️ Delete Row", self.delete_row_wizard),
            ("📋 View All Data", self.view_all_data),
            ("🔍 Search Data", self.search_wizard),
            ("📊 Table Info", self.view_schema),
            ("🗂️ Drop Table", self.drop_table),
        ]
        
        for text, command in actions:
            btn = ttk.Button(left_frame, text=text, command=command, style='Action.TButton')
            btn.pack(fill=tk.X, pady=2)
        
        # === CENTER PANEL - SQL Editor & Data Grid ===
        center_frame = ttk.Frame(main_frame)
        center_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        center_frame.columnconfigure(0, weight=1)
        center_frame.rowconfigure(1, weight=1)
        center_frame.rowconfigure(3, weight=2)
        
        # SQL Editor
        ttk.Label(center_frame, text="💻 SQL Editor", style='Title.TLabel').grid(
            row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        editor_frame = ttk.Frame(center_frame, relief=tk.SOLID, borderwidth=1)
        editor_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        editor_frame.columnconfigure(0, weight=1)
        editor_frame.rowconfigure(0, weight=1)
        
        self.sql_input = scrolledtext.ScrolledText(editor_frame, height=6, wrap=tk.WORD,
                                                   font=('Consolas', 11),
                                                   bg='#ffffff', fg='#000000',
                                                   insertbackground='black',
                                                   selectbackground='#0066cc',
                                                   selectforeground='white',
                                                   padx=10, pady=10)
        self.sql_input.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Toolbar
        toolbar = ttk.Frame(center_frame)
        toolbar.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(toolbar, text="▶️ Execute (F5)", command=self.execute_command,
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="🗑️ Clear", command=self.clear_input).pack(side=tk.LEFT, padx=5)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        ttk.Label(toolbar, text="Templates:", font=('Segoe UI', 9, 'bold')).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(toolbar, text="SELECT", command=self.template_select).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="INSERT", command=self.template_insert).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="UPDATE", command=self.template_update).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="DELETE", command=self.template_delete).pack(side=tk.LEFT, padx=2)
        
        self.root.bind('<F5>', lambda e: self.execute_command())
        
        # Data Grid
        grid_header = ttk.Frame(center_frame)
        grid_header.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        ttk.Label(grid_header, text="📊 Data View", style='Title.TLabel').pack(side=tk.LEFT)
        self.result_count = ttk.Label(grid_header, text="", font=('Segoe UI', 9, 'bold'),
                                      foreground='#0066cc')
        self.result_count.pack(side=tk.RIGHT)
        
        results_frame = ttk.Frame(center_frame, relief=tk.SOLID, borderwidth=1)
        results_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        center_frame.rowconfigure(4, weight=3)
        
        # Treeview
        tree_scroll_y = ttk.Scrollbar(results_frame, orient=tk.VERTICAL)
        tree_scroll_x = ttk.Scrollbar(results_frame, orient=tk.HORIZONTAL)
        
        self.results_tree = ttk.Treeview(results_frame,
                                         yscrollcommand=tree_scroll_y.set,
                                         xscrollcommand=tree_scroll_x.set,
                                         selectmode='browse')
        
        tree_scroll_y.config(command=self.results_tree.yview)
        tree_scroll_x.config(command=self.results_tree.xview)
        
        self.results_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_scroll_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        tree_scroll_x.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Context menu
        self.tree_menu = tk.Menu(self.results_tree, tearoff=0)
        self.tree_menu.add_command(label="📋 Copy Row", command=self.copy_row)
        self.tree_menu.add_command(label="✏️ Edit Row", command=self.edit_selected_row)
        self.tree_menu.add_command(label="🗑️ Delete Row", command=self.delete_selected_row)
        self.results_tree.bind('<Button-3>', self.show_tree_menu)
        self.results_tree.bind('<Double-Button-1>', self.edit_selected_row)
        
        # === RIGHT PANEL - Console ===
        right_frame = ttk.LabelFrame(main_frame, text="🖥️ Interactive Console", padding="10")
        right_frame.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)
        
        # Quick commands
        ttk.Label(right_frame, text="Quick Commands:", font=('Segoe UI', 9, 'bold')).pack(
            anchor=tk.W, pady=(0, 5))
        
        quick_cmds = [
            ("📋 SHOW TABLES", "SHOW TABLES"),
            ("📊 DESCRIBE", "DESCRIBE {table}"),
            ("🔢 COUNT", "SELECT COUNT(*) FROM {table}"),
            ("🗑️ TRUNCATE", "TRUNCATE TABLE {table}"),
        ]
        
        for label, cmd in quick_cmds:
            btn = ttk.Button(right_frame, text=label,
                           command=lambda c=cmd: self.quick_console(c))
            btn.pack(fill=tk.X, pady=2)
        
        ttk.Separator(right_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Console output
        console_frame = ttk.Frame(right_frame, relief=tk.SOLID, borderwidth=1)
        console_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.console = scrolledtext.ScrolledText(console_frame, wrap=tk.WORD,
                                                 font=('Consolas', 9),
                                                 bg='#1e1e1e', fg='#00ff00',
                                                 insertbackground='#00ff00',
                                                 padx=10, pady=10)
        self.console.pack(fill=tk.BOTH, expand=True)
        
        # Tags for colored output
        self.console.tag_config('success', foreground='#00ff00', font=('Consolas', 9, 'bold'))
        self.console.tag_config('error', foreground='#ff4444', font=('Consolas', 9, 'bold'))
        self.console.tag_config('info', foreground='#00bfff', font=('Consolas', 9, 'bold'))
        self.console.tag_config('prompt', foreground='#ffffff', font=('Consolas', 9, 'bold'))
        
        # Console input
        input_frame = ttk.Frame(right_frame)
        input_frame.pack(fill=tk.X)
        input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="SQL>", font=('Consolas', 10, 'bold'),
                 foreground='#00ff00', background='#f5f5f5').grid(row=0, column=0, padx=(0, 5))
        
        self.console_input = ttk.Entry(input_frame, font=('Consolas', 10))
        self.console_input.grid(row=0, column=1, sticky=(tk.W, tk.E))
        self.console_input.bind('<Return>', self.execute_console)
        self.console_input.bind('<Up>', self.history_up)
        self.console_input.bind('<Down>', self.history_down)
        
        ttk.Button(input_frame, text="▶️", command=self.execute_console).grid(row=0, column=2, padx=(5, 0))
    
    def show_welcome(self):
        """Show welcome message"""
        welcome = """╔══════════════════════════════════════════╗
║  Mini Database Engine - Ready!           ║
╚══════════════════════════════════════════╝

• Double-click tables to view data
• Type SQL commands below
• Press ↑/↓ for command history
• F5 to execute from editor

"""
        self.log_console(welcome, 'info')
    
    def log_console(self, message, tag='info'):
        """Log to console"""
        self.console.insert(tk.END, message, tag)
        self.console.see(tk.END)
    
    def filter_tables(self, event=None):
        """Filter tables by search"""
        search = self.table_search.get().lower()
        self.tables_listbox.delete(0, tk.END)
        
        data_dir = self.engine.storage.data_dir
        if os.path.exists(data_dir):
            for file in sorted(os.listdir(data_dir)):
                if file.endswith('.db'):
                    table_name = file[:-3]
                    if search in table_name.lower():
                        self.tables_listbox.insert(tk.END, f"  📊 {table_name}")
    
    def refresh_tables(self):
        """Refresh tables list"""
        self.table_search.delete(0, tk.END)
        self.filter_tables()
        self.log_console("Tables refreshed\n", 'info')
    
    def on_table_select(self, event):
        """Handle table selection"""
        selection = self.tables_listbox.curselection()
        if selection:
            table_text = self.tables_listbox.get(selection[0])
            table_name = table_text.replace('📊', '').strip()
            self.current_table = table_name
            try:
                columns, rows = self.engine.storage.read_table(table_name)
                info = f"{table_name}: {len(columns)} columns, {len(rows)} rows"
                self.table_info.config(text=info)
            except:
                self.table_info.config(text=table_name)
    
    def view_all_data(self, event=None):
        """View all data from selected table"""
        if not self.current_table:
            messagebox.showwarning("No Table", "Select a table first")
            return
        self.sql_input.delete(1.0, tk.END)
        self.sql_input.insert(1.0, f"SELECT * FROM {self.current_table}")
        self.execute_command()
    
    def execute_command(self):
        """Execute SQL from editor"""
        command = self.sql_input.get(1.0, tk.END).strip()
        
        if not command:
            messagebox.showwarning("Empty", "Enter a SQL command")
            return
        
        self.log_console(f"\n▶️ Executing: {command}\n", 'info')
        
        try:
            result = self.engine.execute(command)
            
            if command.strip().upper().startswith('SELECT'):
                self.display_select_results(command)
                self.log_console(f"✓ Query executed\n", 'success')
            else:
                self.log_console(f"✓ {result}\n", 'success')
                self.clear_results_tree()
                self.refresh_tables()
            
        except Exception as e:
            self.log_console(f"✗ Error: {e}\n", 'error')
            messagebox.showerror("Error", str(e))
    
    def display_select_results(self, command):
        """Display SELECT query results in treeview"""
        try:
            parsed = self.engine.parser.parse(command)
            columns, rows = self.engine.storage.read_table(parsed['table'])
            
            # Determine which columns to display
            if parsed['columns'] == ['*']:
                display_columns = columns
                col_indices = list(range(len(columns)))
            else:
                display_columns = parsed['columns']
                col_indices = [columns.index(col) for col in display_columns]
            
            # Filter rows if WHERE clause exists
            if parsed['where']:
                rows = self.engine._filter_rows(columns, rows, parsed['where'])
            
            # Clear existing tree
            self.clear_results_tree()
            
            # Setup columns
            self.results_tree['columns'] = display_columns
            self.results_tree['show'] = 'headings'
            
            for col in display_columns:
                self.results_tree.heading(col, text=col)
                self.results_tree.column(col, width=100, anchor=tk.W)
            
            # Insert rows
            for row in rows:
                display_row = [row[i] for i in col_indices]
                self.results_tree.insert('', tk.END, values=display_row)
            
            self.result_count.config(text=f"{len(rows)} rows")
            
        except Exception as e:
            self.log_console(f"Display error: {e}\n", 'error')
    
    def clear_results_tree(self):
        """Clear the results treeview"""
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        self.results_tree['columns'] = []
        self.result_count.config(text="")
    
    def clear_input(self):
        """Clear SQL editor"""
        self.sql_input.delete(1.0, tk.END)
    
    # Template methods
    def template_select(self):
        if self.current_table:
            self.sql_input.delete(1.0, tk.END)
            self.sql_input.insert(1.0, f"SELECT * FROM {self.current_table}")
        else:
            messagebox.showinfo("Tip", "Select a table first")
    
    def template_insert(self):
        if self.current_table:
            try:
                columns, _ = self.engine.storage.read_table(self.current_table)
                values = ", ".join([f"'value{i+1}'" for i in range(len(columns))])
                self.sql_input.delete(1.0, tk.END)
                self.sql_input.insert(1.0, f"INSERT INTO {self.current_table} VALUES ({values})")
            except:
                pass
        else:
            messagebox.showinfo("Tip", "Select a table first")
    
    def template_update(self):
        if self.current_table:
            self.sql_input.delete(1.0, tk.END)
            self.sql_input.insert(1.0, f"UPDATE {self.current_table} SET column = 'value' WHERE id = 1")
        else:
            messagebox.showinfo("Tip", "Select a table first")
    
    def template_delete(self):
        if self.current_table:
            self.sql_input.delete(1.0, tk.END)
            self.sql_input.insert(1.0, f"DELETE FROM {self.current_table} WHERE id = 1")
        else:
            messagebox.showinfo("Tip", "Select a table first")
    
    # Console methods
    def execute_console(self, event=None):
        """Execute from console"""
        command = self.console_input.get().strip()
        if not command:
            return
        
        self.command_history.append(command)
        self.history_index = len(self.command_history)
        
        self.log_console(f"\nSQL> ", 'prompt')
        self.log_console(f"{command}\n", 'info')
        
        try:
            result = self.engine.execute(command)
            
            if command.strip().upper().startswith('SELECT'):
                self.display_select_results(command)
                self.log_console(f"✓ See Data View\n", 'success')
            else:
                self.log_console(f"✓ {result}\n", 'success')
                self.refresh_tables()
            
        except Exception as e:
            self.log_console(f"✗ Error: {e}\n", 'error')
        
        self.console_input.delete(0, tk.END)
    
    def quick_console(self, cmd_template):
        """Quick console command"""
        if '{table}' in cmd_template:
            if not self.current_table:
                messagebox.showwarning("No Table", "Select a table first")
                return
            cmd = cmd_template.replace('{table}', self.current_table)
        else:
            cmd = cmd_template
        
        self.console_input.delete(0, tk.END)
        self.console_input.insert(0, cmd)
        self.execute_console()
    
    def history_up(self, event):
        """Navigate history up"""
        if self.command_history and self.history_index > 0:
            self.history_index -= 1
            self.console_input.delete(0, tk.END)
            self.console_input.insert(0, self.command_history[self.history_index])
    
    def history_down(self, event):
        """Navigate history down"""
        if self.command_history and self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.console_input.delete(0, tk.END)
            self.console_input.insert(0, self.command_history[self.history_index])
        elif self.history_index >= len(self.command_history) - 1:
            self.history_index = len(self.command_history)
            self.console_input.delete(0, tk.END)
    
    # Context menu
    def show_tree_menu(self, event):
        """Show context menu"""
        item = self.results_tree.identify_row(event.y)
        if item:
            self.results_tree.selection_set(item)
            self.tree_menu.post(event.x_root, event.y_root)
    
    def copy_row(self):
        """Copy row"""
        selection = self.results_tree.selection()
        if selection:
            item = selection[0]
            values = self.results_tree.item(item)['values']
            self.root.clipboard_clear()
            self.root.clipboard_append(str(values))
            self.log_console("📋 Row copied\n", 'info')
    
    # Wizard methods
    def create_table_wizard(self):
        """Create table wizard"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Create New Table")
        dialog.geometry("500x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="CREATE NEW TABLE", font=('Segoe UI', 14, 'bold'),
                fg='#0066cc').pack(pady=15)
        
        tk.Label(dialog, text="Table Name:", font=('Segoe UI', 10, 'bold')).pack(pady=(10, 5))
        table_entry = tk.Entry(dialog, font=('Segoe UI', 11), width=40)
        table_entry.pack(pady=(0, 15))
        table_entry.insert(0, "my_table")
        
        tk.Label(dialog, text="Columns (one per line):", font=('Segoe UI', 10, 'bold')).pack(pady=(10, 5))
        cols_text = scrolledtext.ScrolledText(dialog, width=40, height=8, font=('Consolas', 10))
        cols_text.pack(pady=(0, 15))
        cols_text.insert(1.0, "id\nname\nvalue")
        
        # SQL Preview
        tk.Label(dialog, text="Generated SQL:", font=('Segoe UI', 10, 'bold')).pack(pady=(10, 5))
        sql_preview = scrolledtext.ScrolledText(dialog, width=40, height=4, font=('Consolas', 10),
                                                bg='#f0f0f0', fg='#333')
        sql_preview.pack(pady=(0, 15))
        
        def update_preview(event=None):
            table_name = table_entry.get().strip()
            columns = [c.strip() for c in cols_text.get(1.0, tk.END).strip().split('\n') if c.strip()]
            if table_name and columns:
                command = f"CREATE TABLE {table_name} ({', '.join(columns)})"
                sql_preview.delete(1.0, tk.END)
                sql_preview.insert(1.0, command)
        
        table_entry.bind('<KeyRelease>', update_preview)
        cols_text.bind('<KeyRelease>', update_preview)
        update_preview()
        
        def generate_to_editor():
            command = sql_preview.get(1.0, tk.END).strip()
            if command:
                self.sql_input.delete(1.0, tk.END)
                self.sql_input.insert(1.0, command)
                self.log_console(f"📝 SQL generated in editor\n", 'info')
                dialog.destroy()
        
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="📝 Generate to Editor", command=generate_to_editor,
                 font=('Segoe UI', 10, 'bold'), bg='#28a745', fg='white',
                 relief=tk.FLAT, cursor='hand2', pady=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="❌ Cancel", command=dialog.destroy,
                 font=('Segoe UI', 10), bg='#dc3545', fg='white',
                 relief=tk.FLAT, cursor='hand2', pady=10).pack(side=tk.LEFT, padx=5)
    
    def insert_row_wizard(self):
        """Insert row wizard"""
        if not self.current_table:
            messagebox.showwarning("No Table", "Select a table first")
            return
        
        try:
            columns, _ = self.engine.storage.read_table(self.current_table)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Insert Row - {self.current_table}")
        dialog.geometry("550x600")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text=f"INSERT INTO {self.current_table}",
                font=('Segoe UI', 14, 'bold'), fg='#0066cc').pack(pady=15)
        
        canvas = tk.Canvas(dialog, highlightthickness=0, height=250)
        scrollbar = ttk.Scrollbar(dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>",
                             lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        entries = {}
        for col in columns:
            frame = tk.Frame(scrollable_frame)
            frame.pack(fill=tk.X, padx=30, pady=8)
            tk.Label(frame, text=f"{col}:", width=15, anchor=tk.W,
                    font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=30, font=('Segoe UI', 10))
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            entries[col] = entry
        
        canvas.pack(side="top", fill="x", padx=(20, 0), pady=10)
        scrollbar.pack(side="right", fill="y", pady=10, anchor='ne')
        
        # SQL Preview
        tk.Label(dialog, text="Generated SQL:", font=('Segoe UI', 10, 'bold')).pack(pady=(10, 5))
        sql_preview = scrolledtext.ScrolledText(dialog, width=50, height=4, font=('Consolas', 10),
                                                bg='#f0f0f0', fg='#333', wrap=tk.WORD)
        sql_preview.pack(pady=(0, 15), padx=20, fill=tk.X)
        
        def update_preview(event=None):
            values = [entries[col].get() for col in columns]
            values_str = ", ".join([f"'{v}'" if v else "''" for v in values])
            command = f"INSERT INTO {self.current_table} VALUES ({values_str})"
            sql_preview.delete(1.0, tk.END)
            sql_preview.insert(1.0, command)
        
        for entry in entries.values():
            entry.bind('<KeyRelease>', update_preview)
        
        update_preview()
        
        def generate_to_editor():
            command = sql_preview.get(1.0, tk.END).strip()
            if command:
                self.sql_input.delete(1.0, tk.END)
                self.sql_input.insert(1.0, command)
                self.log_console(f"📝 SQL generated in editor\n", 'info')
                dialog.destroy()
        
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="📝 Generate to Editor", command=generate_to_editor,
                 font=('Segoe UI', 10, 'bold'), bg='#28a745', fg='white',
                 relief=tk.FLAT, cursor='hand2', pady=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="❌ Cancel", command=dialog.destroy,
                 font=('Segoe UI', 10), bg='#dc3545', fg='white',
                 relief=tk.FLAT, cursor='hand2', pady=10).pack(side=tk.LEFT, padx=5)
    
    def edit_row_wizard(self):
        """Edit row wizard"""
        selection = self.results_tree.selection()
        if not selection or not self.current_table:
            messagebox.showinfo("Info", "Select a row from data view first")
            return
        self.edit_selected_row()
    
    def edit_selected_row(self, event=None):
        """Edit selected row"""
        selection = self.results_tree.selection()
        if not selection or not self.current_table:
            return
        
        item = selection[0]
        values = list(self.results_tree.item(item)['values'])
        columns = list(self.results_tree['columns'])
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit Row - {self.current_table}")
        dialog.geometry("550x600")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text=f"EDIT ROW IN {self.current_table}",
                font=('Segoe UI', 14, 'bold'), fg='#ff8c00').pack(pady=15)
        
        canvas = tk.Canvas(dialog, highlightthickness=0, height=250)
        scrollbar = ttk.Scrollbar(dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>",
                             lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        entries = {}
        for i, col in enumerate(columns):
            frame = tk.Frame(scrollable_frame)
            frame.pack(fill=tk.X, padx=30, pady=8)
            tk.Label(frame, text=f"{col}:", width=15, anchor=tk.W,
                    font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=30, font=('Segoe UI', 10))
            entry.insert(0, values[i])
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            entries[col] = entry
        
        canvas.pack(side="top", fill="x", padx=(20, 0), pady=10)
        scrollbar.pack(side="right", fill="y", pady=10, anchor='ne')
        
        # SQL Preview
        tk.Label(dialog, text="Generated SQL:", font=('Segoe UI', 10, 'bold')).pack(pady=(10, 5))
        sql_preview = scrolledtext.ScrolledText(dialog, width=50, height=4, font=('Consolas', 10),
                                                bg='#f0f0f0', fg='#333', wrap=tk.WORD)
        sql_preview.pack(pady=(0, 15), padx=20, fill=tk.X)
        
        def update_preview(event=None):
            first_col = columns[0]
            first_val = values[0]
            set_parts = []
            for col in columns:
                new_val = entries[col].get()
                set_parts.append(f"{col} = '{new_val}'")
            command = f"UPDATE {self.current_table} SET {', '.join(set_parts)} WHERE {first_col} = '{first_val}'"
            sql_preview.delete(1.0, tk.END)
            sql_preview.insert(1.0, command)
        
        for entry in entries.values():
            entry.bind('<KeyRelease>', update_preview)
        
        update_preview()
        
        def generate_to_editor():
            command = sql_preview.get(1.0, tk.END).strip()
            if command:
                self.sql_input.delete(1.0, tk.END)
                self.sql_input.insert(1.0, command)
                self.log_console(f"📝 SQL generated in editor\n", 'info')
                dialog.destroy()
        
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="📝 Generate to Editor", command=generate_to_editor,
                 font=('Segoe UI', 10, 'bold'), bg='#28a745', fg='white',
                 relief=tk.FLAT, cursor='hand2', pady=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="❌ Cancel", command=dialog.destroy,
                 font=('Segoe UI', 10), bg='#dc3545', fg='white',
                 relief=tk.FLAT, cursor='hand2', pady=10).pack(side=tk.LEFT, padx=5)
    
    def delete_row_wizard(self):
        """Delete row wizard"""
        selection = self.results_tree.selection()
        if not selection or not self.current_table:
            messagebox.showinfo("Info", "Select a row from data view first")
            return
        self.delete_selected_row()
    
    def delete_selected_row(self, event=None):
        """Delete selected row"""
        selection = self.results_tree.selection()
        if not selection or not self.current_table:
            return
        
        item = selection[0]
        values = list(self.results_tree.item(item)['values'])
        columns = list(self.results_tree['columns'])
        
        first_col = columns[0]
        first_val = values[0]
        
        command = f"DELETE FROM {self.current_table} WHERE {first_col} = '{first_val}'"
        
        # Show confirmation dialog with SQL preview
        dialog = tk.Toplevel(self.root)
        dialog.title("Confirm Delete")
        dialog.geometry("500x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="⚠️ DELETE ROW", font=('Segoe UI', 14, 'bold'),
                fg='#dc3545').pack(pady=15)
        
        tk.Label(dialog, text="This will execute the following SQL:",
                font=('Segoe UI', 10)).pack(pady=(10, 5))
        
        sql_preview = scrolledtext.ScrolledText(dialog, width=50, height=4, font=('Consolas', 10),
                                                bg='#f0f0f0', fg='#333', wrap=tk.WORD)
        sql_preview.pack(pady=(0, 15), padx=20, fill=tk.X)
        sql_preview.insert(1.0, command)
        sql_preview.config(state=tk.DISABLED)
        
        def generate_to_editor():
            self.sql_input.delete(1.0, tk.END)
            self.sql_input.insert(1.0, command)
            self.log_console(f"📝 SQL generated in editor\n", 'info')
            dialog.destroy()
        
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="📝 Generate to Editor", command=generate_to_editor,
                 font=('Segoe UI', 10, 'bold'), bg='#28a745', fg='white',
                 relief=tk.FLAT, cursor='hand2', pady=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="❌ Cancel", command=dialog.destroy,
                 font=('Segoe UI', 10), bg='#6c757d', fg='white',
                 relief=tk.FLAT, cursor='hand2', pady=10).pack(side=tk.LEFT, padx=5)
    
    def search_wizard(self):
        """Search wizard"""
        if not self.current_table:
            messagebox.showwarning("No Table", "Select a table first")
            return
        
        try:
            columns, _ = self.engine.storage.read_table(self.current_table)
        except:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Search - {self.current_table}")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="🔍 SEARCH", font=('Segoe UI', 14, 'bold'),
                fg='#0066cc').pack(pady=15)
        
        tk.Label(dialog, text="Column:", font=('Segoe UI', 10, 'bold')).pack(pady=(10, 5))
        col_combo = ttk.Combobox(dialog, values=columns, font=('Segoe UI', 10), width=40)
        col_combo.pack(pady=(0, 15))
        if columns:
            col_combo.set(columns[0])
        
        tk.Label(dialog, text="Value:", font=('Segoe UI', 10, 'bold')).pack(pady=(10, 5))
        val_entry = tk.Entry(dialog, font=('Segoe UI', 10), width=42)
        val_entry.pack(pady=(0, 15))
        
        # SQL Preview
        tk.Label(dialog, text="Generated SQL:", font=('Segoe UI', 10, 'bold')).pack(pady=(10, 5))
        sql_preview = scrolledtext.ScrolledText(dialog, width=50, height=4, font=('Consolas', 10),
                                                bg='#f0f0f0', fg='#333', wrap=tk.WORD)
        sql_preview.pack(pady=(0, 15), padx=20, fill=tk.X)
        
        def update_preview(event=None):
            col = col_combo.get()
            val = val_entry.get()
            if col:
                command = f"SELECT * FROM {self.current_table} WHERE {col} = '{val}'"
                sql_preview.delete(1.0, tk.END)
                sql_preview.insert(1.0, command)
        
        col_combo.bind('<<ComboboxSelected>>', update_preview)
        val_entry.bind('<KeyRelease>', update_preview)
        update_preview()
        
        def generate_to_editor():
            command = sql_preview.get(1.0, tk.END).strip()
            if command:
                self.sql_input.delete(1.0, tk.END)
                self.sql_input.insert(1.0, command)
                self.log_console(f"📝 SQL generated in editor\n", 'info')
                dialog.destroy()
        
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="📝 Generate to Editor", command=generate_to_editor,
                 font=('Segoe UI', 10, 'bold'), bg='#28a745', fg='white',
                 relief=tk.FLAT, cursor='hand2', pady=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="❌ Cancel", command=dialog.destroy,
                 font=('Segoe UI', 10), bg='#dc3545', fg='white',
                 relief=tk.FLAT, cursor='hand2', pady=10).pack(side=tk.LEFT, padx=5)
    
    def view_schema(self):
        """View schema"""
        if not self.current_table:
            messagebox.showwarning("No Table", "Select a table first")
            return
        
        self.console_input.delete(0, tk.END)
        self.console_input.insert(0, f"DESCRIBE {self.current_table}")
        self.execute_console()
    
    def drop_table(self):
        """Drop table"""
        if not self.current_table:
            messagebox.showwarning("No Table", "Select a table first")
            return
        
        command = f"DROP TABLE {self.current_table}"
        
        # Show confirmation dialog with SQL preview
        dialog = tk.Toplevel(self.root)
        dialog.title("Confirm Drop Table")
        dialog.geometry("500x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="⚠️ DROP TABLE", font=('Segoe UI', 14, 'bold'),
                fg='#dc3545').pack(pady=15)
        
        tk.Label(dialog, text=f"This will permanently delete '{self.current_table}':",
                font=('Segoe UI', 10)).pack(pady=(10, 5))
        
        sql_preview = scrolledtext.ScrolledText(dialog, width=50, height=4, font=('Consolas', 10),
                                                bg='#f0f0f0', fg='#333', wrap=tk.WORD)
        sql_preview.pack(pady=(0, 15), padx=20, fill=tk.X)
        sql_preview.insert(1.0, command)
        sql_preview.config(state=tk.DISABLED)
        
        def generate_to_editor():
            self.sql_input.delete(1.0, tk.END)
            self.sql_input.insert(1.0, command)
            self.log_console(f"📝 SQL generated in editor\n", 'info')
            dialog.destroy()
        
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="📝 Generate to Editor", command=generate_to_editor,
                 font=('Segoe UI', 10, 'bold'), bg='#28a745', fg='white',
                 relief=tk.FLAT, cursor='hand2', pady=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="❌ Cancel", command=dialog.destroy,
                 font=('Segoe UI', 10), bg='#6c757d', fg='white',
                 relief=tk.FLAT, cursor='hand2', pady=10).pack(side=tk.LEFT, padx=5)


def main():
    root = tk.Tk()
    app = DatabaseGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

import tkinter as tk
"""Allows the Displaying of Combat Calculation Interface"""


# Convert a 2d list table to a dictionary
def list_to_dict(starting_list, headings):

    output_dict = {}

    for row in starting_list:
        row_dict = {}

        for column, entry in enumerate(row, start=1):
            row_dict[headings[column]] = entry

        output_dict[row[0]] = row_dict

    return output_dict


# A table to put info in
class EntryTable:

    def __init__(self, master, title_str, headings_list, n_rows=1):
        self.master = master
        self.title_str = title_str
        self.headings = headings_list
        self.n_rows = n_rows

        self.frame = tk.Frame(self.master)
        self.frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.frame_widgets = []

        self.grid_frame = tk.Frame(self.frame)

        self.n_col = len(self.headings)

        self.entries_str = [['' for _ in range(self.n_col)] for _ in range(self.n_rows)]
        self.entries = []

        self.create_title()
        self.create_grid()

        self.pack()

    def pack(self):
        for item in self.frame_widgets:
            item.pack()

    # Creates the table title
    def create_title(self):
        title = tk.Label(self.frame, text=self.title_str, font='50')
        self.frame_widgets.append(title)

    # Creates the table as a grid of entry widgets
    def create_grid(self):

        self.frame_widgets.append(self.grid_frame)

        if len(self.headings) == 0:
            raise ValueError

        for i, heading in enumerate(self.headings):
            heading_label = tk.Label(self.grid_frame, text=heading)
            heading_label.grid(row=0, column=i, sticky=tk.W)

        for row in range(self.n_rows):
            row_entries = []
            for column in range(len(self.headings)):

                entry_field = tk.Entry(self.grid_frame)
                entry_field.grid(row=row+1, column=column, sticky=tk.W)

                row_entries.append(entry_field)

            self.entries.append(row_entries)

    # Gets entries from entry widget and puts in a 2d list
    def get_entries(self):

        for column in range(self.n_col):
            row_entries = []
            for row in range(self.n_rows):

                entry_str = self.entries[row+1][column].get()

                row_entries.append(entry_str)

            self.entries_str.append(row_entries)


# A table with a '+' button to extend it
class ExtendableTable(EntryTable):

    def __init__(self, master, title_str, headings_list):
        super().__init__(master, title_str, headings_list)

        self.create_plus()

        self.pack()

    def create_plus(self):
        plus_button = tk.Button(self.frame, text='+', bd='3', command=self.extend)

        self.frame_widgets.append(plus_button)

    def extend(self):
        self.n_rows += 1

        row_entries = []
        for column in range(len(self.headings)):

            entry_field = tk.Entry(self.grid_frame)
            entry_field.grid(row=self.n_rows, column=column, sticky=tk.W)

            row_entries.append(entry_field)

        self.entries.append(row_entries)

        self.pack()


# A sheet is one of many to be displayed by one window
class Sheet:

    def __init__(self, sheet_name, window):
        self.master = window.master

        self.name = sheet_name
        self.size = window.size

        self.menubar = window.menubar

        self.master = None
        self.commands = {}

        self.reset()

    def reset(self):
        self.master = tk.Tk()

        self.master.title(self.name)
        self.master.geometry(self.size)

        self.master.config(menu=self.menubar)

    # Creates a frame with an extendable table with given title and headings
    def create_xtable(self, title_str, headings_list):
        table = ExtendableTable(self.master, title_str, headings_list)
        self.master = table.master


# A window with functions to place items within
class Window:

    def __init__(self, window_name, size):
        self.name = window_name
        self.size = size

        self.master = tk.Tk()
        self.current_sheet = None
        self.sheets = {}
        self.sheet_order = []

        self.menubar = tk.Menu(self.master)

        self.master.title(self.name)
        self.master.geometry(self.size)

    def mainloop(self):
        self.master.mainloop()

    # Creates a sheet to display
    def create_sheet(self, sheet_name):
        sheet = Sheet(sheet_name, self.size, self.menubar)

        self.sheets[sheet_name] = sheet
        self.sheet_order.append(sheet_name)

        return sheet

    # Moves to the next sheet
    def next_sheet(self):
        current_no = self.sheet_order.index(self.current_sheet.name)
        if current_no < len(self.sheet_order):
            current_no += 1
        self.current_sheet = self.sheets[self.sheet_order[current_no]]

    # Moves to the previous sheet
    def prev_sheet(self):
        current_no = self.sheet_order.index(self.current_sheet.name)
        if current_no > 0:
            current_no -= 1
        self.current_sheet = self.sheets[self.sheet_order[current_no]]

    # Resets the currently displayed sheet
    def reset_sheet(self):
        self.current_sheet.reset()

    # Resets all sheets and returns to first sheet
    def reset_window(self):

        for sheet_name in self.sheets:
            self.sheets[sheet_name].reset()

        self.current_sheet = self.sheets[self.sheet_order[0]]

    # Saves entries on a sheet (auto when changing sheet)
    def save_sheet(self):
        pass

    # Creates the drop menu to help manipulate the data
    def create_menu(self):

        # File cascade
        file = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='File', menu=file)

        file.add_command(label='Reset', command=self.reset_sheet)
        file.add_command(label='Reset All', command=self.reset_window)
        file.add_command(label='Save', command=self.save_sheet)
        file.add_separator()
        file.add_command(label='Exit', command=self.master.destroy)

        edit = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Edit', menu=edit)

        self.menubar.add_separator()
        self.menubar.add_command(label='Previous', command=self.prev_sheet)
        self.menubar.add_command(label='Next', command=self.next_sheet)

        self.master.config(menu=self.menubar)


# Window for the combat calculator
class CalculatorWindow(Window):
    name = 'DnD Combat Calculator'
    size = '1400x700'

    def __init__(self):
        super().__init__(CalculatorWindow.name, CalculatorWindow.size)

        self.create_ent_sheet()

    # Creates the creature and player entry sheet
    def create_ent_sheet(self):
        sheet = self.create_sheet('Creature and Player Entry')

        sheet.create_xtable('Creatures', ['Creature Type', 'Number of Creatures', 'Number of Groups'])
        sheet.create_xtable('Players', ['Player Name'])

    # Creates the initiative rolls sheet
    def create_init_sheet(self):
        pass

    # Creates the health tracker sheet
    def create_hp_sheet(self):
        pass

    # Runs the window
    def run(self):
        self.create_menu()

        self.mainloop()




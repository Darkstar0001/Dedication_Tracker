import tkinter as tk
from tkinter import messagebox, colorchooser
from datetime import date
from tkcalendar import Calendar
from os.path import exists, getsize
from math import log
import csv
import dedicationsharedfunctions as util
# matplotlib is imported within GraphCreator.graph_create(), to improve program startup speed


class GraphCreator(tk.Frame):
    __slots__ = ('line_dash_text', 'line_style', 'nil_type', 'date_type', 'color_chooser', 'remove_category_button',
                 'graph_type', 'zero_type', 'create_button', 'nil_type_box', 'zero_type_box', 'chosen_color_mode',
                 'end_date', 'min_value_mode', 'min_value_hours', 'line_style_header', 'max_value_hours',
                 'target_value_box', 'max_value_seconds', 'max_value_mode', 'date_win', 'graph_config_categories',
                 'style_overwrite', 'exclude_today', 'graph_name_entry', 'chosen_categories',
                 'chosen_line_styles', 'target_value_box_two', 'all_categories', 'colon_3', 'color_overwrite',
                 'first_time_date', 'save_options', 'line_dot_style', 'days_ago_field', 'chosen_color',
                 'saved_categories', 'colon_2', 'add_category_button', 'load_options', 'dedication_mode_file',
                 'chosen_color_options', 'graph_type_options', 'colon_4', 'line_dash_options', 'style_dict_back',
                 'days_ago_mode', 'line_dot_style_options', 'colon_1', 'target_value_header', 'dedication_mode',
                 'incoming_graph_type', 'start_date_button', 'chosen_colors', 'graph_format_button', 'line_dot_text',
                 'max_value_minutes', 'zero_type_header', 'end_date_button', 'nil_type_header', 'duration_mode',
                 'min_value_minutes', 'selected_option', 'max_value_options', 'graph_creator', 'min_value_seconds',
                 'min_value_options', 'first_increment_date', 'graph_format', 'days_ago_text', 'start_date',
                 'widgetName', 'master', 'tk', '_w', '_name', 'children', 'all_categories_time', 'style_dict',
                 'all_categories_increment', 'rolling_average_on', 'interval_label', 'rolling_average_interval')

    def __init__(self, all_categories_time: list, all_categories_increment: list, dedication_mode_file: str):
        if __name__ == "__main__":
            self.graph_creator = tk.Tk()
        else:
            self.graph_creator = tk.Toplevel()
            self.graph_creator.grab_set()
        tk.Frame.__init__(self)
        self.graph_creator.title("Graph Creation Options")
        self.graph_creator.resizable(False, False)

        self.place(relx=0.5, relwidth=1, anchor='n')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(5, weight=1)

        self.first_time_date = date.fromisoformat(self.get_start_date("Dedication Record.txt"))
        self.first_increment_date = date.fromisoformat(self.get_start_date("Dedication#Record.txt"))

        self.all_categories_time = tuple(all_categories_time)
        self.all_categories_increment = tuple(all_categories_increment)

        self.date_type = tk.StringVar()
        self.duration_mode = tk.StringVar(value='Days ago')
        self.dedication_mode_file = dedication_mode_file
        self.graph_type = tk.StringVar()
        if dedication_mode_file == "Dedication Record.txt":
            self.graph_type.set('Time')
            self.all_categories = self.all_categories_time
        else:
            self.graph_type.set('Increment')
            self.all_categories = self.all_categories_increment
        self.incoming_graph_type = tk.StringVar(value=self.graph_type.get())
        self.max_value_mode = tk.StringVar(value='Automatic')
        self.min_value_mode = tk.StringVar(value='Automatic')
        self.line_dot_style = tk.StringVar(value='Flat')
        self.line_style = tk.StringVar(value='solid')
        self.selected_option = tk.StringVar()
        self.chosen_color = '#f0f0f0'
        self.chosen_color_mode = tk.StringVar(value='Automatic')
        self.graph_format = tk.StringVar(value='Line')
        self.zero_type = tk.StringVar(value='Zero')
        self.nil_type = tk.StringVar(value='All')
        self.exclude_today = tk.BooleanVar(value=False)
        self.rolling_average_on = tk.BooleanVar(value=False)
        self.start_date_button = tk.Button(self.graph_creator, text="Set start date", state='disabled', takefocus=False,
                                           command=lambda: self.date_window('start'))
        self.start_date_button.grid(column=1, pady=(10, 0))
        self.start_date = tk.Entry(self.graph_creator, state='disabled', justify='center', width=10,
                                   font='arial 12')
        self.start_date.grid(row=1, column=1)
        self.end_date_button = tk.Button(self.graph_creator, text="Set end date", state='disabled', takefocus=False,
                                         command=lambda: self.date_window('end'))
        self.end_date_button.grid(row=0, column=2, pady=(10, 0), padx=(0, 50))
        self.end_date = tk.Entry(self.graph_creator, state='disabled', justify='center', width=10, font='arial 12')
        self.end_date.grid(row=1, column=2, padx=(0, 50))
        self.days_ago_text = tk.Label(self.graph_creator, text="Start how many days ago")
        self.days_ago_text.grid(row=0, column=3, pady=(10, 0), padx=(0, 130))
        self.days_ago_field = tk.Spinbox(self.graph_creator, from_=1, to=9999, width=4,
                                         font='arial 12', repeatinterval=2)
        self.days_ago_field.grid(row=1, column=3, padx=(0, 130), pady=(0, 10))
        self.days_ago_field.delete(0)
        self.days_ago_field.insert(0, 7)
        self.days_ago_field.config(state='readonly')
        tk.Checkbutton(self.graph_creator, text="Exclude current day", variable=self.exclude_today).grid(
            row=1, column=3, padx=(150, 0), pady=(28, 0))
        tk.Label(self.graph_creator, text='Duration setting').grid(row=0, column=3, pady=(10, 0), padx=(150, 0))
        self.days_ago_mode = tk.OptionMenu(self.graph_creator, self.duration_mode, 'Days ago', 'Date range', 'All',
                                           command=self.duration_mode_change)
        self.days_ago_mode.grid(row=1, column=3, padx=(150, 0), pady=(0, 20))
        self.days_ago_mode.config(width=10)

        tk.Label(self.graph_creator, text='Graph type').grid(row=2, column=1)
        self.graph_type_options = tk.OptionMenu(self.graph_creator, self.incoming_graph_type, 'Time', 'Increment',
                                                command=self.graph_type_switch)
        self.graph_type_options.grid(row=3, column=1)
        self.graph_type_options.config(width=9)

        tk.Label(self.graph_creator, text='Min value').grid(row=2, column=2)
        self.min_value_options = tk.OptionMenu(self.graph_creator, self.min_value_mode, 'Automatic', 'Manual',
                                               command=self.min_value_mode_toggle)
        self.min_value_options.grid(row=3, column=2)
        self.min_value_options.config(width=9)
        # Colons are defined first so that their backgrounds are layered under the spinboxes
        self.colon_1 = tk.Label(self.graph_creator, text=':', font=('arial bold', '12'))
        self.colon_2 = tk.Label(self.graph_creator, text=':', font=('arial bold', '12'))
        self.min_value_hours = tk.Spinbox(self.graph_creator, state='disabled', from_=0, to=23, repeatinterval=2,
                                          width=2, font='arial 12')
        self.min_value_minutes = tk.Spinbox(self.graph_creator, state='disabled', font='arial 12')
        self.min_value_minutes.grid(row=4, column=2)

        self.min_value_seconds = tk.Spinbox(self.graph_creator, state='disabled', from_=0, to=59, repeatinterval=2,
                                            width=2, font='arial 12')

        tk.Label(self.graph_creator, text='Max value').grid(row=2, column=3, padx=(0, 130))
        self.max_value_options = tk.OptionMenu(self.graph_creator, self.max_value_mode, 'Automatic', 'Manual',
                                               command=self.max_value_mode_toggle)
        self.max_value_options.grid(row=3, column=3, padx=(0, 130))
        self.max_value_options.config(width=9)
        self.colon_3 = tk.Label(self.graph_creator, text=':', font=('arial bold', '12'))
        self.colon_4 = tk.Label(self.graph_creator, text=':', font=('arial bold', '12'))
        self.max_value_hours = tk.Spinbox(self.graph_creator, state='disabled', from_=0, to=24, repeatinterval=2,
                                          width=2, font='arial 12')
        self.max_value_minutes = tk.Spinbox(self.graph_creator, state='disabled', font='arial 12')
        self.max_value_minutes.grid(row=4, column=3, padx=(0, 130))

        self.max_value_seconds = tk.Spinbox(self.graph_creator, state='disabled', from_=0, to=59, repeatinterval=2,
                                            width=2, font='arial 12')
        self.target_value_header = tk.Label(self.graph_creator)
        self.target_value_header.grid(row=2, column=3, padx=(150, 0))
        self.target_value_box = tk.Spinbox(self.graph_creator, width=4, font='arial 12', from_=0, to=24)
        self.target_value_box.grid(row=3, column=3, padx=(95, 0))
        self.target_value_box_two = tk.Spinbox(self.graph_creator, width=4, font='arial 12', from_=0, to=24)
        self.target_value_box_two.grid(row=3, column=3, padx=(205, 0))
        self.create_minmax_value_spinbox()

        self.zero_type_header = tk.Label(self.graph_creator, text='\nEmpty values are\ndisplayed as')
        self.zero_type_header.grid(row=0, column=4)
        self.zero_type_box = tk.OptionMenu(self.graph_creator, self.zero_type, 'Zero', 'Nil', command=self.nil_swap)
        self.zero_type_box.config(width=4)
        self.zero_type_box.grid(row=1, column=4, pady=(0, 18))
        self.nil_type_header = tk.Label(self.graph_creator, text='Nil value range', state='disabled')
        self.nil_type_header.grid(row=2, column=4)
        self.nil_type_box = tk.OptionMenu(self.graph_creator, self.nil_type, 'All', 'Left', 'Right', 'Min')
        self.nil_type_box.config(width=4, state='disabled')
        self.nil_type_box.grid(row=3, column=4)

        tk.Label(self.graph_creator, text='Add/remove graph categories').grid(row=4, column=1)
        tk.Label(self.graph_creator, text='_' * 39).grid(row=6, column=1, pady=(0, 124))
        self.saved_categories = tk.OptionMenu(self.graph_creator, self.selected_option, *self.all_categories)
        self.saved_categories.grid(row=5, column=1)
        self.saved_categories.config(width=24)
        self.add_category_button = tk.Button(self.graph_creator, text='Add', command=self.add_category, width=6)
        self.add_category_button.grid(row=6, column=1, padx=(0, 55), sticky='n')
        self.remove_category_button = tk.Button(self.graph_creator, text='Remove', command=self.remove_category)
        self.remove_category_button.grid(row=6, column=1, padx=(55, 0), sticky='n')

        tk.Label(self.graph_creator, text='Graph categories').grid(row=5, column=2)
        self.chosen_categories = tk.Listbox(self.graph_creator, width=24, height=12)
        self.chosen_categories.grid(row=6, column=2, stick='n', pady=(0, 10))

        tk.Label(self.graph_creator, text='Color').grid(row=5, column=3, padx=(0, 215))
        self.chosen_colors = tk.Listbox(self.graph_creator, width=8, height=12)
        self.chosen_colors.grid(row=6, column=3, sticky='n', padx=(0, 215))

        self.line_style_header = tk.Label(self.graph_creator, text='Line style')
        self.line_style_header.grid(row=5, column=3, padx=(0, 70))
        self.chosen_line_styles = tk.Listbox(self.graph_creator, width=14, height=12)
        self.chosen_line_styles.grid(row=6, column=3, sticky='n', padx=(0, 70))

        tk.Label(self.graph_creator, text='_' * 45).grid(row=5, column=3, columnspan=2, rowspan=2, sticky='e', pady=(0, 182))

        tk.Checkbutton(self.graph_creator, text='Plot rolling average', variable=self.rolling_average_on,
                       command=self.rolling_average_toggle).grid(row=4, column=3, padx=(140, 0), columnspan=2)
        self.interval_label = tk.Label(self.graph_creator, text="Rolling interval (days):", state='disabled')
        self.interval_label.grid(row=5, column=3, padx=(100, 0), columnspan=3)
        self.rolling_average_interval = tk.Spinbox(self.graph_creator, from_=0, to=9999, width=4, font='arial 11', repeatinterval=2)
        self.rolling_average_interval.grid(row=5, column=4)
        self.spin_entry_insert(self.rolling_average_interval, 'All', state='disabled')

        triple_scroll = tk.Scrollbar(self.graph_creator, command=self.triple_scroll)
        triple_scroll.grid(row=6, column=3, padx=(32, 0), sticky='ns', pady=(2, 10))
        self.chosen_categories.config(yscrollcommand=triple_scroll.set)
        self.chosen_colors.config(yscrollcommand=triple_scroll.set)
        self.chosen_line_styles.config(yscrollcommand=triple_scroll.set)

        tk.Label(self.graph_creator, text='Color select mode').grid(row=6, column=3, pady=(0, 175), padx=(160, 0))
        self.chosen_color_options = tk.OptionMenu(self.graph_creator, self.chosen_color_mode, 'Automatic', 'Manual',
                                                  command=lambda color_mode: self.color_chooser.config(state='disabled')
                                                  if color_mode == 'Automatic'
                                                  else self.color_chooser.config(state='normal'))
        self.chosen_color_options.grid(row=6, column=3, padx=(160, 0), pady=(0, 126))
        self.chosen_color_options.config(width=9)
        self.color_chooser = tk.Button(self.graph_creator, text='Choose color', state='disabled',
                                       command=self.choose_color)
        self.color_chooser.grid(row=6, column=3, padx=(160, 0), pady=(0, 60))
        self.color_overwrite = tk.Button(self.graph_creator, text='Overwrite selected\n color',
                                         command=lambda: self.overwrite_color_style('Color'))
        self.color_overwrite.grid(row=6, column=3, padx=(160, 0), pady=(35, 0))
        self.style_overwrite = tk.Button(self.graph_creator, text='Overwrite selected\n style',
                                         command=lambda: self.overwrite_color_style('Style'))
        self.style_overwrite.grid(row=6, column=3, padx=(160, 0), pady=(145, 0))

        tk.Label(self.graph_creator, text="Graph format").grid(row=6, column=4, pady=(0, 170))
        self.graph_format_button = tk.OptionMenu(self.graph_creator, self.graph_format, 'Line', 'Bar',
                                                 command=lambda graph_format: self.graph_format_toggle(graph_format))
        self.graph_format_button.grid(row=6, column=4, pady=(0, 120))
        self.graph_format_button.config(width=4)
        self.line_dot_text = tk.Label(self.graph_creator, text='Line dot style')
        self.line_dot_text.grid(row=6, column=4, pady=(0, 50))
        self.line_dot_style_options = tk.OptionMenu(self.graph_creator, self.line_dot_style, 'Flat', '.', '●', '◼', '◆',
                                                    '♦', '⬟', '⬢', '⬣', '⯃', '▲', '▼', '◀', '▶', '*', '+', '✚', 'x', 'X', '|', '_')
        self.style_dict = {'Flat': 'None', '●': 'o', '◼': 's', '◆': 'D', '♦': 'd', '⬟': 'p', '⬢': 'h', '⬣': 'H',
                           '⯃': '8', '▲': '^', '▼': 'v', '◀': '<', '▶': '>', '✚': 'P'}
        self.style_dict_back = {'None': 'Flat', 'o': '●', 's': '◼', 'D': '◆', 'd': '♦', '^': '▲', 'p': '⬟', 'h': '⬢',
                                'H': '⬣', '8': '⯃', 'v': '▼', '<': '◀', '>': '▶', 'P': '✚'}
        self.line_dot_style_options.grid(row=6, column=4)
        self.line_dash_text = tk.Label(self.graph_creator, text='Line style')
        self.line_dash_text.grid(row=6, column=4, pady=(60, 0))
        self.line_dash_options = tk.OptionMenu(self.graph_creator, self.line_style,
                                               'solid', 'dashed', 'dotted', 'dashdot', 'None')
        self.line_dash_options.config(width=7)
        self.line_dash_options.grid(row=6, column=4, pady=(110, 0), padx=10)

        tk.Label(self.graph_creator, text='Graph name').grid(row=6, column=1, pady=(0, 90))
        self.graph_name_entry = tk.Entry(self.graph_creator, width=32)
        self.graph_name_entry.grid(row=6, column=1, pady=(0, 50))
        self.save_options = tk.Button(self.graph_creator, text="Save current configuration to file",
                                      command=lambda: self.graph_prep('save'))
        self.save_options.grid(row=6, column=1, padx=10)
        self.load_options = tk.Button(self.graph_creator, text="Load configuration from file",
                                      command=self.graph_config_load, takefocus=False)
        self.load_options.grid(row=6, column=1, pady=(65, 0))
        self.create_button = tk.Button(self.graph_creator, text="Create graph", font='arial 12',
                                       command=lambda: self.graph_prep('create'), takefocus=False)
        self.create_button.grid(row=6, column=1, pady=(135, 0))

        self.graph_config_categories = (
            'Title', 'Start Date', 'End Date', 'Days Ago', 'Duration Setting',
            'Graph Type', 'Min Value Type', 'Min Value (Hours)', 'Min Value (Minutes)', 'Min Value (Seconds)',
            'Max Value Type', 'Max Value (Hours)', 'Max Value (Minutes)', 'Max Value (Seconds)', 'Line Styles',
            'Graph Format', 'Categories', 'Category Colors', 'Target Value 1', 'Target Value 2',
            'Empty Value Placeholder', 'Nil Type', 'Exclude Today', 'Plot Rolling Average', 'Rolling Average Interval')

        if (not exists('Graph Config.csv') or getsize('Graph Config.csv') == 0) and exists('Graph Config.csv.bak'):
            if tk.messagebox.askyesno('Empty data file',
                                      f'Saved graph configurations for Dedication Tracker are missing or corrupted.\n'
                                      'Would you like to restore from a backup?', icon='error'):
                util.restore_from_backup('Graph Config.csv')
        elif not exists("Graph Config.csv"):
            with open(r"Graph Config.csv", 'a') as csvfile:
                csv.writer(csvfile).writerow(self.graph_config_categories)

    @staticmethod
    def get_start_date(filename: str):
        with open(filename, 'r') as file:
            for _ in range(3):
                next(file)
            return file.readline()[:10]

    def triple_scroll(self, *args):
        self.chosen_categories.yview(*args)
        self.chosen_colors.yview(*args)
        self.chosen_line_styles.yview(*args)

    def create_minmax_value_spinbox(self):  # Also toggles target value box state
        if self.dedication_mode_file == "Dedication Record.txt":
            self.min_value_hours.grid(row=4, column=2, padx=(0, 86))
            self.colon_1.grid(row=4, column=2, padx=(0, 45))
            self.colon_2.grid(row=4, column=2, padx=(41, 0))
            self.min_value_seconds.grid(row=4, column=2, padx=(86, 0))
            self.max_value_hours.grid(row=4, column=3, padx=(0, 216))
            self.colon_3.grid(row=4, column=3, padx=(0, 175))
            self.colon_4.grid(row=4, column=3, padx=(0, 89))
            self.max_value_seconds.grid(row=4, column=3, padx=(0, 44))
            for minutes in (self.min_value_minutes, self.max_value_minutes):
                minutes.config(from_=0, to=59, width=2, repeatinterval=3)
            for target in (self.target_value_box, self.target_value_box_two):
                target.config(to=24, increment=0.1, repeatinterval=3)
            self.target_value_header.config(text="Target value(s) (hours)")
        else:
            for target in (self.min_value_hours, self.min_value_seconds, self.colon_1, self.colon_2,
                           self.max_value_hours, self.max_value_seconds, self.colon_3, self.colon_4):
                target.grid_forget()
            for minutes in (self.min_value_minutes, self.max_value_minutes):
                minutes.config(from_=0, to=9999, width=4, repeatinterval=2)
            for target in (self.target_value_box, self.target_value_box_two):
                target.config(to=9999, increment=1, repeatinterval=2)
            self.target_value_header.config(text="Target value(s)")
        self.spin_entry_insert(self.target_value_box, 0, True)
        self.spin_entry_insert(self.target_value_box_two, 0, True)

    @staticmethod
    def spin_entry_insert(box: tk.Spinbox | tk.Entry, entry: str, insert_none=False, state='readonly'):
        box.config(state='normal')
        box.delete(0, 'end')
        try:
            if float(entry) == 0 and insert_none:
                box.insert(0, 'None')
            else:
                box.insert(0, entry)
        except ValueError:
            box.insert(0, entry)
        box.config(state=state)

    def nil_swap(self, mode: str):
        if mode == 'Zero':
            self.state_toggle('disabled', self.nil_type_header, self.nil_type_box)
        else:
            self.state_toggle('normal', self.nil_type_header, self.nil_type_box)

    @staticmethod
    def state_toggle(state: str, *args):
        for target in args:
            target.config(state=state)

    def date_window(self, date_type: str):
        date_window = tk.Toplevel(self.graph_creator)
        date_window.resizable(False, False)
        date_window.title('Choose a date')
        date_window.grab_set()
        date_window.protocol('WM_DELETE_WINDOW', lambda: self._date_window_close(date_window))

        if date_type == 'start' and self.end_date.get() != '':
            maximum = date.fromisoformat(self.end_date.get())
        else:
            maximum = date.today()
        if date_type == 'start' or (date_type == 'end' and self.start_date.get() == ''):
            if self.dedication_mode_file == "Dedication Record.txt":
                minimum = self.first_time_date
            else:
                minimum = self.first_increment_date
        else:
            minimum = date.fromisoformat(self.start_date.get())
        if date_type == 'start':
            year = int(str(minimum)[:4])
            month = int(str(minimum)[5:7])
            day = int(str(minimum)[8:])
        else:
            year = int(str(maximum)[:4])
            month = int(str(maximum)[5:7])
            day = int(str(maximum)[8:])
        date_picker = Calendar(
                date_window, selectmode='day', mindate=minimum, maxdate=maximum, date_pattern='yyyy-mm-dd',
                font='arial 11', year=year, month=month, day=day, showweeknumbers=False, weekendbackground='#ffffff',
                othermonthwebackground='#ededed', disableddaybackground='#cccccc')
        date_picker.grid()
        tk.Button(date_window, text='Set', command=lambda: self._set_date(
            date_type=date_type, chosen_date=date_picker.get_date(), date_window=date_window)).grid(ipadx=20)

    def _set_date(self, date_type: str, chosen_date: str, date_window: tk.Toplevel):
        field = self.start_date if date_type == 'start' else self.end_date
        self.spin_entry_insert(field, chosen_date, False, 'disabled')
        self._date_window_close(date_window)

    def _date_window_close(self, date_window: tk.Toplevel):
        date_window.destroy()
        self.graph_creator.grab_set()

    def duration_mode_change(self, duration_mode: str):
        if duration_mode == 'Date range':
            self.state_toggle('disabled', self.days_ago_field, self.days_ago_text)
            self.state_toggle('normal', self.start_date_button, self.end_date_button)
        elif duration_mode == 'Days ago':
            self.days_ago_field.config(state='readonly')
            self.days_ago_text.config(state='normal')
            self.state_toggle('disabled', self.start_date_button, self.end_date_button)
        else:
            self.state_toggle('disabled', self.days_ago_field, self.days_ago_text,
                              self.start_date_button, self.end_date_button)

    def max_value_mode_toggle(self, max_mode: str):
        if max_mode == 'Automatic':
            self.state_toggle('disabled', self.max_value_hours, self.max_value_minutes, self.max_value_seconds)
        else:
            self.state_toggle('readonly', self.max_value_hours, self.max_value_minutes, self.max_value_seconds)

    def min_value_mode_toggle(self, min_mode: str):
        if min_mode == 'Automatic':
            self.state_toggle('disabled', self.min_value_hours, self.min_value_minutes, self.min_value_seconds)
        else:
            self.state_toggle('readonly', self.min_value_hours, self.min_value_minutes, self.min_value_seconds)

    def rolling_average_toggle(self):
        if self.rolling_average_on.get():
            self.interval_label.config(state='normal')
            self.rolling_average_interval.config(state='readonly')
        else:
            self.state_toggle('disabled', self.interval_label, self.rolling_average_interval)

    def add_category(self):
        if self.selected_option.get() not in self.chosen_categories.get(0, 'end') and self.selected_option.get() != '':
            self.chosen_categories.insert('end', self.selected_option.get())
            if self.chosen_color_mode.get() == 'Automatic':
                self.chosen_colors.insert('end', 'Auto')
            else:
                self.chosen_colors.insert('end', self.chosen_color)
            self.chosen_line_styles.insert(
                'end', f"{self.line_dot_style.get()} {self.line_style.get()}")

    @staticmethod
    def translate_style_name(dot: str, style_dict: dict) -> str:
        try:
            return style_dict[dot]
        except KeyError:
            pass
        return dot

    def remove_category(self, color=False):
        all_categories = self.chosen_categories.get(0, 'end')
        try:
            index = all_categories.index(self.selected_option.get())
        except ValueError:
            return
        self.chosen_colors.delete(index)
        if color:
            if self.chosen_color_mode.get() == 'Automatic':
                self.chosen_colors.insert(index, 'Auto')
            else:
                self.chosen_colors.insert(index, self.chosen_color)
        else:
            self.chosen_categories.delete(index)
            self.chosen_line_styles.delete(index)

    def choose_color(self):
        self.chosen_color = str(colorchooser.askcolor(color=self.chosen_color)[1])
        self.color_chooser.config(bg=self.chosen_color)

    def overwrite_color_style(self, field: str):
        if field == 'Color':
            target_listbox = self.chosen_colors
        else:
            target_listbox = self.chosen_line_styles
        try:
            target_num = target_listbox.curselection()[0]
        except (TypeError, tk.TclError, IndexError):
            return
        target_listbox.delete(target_num)
        if field == 'Color':
            if self.chosen_color_mode.get() == 'Automatic':
                self.chosen_colors.insert(target_num, 'Auto')
            else:
                self.chosen_colors.insert(target_num, self.chosen_color)
        else:
            self.chosen_line_styles.insert(
                target_num, f"{self.line_dot_style.get()} {self.line_style.get()}")

    def graph_type_switch(self, incoming_graph_type: str, skip_message=False):
        if incoming_graph_type == self.graph_type.get():
            return
        if self.chosen_categories.get(0):
            if skip_message and self.incoming_graph_type.get() == self.graph_type.get():
                return
            if not skip_message and not tk.messagebox.askyesno(
                    'mode reset', 'Changing graph types will reset selected categories. '
                                  'Are you sure you wish to proceed?', icon='warning'):
                    self.incoming_graph_type.set(self.graph_type.get())
                    return
            self.chosen_categories.delete(0, 'end')
            self.chosen_colors.delete(0, 'end')
            self.chosen_line_styles.delete(0, 'end')
        if incoming_graph_type == 'Time':
            self.dedication_mode_file = "Dedication Record.txt"
            self.all_categories = self.all_categories_time
        else:  # Interval
            self.dedication_mode_file = "Dedication#Record.txt"
            self.all_categories = self.all_categories_increment
        self.create_minmax_value_spinbox()
        self.graph_type.set(self.incoming_graph_type.get())
        self.selected_option.set('')
        self.saved_categories.destroy()
        self.saved_categories = tk.OptionMenu(self.graph_creator, self.selected_option, *self.all_categories)
        self.saved_categories.grid(row=5, column=1)
        self.saved_categories.config(width=24)

    def graph_format_toggle(self, graph_format: str):
        if graph_format == 'Line':
            self.state_toggle('normal', self.line_dot_text, self.line_dash_text, self.line_dot_style_options,
                              self.line_dash_options, self.line_style_header, self.zero_type_box, self.zero_type_header)
            self.nil_swap(self.zero_type.get())
        else:
            self.state_toggle('disabled', self.line_dot_text, self.line_dash_text, self.line_dot_style_options,
                              self.line_dash_options, self.line_style_header, self.zero_type_box, self.zero_type_header)
            self.nil_swap('Zero')

    def graph_prep(self, mode: str):
        """Prepares the configuration dictionary from all selected options for use in graph creation, or to save the
        configuration to a file. First performs error-checking."""
        if (overwrite_line := self.graph_error_check(mode, self.graph_name_entry.get().strip())) is True:
            overwrite_line = False
        elif not overwrite_line:
            return
        configuration = dict(zip(self.graph_config_categories, (
                self.graph_name_entry.get(), self.start_date.get(), self.end_date.get(), self.days_ago_field.get(),
                self.duration_mode.get(), self.graph_type.get(), self.min_value_mode.get(), self.min_value_hours.get(),
                self.min_value_minutes.get(), self.min_value_seconds.get(), self.max_value_mode.get(),
                self.max_value_hours.get(), self.max_value_minutes.get(), self.max_value_seconds.get(),
                [f"{self.translate_style_name(dot=line_style.split()[0], style_dict=self.style_dict)} {line_style.split()[1]}"
                    for line_style in self.chosen_line_styles.get(0, 'end')],  # Chosen line styles, dots translated
                self.graph_format.get(), self.chosen_categories.get(0, 'end'),
                self.chosen_colors.get(0, 'end'), self.target_value_box.get(), self.target_value_box_two.get(),
                self.zero_type.get(), self.nil_type.get(), self.exclude_today.get(), self.rolling_average_on.get(),
                self.rolling_average_interval.get())))
        if mode == 'save':
            self.graph_config_save(configuration=configuration, overwrite_line=overwrite_line)
        else:
            self.graph_create(configuration)

    def graph_config_save(self, configuration: dict, overwrite_line: int | bool):
        for category in ('Line Styles', 'Categories', 'Category Colors'):
            configuration[category] = '|'.join(configuration[category])
        try:
            if overwrite_line:
                util.prepare_backup("Graph Config.csv")  # does not use return value
                with open("Graph Config.csv", 'r', newline='') as csvfile:
                    new = [line for line in csv.reader(csvfile)]  # csv requires different method for usable file data
                new[overwrite_line] = configuration.values()
                with open(r"Graph Config.csv", 'w+', newline='') as csvfile:
                    csv.writer(csvfile).writerows(new)
            else:
                with open(r"Graph Config.csv", 'a', newline='') as csvfile:
                    csv.DictWriter(csvfile, fieldnames=self.graph_config_categories).writerow(configuration)
        except PermissionError:
            tl.messagebox.showerror('Access denied', 'The destination file could not be accessed. Make sure that '
                                                     'it is not open in another program.')
        tk.messagebox.showinfo('Configuration saved', 'Graph settings saved successfully.',
                               parent=self.graph_creator)

    def graph_error_check(self, mode: str, graph_name: str) -> bool | int:
        """Checks for potential errors or issues with selected graph options. Returns False if there is an error, or the
        user declined to continue after an issue. Returns True if there are no issues and a configuration in the file
        is not being overwritten. Returns an integer if there are no issues, and a line in the file corresponding to the
        integer is being overwritten."""
        if mode == 'save':  # Saving config to file
            if len(graph_name) > 40:
                if not tk.messagebox.askyesno('Excessive name length', 'Long config names may result in display issues.'
                                              ' Are you sure you wish to proceed?', icon='warning', parent=self.graph_creator):
                    return False
            if graph_name == '':
                tk.messagebox.showwarning('Empty name field', 'Graph name is required when saving '
                                                              'configuration to a file.', parent=self.graph_creator)
                return False
        if self.max_value_mode.get() == self.min_value_mode.get() != 'Automatic':
            if self.minmax_error_check():
                tk.messagebox.showwarning('Invalid value range',
                                          'Maximum graph value must be larger than minimum value.',
                                          parent=self.graph_creator)
                return False
        if len(self.chosen_categories.get(0, 1)) == 0:
            tk.messagebox.showwarning('Empty mode field', 'You must specify at least one mode to be graphed.',
                                      parent=self.graph_creator)
            return False
        if self.duration_mode.get() == 'Date range' and (
                len(self.start_date.get()) == 0 or len(self.end_date.get()) == 0):
            tk.messagebox.showwarning('Empty date field', 'When using a manual date range, both starting and ending'
                                                          ' date must be specified.', parent=self.graph_creator)
            return False
        if mode == 'save':
            try:
                with open(r"Graph Config.csv", 'r') as csvfile:
                    for line_num, line in enumerate(csv.DictReader(csvfile)):
                        if line['Title'] == graph_name:
                            if not tk.messagebox.askyesno(
                                   'Overwrite configuration', 'A saved configuration with the same name already exists.'
                                   ' Would you like to overwrite it?', icon='warning', parent=self.graph_creator):
                                return False
                            return int(line_num+1)
            except (KeyError, FileNotFoundError):
                self.backup_prompt()
                return False
        return True

    def minmax_error_check(self):
        minimum = int(self.min_value_minutes.get()) * 60
        maximum = int(self.max_value_minutes.get()) * 60
        if self.graph_type.get() == "Time":
            minimum += (int(self.min_value_hours.get()) * 3600) + int(self.min_value_seconds.get())
            maximum += (int(self.max_value_hours.get()) * 3600) + int(self.max_value_seconds.get())
        if minimum >= maximum:
            return True

    def backup_prompt(self) -> bool | None:
        if exists("Graph Config.csv.bak") and tk.messagebox.askyesno(
                'Saved settings not found', 'No saved settings could be found. It is possible that they are either '
                                            'missing or corrupted. Would you like to restore from a backup?',
                parent=self.graph_creator, icon='error'):
            util.restore_from_backup("Graph Config.csv")
            return True

    def graph_config_load(self):
        try:
            with open(r"Graph Config.csv", 'r') as csvfile:
                saved_settings = [config['Title'] for config in csv.DictReader(csvfile)]
        except (KeyError, FileNotFoundError):
            saved_settings = False
        if not saved_settings:
            if not self.backup_prompt():
                tk.messagebox.showwarning('No saved settings', 'No settings to load', parent=self.graph_creator)
        else:
            self.graph_config_load_window(saved=tuple(saved_settings))

    def graph_config_load_window(self, saved: tuple):
        config_load_window = tk.Toplevel(self.graph_creator)
        config_load_window.title("Select a graph configuration to load")
        config_load_window.resizable(False, False)
        config_load_window.grab_set()
        config_load_window.protocol('WM_DELETE_WINDOW', lambda: self._config_load_close(config_load_window))
        scroll = tk.Scrollbar(config_load_window)
        scroll.grid(column=1, sticky='ns')
        load_list = tk.Listbox(config_load_window, font='courier 12', width=40, height=20, yscrollcommand=scroll.set)
        load_list.grid(row=0)
        scroll.config(command=load_list.yview)

        for item in saved:
            load_list.insert('end', item)
        tk.Button(config_load_window, text='Direct graph',
                  command=lambda: self.select_load(window=config_load_window, load_list=load_list,
                                                   direct=True)).grid(row=1, padx=(0, 200))
        tk.Button(config_load_window, text='Select', command=lambda: self.select_load(
            window=config_load_window, load_list=load_list)).grid(row=1)
        tk.Button(config_load_window, text='Delete', command=lambda: util.select_delete(load_list, "Graph Config.txt")
                  ).grid(row=1, padx=(170, 0))

    def select_load(self, window: tk.Toplevel, load_list: tk.Listbox, direct=False):
        try:
            target, target_num = load_list.get(load_list.curselection()[0]), load_list.curselection()[0]
        except (TypeError, tk.TclError, IndexError):
            return
        load = False
        with open("Graph Config.csv", 'r') as csvfile:
            for line in csv.DictReader(csvfile):
                if line['Title'] == target:
                    load = line
        if load and not direct:
            self.full_select_load(window=window, settings=load, target=target)
        elif direct:
            for category in ('Line Styles', 'Categories', 'Category Colors'):
                load[category] = load[category].split('|')
            self.graph_create(load)

    def full_select_load(self, window: tk.Toplevel, settings: dict, target: str):
        self.graph_name_entry.delete(0, 'end')
        self.graph_name_entry.insert(0, settings['Title'])
        self.spin_entry_insert(self.start_date, settings['Start Date'], False, 'disabled')
        self.spin_entry_insert(self.end_date, settings['End Date'], False, 'disabled')
        self.spin_entry_insert(self.days_ago_field, settings['Days Ago'])
        self.duration_mode.set(settings['Duration Setting'])
        self.duration_mode_change(self.duration_mode.get())

        self.incoming_graph_type.set(settings['Graph Type'])
        self.graph_type_switch(settings['Graph Type'], True)
        self.min_value_mode.set(settings['Min Value Type'])
        if self.min_value_mode.get() != 'Automatic':
            self.spin_entry_insert(self.min_value_minutes, settings['Min Value (Minutes)'])
            if self.graph_type.get() == 'Time':
                self.spin_entry_insert(self.min_value_hours, settings['Min Value (Hours)'])
                self.spin_entry_insert(self.min_value_seconds, settings['Min Value (Seconds)'])
        self.min_value_mode_toggle(settings['Min Value Type'])

        self.max_value_mode.set(settings['Max Value Type'])
        if self.max_value_mode.get() != 'Automatic':
            self.spin_entry_insert(self.max_value_minutes, settings['Max Value (Minutes)'])
            if self.graph_type.get() == 'Time':
                self.spin_entry_insert(self.max_value_hours, settings['Max Value (Hours)'])
                self.spin_entry_insert(self.max_value_seconds, settings['Max Value (Seconds)'])
        self.max_value_mode_toggle(settings['Max Value Type'])

        self.chosen_line_styles.delete(0, 'end')
        for mode in settings['Line Styles'].split('|'):
            self.chosen_line_styles.insert(
                'end', f"{self.translate_style_name(dot=mode.split()[0], style_dict=self.style_dict_back)} "
                       f"{mode.split()[1]}")  # Translates style dots back (special characters fail to save in file)
        self.graph_format.set(settings['Graph Format'])
        self.graph_format_toggle(settings['Graph Format'])

        self.chosen_categories.delete(0, 'end')
        for mode in settings['Categories'].split('|'):
            self.chosen_categories.insert('end', mode)

        self.chosen_colors.delete(0, 'end')
        for color in settings['Category Colors'].split('|'):
            self.chosen_colors.insert('end', color)
        if settings['Target Value 1'] == '': settings['Target Value 1'] = 'None'
        if settings['Target Value 2'] == '': settings['Target Value 2'] = 'None'

        self.spin_entry_insert(self.target_value_box, settings['Target Value 1'], True)
        self.spin_entry_insert(self.target_value_box_two, settings['Target Value 2'], True)

        self.zero_type.set(settings['Empty Value Placeholder'])
        self.nil_swap(settings['Empty Value Placeholder'])
        if settings['Nil Type'] == '':
            settings['Nil Type'] = 'All'
        self.nil_type.set(settings['Nil Type'])

        self.exclude_today.set(settings['Exclude Today'])

        self.rolling_average_on.set(settings['Plot Rolling Average'])
        if self.rolling_average_on.get():
            if settings['Rolling Average Interval'] == 0:
                settings['Rolling Average Interval'] = 'All'
            self.spin_entry_insert(self.rolling_average_interval, settings['Rolling Average Interval'])
        else:
            self.spin_entry_insert(self.rolling_average_interval, entry='All', state='disabled')
        tk.messagebox.showinfo('Load complete', f"{target} settings loaded successfully.")
        self._config_load_close(window)

    def _config_load_close(self, window: tk.Toplevel):
        window.destroy()
        self.graph_creator.grab_set()

    def graph_create(self, config: dict):
        """{'Title': self.graph_name_entry.get(),
         'Start date': self.start_date.get(),
         'End date': self.end_date.get(),
         'Days ago': self.days_ago_field.get(),
         'Duration setting': self.duration_mode.get(),
         'Graph type': self.graph_type.get(),
         'Min value type': self.min_value_mode.get(),
         'Min value (hours)': self.min_value_hours.get(),
         'Min value minutes': self.min_value_minutes.get(),
         'Min value (seconds)': self.min_value_seconds.get(),
         'Max value type': self.max_value_mode.get(),
         'Max value (hours)': self.max_value_hours.get(),
         'Max value (minutes)': self.max_value_minutes.get(),
         'Max value (seconds)': self.max_value_seconds.get(),
         'Line styles': self.chosen_line_styles.get(0, 'end'),
         'Graph format': self.graph_format.get(),
         'Categories': self.chosen_categories.get(0, 'end'),
         'Category colors': self.chosen_colors.get(0, 'end'),
         'Target value 1': self.target_value_box.get(),
         'Target value 2': self.target_value_box_two.get(),
         'Empty value placeholder': self.zero_type.get(),
         'Nil type': self.nil_type.get(),
         'Exclude today': self.exclude_today.get(),
         'Plot rolling average': self.rolling_average_on.get(),
         'Rolling average interval': self.rolling_average_interval.get()}"""
        import matplotlib.pyplot as plt
        plt.title(config['Title'])
        miny = 0
        maxy = None
        exclude_today = ''
        if config['Graph Type'] == 'Time':
            filename = "Dedication Record.txt"
            plt.ylabel('Time (hours)')
            if config['Min Value Type'] != 'Automatic':
                miny = int(config['Min Value (Hours)']) + (int(config['Min Value (Minutes)']) / 60
                                                           ) + (int(config['Min Value (Seconds)']) / 3600)
            if config['Max Value Type'] != 'Automatic':
                maxy = int(config['Max Value (Hours)']) + (int(config['Max Value (Minutes)']) / 60
                                                           ) + (int(config['Max Value (Seconds)']) / 3600)
        else:  # Increment
            filename = "Dedication#Record.txt"
            if config['Min Value Type'] != 'Automatic':
                miny = int(config['Min Value (Minutes)'])
            if config['Max Value Type'] != 'Automatic':
                maxy = int(config['Max Value (Minutes)'])
        plt.ylim(miny, maxy)
        contents = util.prepare_backup(filename)
        if config['Duration Setting'] == 'Days ago':
            if int(config['Days Ago']) >= len(contents) - 2:
                plot_dates = contents[3:]
            else:
                plot_dates = contents[-int(config['Days Ago']):]
        elif config['Duration Setting'] == 'Date range':
            for target_date in enumerate(contents[3:]):
                if target_date[1].split(' ')[0] == config['Start Date']:
                    date_one = target_date[0]
                if target_date[1].split(' ')[0] == config['End Date']:
                    date_two = target_date[0]
            try:
                plot_dates = contents[date_one + 3:date_two + 4]
            except UnboundLocalError:
                tk.messagebox.showerror('Error reading dates',
                                        'The selected date range could not be read from the file.')
                return None
        else:
            plot_dates = contents[3:]
        del contents

        # Setting x-axis labels
        if config['Exclude Today'] is True and plot_dates[-1][0:10] == str(date.today()):
            del plot_dates[-1]
            exclude_today = " (Today excluded)"

        if config['Graph Format'] == 'Line':
            plt.xlabel(f'Date')
            short_dates = [full_date[5:10] for full_date in plot_dates]
            dots = []
            styles = []
            for entry in config['Line Styles']:
                dots.append(entry.split(' ')[0])
                styles.append(entry.split(' ')[1])
        else:
            bar_locations = []
            bar_labels = []
            if config['Duration Setting'] == 'Days ago':
                s = '' if len(plot_dates) == 1 else 's'
                plt.xlabel(f'Previous {len(plot_dates)} day{s}')
            elif config['Duration Setting'] == 'Date range':
                plt.xlabel(f"{config['Start Date']} to {config['End Date']}{exclude_today}")
            else:
                plt.xlabel(f"All recorded dates{exclude_today}")

        plot_points = []
        bar_max = []
        for index, category in enumerate(config['Categories']):
            plot_points.append(self.get_data_points(
                category=category, dataset=plot_dates, graph_type=config['Graph Type'],
                zero_type=config['Empty Value Placeholder'], graph_format=config['Graph Format']))
            if config['Graph Format'] == 'Line':
                if config['Category Colors'][index] == 'Auto':
                    plt.plot(short_dates, plot_points[index], marker=dots[index],
                             linestyle=styles[index], label=category)
                else:
                    plt.plot(short_dates, plot_points[index], color=config['Category Colors'][index],
                             marker=dots[index], linestyle=styles[index], label=category)
            else:
                if config['Category Colors'][index] == 'Auto':
                    plt.bar(int(index), height=sum(plot_points[index]), label=category)
                else:
                    plt.bar(int(index), height=sum(plot_points[index]),
                            color=config[17][index], label=category)
                bar_max.append(sum(plot_points[index]))
                bar_locations.append(int(index))
                bar_labels.append(category)

        # Setting X and Y limits (automatic)
        if config['Max Value Type'] == 'Automatic':
            if bar_max:
                maxy = max(bar_max)
            else:
                try:
                    maxy = max([item for group in plot_points for item in group if item is not None])
                except (TypeError, ValueError):
                    pass
            if config['Target Value 1'] not in ('None', '') and float(config['Target Value 1']) > maxy:
                maxy = float(config['Target Value 1']) + 0.5
            if maxy == 0:
                maxy = 1
            plt.ylim(miny, maxy)

        second = 'Target'
        if config['Target Value 1'] not in ('None', '') and float(config['Target Value 1']) > 0:
            plt.axhline(y=float(config['Target Value 1']), color='black', label='Target')
            second = None
        if config['Target Value 2'] not in ('None', '') and float(config['Target Value 2']) > 0:
            plt.axhline(y=float(config['Target Value 2']), color='black', label=second)
        if config['Graph Format'] == 'Bar':
            plt.xticks(ticks=bar_locations, labels=bar_labels)
        else:  # Line
            if config['Empty Value Placeholder'] == 'Nil' and config['Nil Type'] != 'Min':
                start = end = None
                if (config['Nil Type'] == 'All' or config['Nil Type'] == 'Left'
                  ) and any(plot[0] is None for plot in plot_points):
                    start = 0
                if (config['Nil Type'] == 'All' or config['Nil Type'] == 'Right'
                  ) and any(plot[-1] is None for plot in plot_points):
                    end = 0
                if start is not None or end is not None:  # Extends Nil graph range
                    invisible_graph_extender = [None for _ in short_dates]
                    invisible_graph_extender[0] = start
                    invisible_graph_extender[-1] = end
                    plt.plot(short_dates, invisible_graph_extender, linestyle='None')
            if config['Plot Rolling Average'] is True and config['Rolling Average Interval'] != 1:
                from statistics import mean
                if config['Rolling Average Interval'] in ('0', 'All'):
                    plt.plot(short_dates, [mean(plot_points[0][:index+1]) for index in range(len(plot_points[0]))],
                             label=f"Rolling average ({config['Categories'][0]})", color='#444444')
                else:
                    chunk_size = int(config['Rolling Average Interval'])
                    try:
                        plt.plot(short_dates[:chunk_size], [mean(plot_points[0][chunk_size:chunk_size + index + 1])
                                                            for index in range(chunk_size)],
                                 label=f"Rolling average ({config['Categories'][0]})", color='#444444')
                    except TypeError:
                        pass
                    for chunk_num in range(int(len(short_dates)/chunk_size))[1:]:
                        try:
                            plt.plot(short_dates[chunk_num*chunk_size:(chunk_num*chunk_size)+chunk_size],
                                     [mean(plot_points[0][chunk_num*chunk_size:(chunk_num*chunk_size) + index + 1])
                                      for index in range(chunk_size)], color='#444444')
                        except TypeError:
                            break

            plt.legend()
            if config['Graph Type'] == 'Time':
                font_size = int(10 - (len(short_dates)) / 40)
                if font_size < 1:
                    font_size = 1
                plt.xticks(rotation=45, ha='right', fontsize=font_size)
        plt.show()

    @staticmethod
    def get_data_points(category: str, dataset: list, graph_type: str, zero_type: str, graph_format: str) -> list:
        """Takes category, dataset (plot_dates (lines from file containing dates to be plotted)),
        graph_type (Time or Increment), zero_type (Zero or Nil) and graph_format (Line or Bar) and processes the
        dataset to return the time/increment values for each date in a list that can be used by pyplot"""
        category_plot_points = []
        for data_set in dataset:
            for num, data_point in enumerate(data_set.split()):
                if ' ' in category:  # Check if spaced name
                    if index := util.verify_spaced_name(category_list=data_set.split(), category=category):
                        if graph_type == 'Time':
                            category_plot_points.append(get_time_from_data(data_set.split()[index+2]))
                        else:
                            category_plot_points.append(float(data_set.split(' ')[index + 2]))
                        break
                elif data_point == category:
                    if graph_type == 'Time':
                        category_plot_points.append(get_time_from_data(data=data_set.split()[num + 2]))
                    else:
                        category_plot_points.append(float(data_set.split()[num + 2]))
                    break
            else:
                if zero_type == 'Zero' or graph_format == 'Bar':
                    category_plot_points.append(0)
                else:
                    category_plot_points.append(None)
        return category_plot_points


def get_time_from_data(data: str) -> float:
    return float(int(data.split(':')[0]) + (int(data.split(':')[1]) / 60) + (int(data.split(':')[2]) / 3600))


def get_dedication_mode_file() -> str:
    current_date = str(date.today())
    util.ensure_data_file_existence(current_date, "Dedication Record.txt")
    util.ensure_data_file_existence(current_date, "Dedication#Record.txt")
    with open(r"Dedication Record.txt", 'r') as file:
        dedication_mode_file = file.readline()[0:21]
    return dedication_mode_file


if __name__ == "__main__":
    GraphCreator(dedication_mode_file=get_dedication_mode_file(),
                 all_categories_time=util.get_categories_from_file(filename="Dedication Record.txt"),
                 all_categories_increment=util.get_categories_from_file(filename="Dedication#Record.txt")).mainloop()

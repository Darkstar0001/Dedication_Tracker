import tkinter as tk
from tkinter import messagebox, colorchooser
from datetime import datetime, date
from tkcalendar.calendar_ import Calendar
from os.path import exists
from math import log
import dedicationsharedfunctions as util
# matplotlib is imported within the graph class's graphing function, to improve program startup speed


class GraphCreator(tk.Frame):
    __slots__ = ('line_dash_text', 'line_style', 'nil_type', 'date_type', 'color_chooser', 'remove_category_button',
                 'graph_type', 'zero_type', 'create_button', 'nil_type_box', 'zero_type_box', 'chosen_color_mode',
                 'end_date', 'min_value_mode', 'min_value_hours', 'line_style_header', 'max_value_hours',
                 'target_value_box', 'max_value_seconds', 'max_value_mode', 'date_win', 'data_store',
                 'style_overwrite', 'exclude_today', 'graph_name_entry', 'chosen_categories',
                 'chosen_line_styles', 'target_value_box_two', 'all_categories', 'colon_3', 'color_overwrite',
                 'first_time_date', 'save_options', 'line_dot_style', 'days_ago_field', 'chosen_color',
                 'saved_categories', 'colon_2', 'add_category_button', 'load_options', 'dedication_mode_file',
                 'chosen_color_options', 'graph_type_options', 'colon_4', 'line_dash_options',
                 'days_ago_mode', 'line_dot_style_options', 'colon_1', 'target_value_header', 'dedication_mode',
                 'incoming_graph_type', 'start_date_button', 'chosen_colors', 'graph_format_button', 'line_dot_text',
                 'max_value_minutes', 'zero_type_header', 'end_date_button', 'nil_type_header', 'duration_mode',
                 'min_value_minutes', 'selected_option', 'max_value_options', 'graph_creator', 'min_value_seconds',
                 'min_value_options', 'first_increment_date', 'graph_format', 'days_ago_text', 'start_date',
                 'widgetName', 'master', 'tk', '_w', '_name', 'children', 'all_categories_time',
                 'all_categories_increment', 'rolling_average_on', 'interval_label', 'rolling_average_interval')

    def __init__(self, all_categories_time: list, all_categories_increment: list, dedication_mode_file: str):
        self.graph_creator = tk.Toplevel()
        tk.Frame.__init__(self)
        self.graph_creator.title("Graph Creation Options")
        self.graph_creator.resizable(False, False)

        self.place(relx=0.5, relwidth=1, anchor='n')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(5, weight=1)
        self.graph_creator.grab_set()

        if not exists("Graph Config.txt"):
            with open(r"Graph Config.txt", 'a') as file:
                file.write("Modifying this file directly may render it unreadable to the program.\n")

        self.first_time_date = date(*self.get_start_date("Dedication Record.txt"))
        self.first_increment_date = date(*self.get_start_date("Dedication#Record.txt"))

        self.all_categories_time = tuple(all_categories_time)
        self.all_categories_increment = tuple(all_categories_increment)

        self.data_store = tk.StringVar()
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
        self.line_dot_style_options = tk.OptionMenu(self.graph_creator, self.line_dot_style, 'Flat', '.',
                                                    'o', 'Square', 'Triangle', '*', '+', 'x', 'X', '|', '_')
        self.line_dot_style_options.grid(row=6, column=4)
        self.line_dash_text = tk.Label(self.graph_creator, text='Line style')
        self.line_dash_text.grid(row=6, column=4, pady=(60, 0))
        self.line_dash_options = tk.OptionMenu(self.graph_creator, self.line_style, 'solid', 'dashed', 'dotted', 'dashdot', 'None')
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

    @staticmethod
    def get_start_date(filename):
        with open(filename, 'r') as file:
            for _ in range(3):
                next(file)
            return [int(x) for x in file.readline()[:10].split('-')]

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
    def spin_entry_insert(box, entry: str, insert_none=False, state='readonly'):
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
        date_window.protocol('WM_DELETE_WINDOW', lambda: self.__date_window_close(date_window))

        if date_type == 'start' and self.end_date.get() != '':
            a, b, c = self.end_date.get().split('-')
            maximum = date(int(a), int(b), int(c))
        else:
            maximum = datetime.now()
        if date_type == 'start' or (date_type == 'end' and self.start_date.get() == ''):
            if self.dedication_mode_file == "Dedication Record.txt":
                minimum = self.first_time_date
            else:
                minimum = self.first_increment_date
        else:
            a, b, c = self.start_date.get().split('-')
            minimum = date(int(a), int(b), int(c))
        date_picker = Calendar(date_window, selectmode='day', mindate=minimum, maxdate=maximum,
                               date_pattern='yyyy-mm-dd')
        date_picker.grid()
        tk.Button(date_window, text='Set', command=lambda: self.__set_date(date_type, date_picker.get_date(),
                                                                           date_window)).grid(ipadx=20)

    def __set_date(self, date_type: str, chosen_date, date_window):
        field = self.start_date if date_type == 'start' else self.end_date
        self.spin_entry_insert(field, chosen_date, False, 'disabled')
        if date_window:
            self.__date_window_close(date_window)

    def __date_window_close(self, date_window):
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
        all_cats = self.chosen_categories.get(0, 'end')
        if self.selected_option.get() not in all_cats and self.selected_option.get() != '':
            self.chosen_categories.insert('end', self.selected_option.get())
            if self.chosen_color_mode.get() == 'Automatic':
                self.chosen_colors.insert('end', 'Auto')
            else:
                self.chosen_colors.insert('end', self.chosen_color)
            self.chosen_line_styles.insert('end',
                                           f"{self.translate_style_name(self.line_dot_style.get())} {self.line_style.get()}")

    @staticmethod
    def translate_style_name(dot):
        if dot == 'Flat':
            return 'None'
        elif dot == 'Square':
            return 's'
        elif dot == 'Triangle':
            return '^'
        else:
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
            return None
        target_listbox.delete(target_num)
        if field == 'Color':
            if self.chosen_color_mode.get() == 'Automatic':
                self.chosen_colors.insert(target_num, 'Auto')
            else:
                self.chosen_colors.insert(target_num, self.chosen_color)
        else:
            self.chosen_line_styles.insert(target_num,
                                           f"{self.translate_style_name(self.line_dot_style.get())} {self.line_style.get()}")

    def graph_type_switch(self, incoming_graph_type: str, skip_message=False):
        if incoming_graph_type != self.graph_type.get():
            if self.chosen_categories.get(0):
                if not skip_message:
                    if not tk.messagebox.askyesno('mode reset', 'Changing graph types will reset selected'
                                                  ' categories. Are you sure you wish to proceed?', icon='warning'):
                        self.incoming_graph_type.set(self.graph_type.get())
                        return None
                self.chosen_categories.delete(0, 'end')
                self.chosen_colors.delete(0, 'end')
                self.chosen_line_styles.delete(0, 'end')
                if skip_message and self.incoming_graph_type.get() == self.graph_type.get():
                    return None
            if incoming_graph_type == 'Time':
                self.dedication_mode_file = "Dedication Record.txt"
                self.all_categories = self.all_categories_time
            else:
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
        if (overwrite_line := self.graph_error_check(mode, self.graph_name_entry.get().strip())) is True:
            overwrite_line = False
        elif not overwrite_line:
            return

        one = two = three = ''
        if self.duration_mode.get() == 'Date range':
            one = self.start_date.get()
            two = self.end_date.get()
        elif self.duration_mode.get() == 'Days ago':
            three = self.days_ago_field.get()
        configuration = [self.graph_name_entry.get().strip(), one, two, three, self.duration_mode.get(),
                         self.graph_type.get(), self.min_value_mode.get()]

        one = three = ''
        if self.min_value_mode.get() != 'Automatic':
            one = self.min_value_hours.get()
            three = self.min_value_seconds.get()
        two = self.min_value_minutes.get()
        configuration.extend([one, two, three, self.max_value_mode.get()])

        one = three = ''
        two = self.max_value_minutes.get()
        if self.max_value_mode.get() != 'Automatic':
            one = self.max_value_hours.get()
            three = self.max_value_seconds.get()
        graph_line_styles = self.chosen_line_styles.get(0, 'end')
        configuration.extend([one, two, three, ':'.join(graph_line_styles), self.graph_format.get()])

        graph_categories = self.chosen_categories.get(0, 'end')
        graph_colors = self.chosen_colors.get(0, 'end')
        target_one = target_two = nil = ''
        if self.target_value_box.get() != 0 and self.target_value_box.get() != 'None':
            target_one = self.target_value_box.get()
        if self.target_value_box_two.get() != 0 and self.target_value_box_two.get() != 'None':
            target_two = self.target_value_box_two.get()
        if self.zero_type.get() == 'Nil':
            nil = self.nil_type.get()

        to_write = f"{'|'.join(configuration)}|{':'.join(graph_categories)}|{':'.join(graph_colors)}|{target_one}|" \
                   f"{target_two}|{self.zero_type.get()}|{nil}|{self.exclude_today.get()}|{self.rolling_average_on.get()}"\
                   f"{self.rolling_average_interval.get()}|\n"
        if mode == 'save':
            if overwrite_line > 0:
                new = util.prepare_backup("Graph Config.txt")
                new[overwrite_line] = to_write
                with open(r"Graph Config.txt", 'w') as file:
                    file.write(''.join(new))
            else:
                with open(r"Graph Config.txt", 'a') as file:
                    file.write(to_write)
            tk.messagebox.showinfo('Configuration saved', 'Graph settings saved successfully.',
                                   parent=self.graph_creator)
        else:
            configuration.extend([graph_categories, graph_colors, self.target_value_box.get(),
                                  self.target_value_box_two.get(), self.zero_type.get(), self.nil_type.get(),
                                  self.exclude_today.get(), self.rolling_average_on.get(), self.rolling_average_interval.get()])
            self.graph_create(configuration)

    def graph_error_check(self, mode: str, graph_name: str):
        if len(graph_name) > 40 and mode == 'save':
            if not tk.messagebox.askyesno('Excessive name length', 'Long config names may result in display issues. Are'
                                                                   ' you sure you wish to proceed?', icon='warning',
                                          parent=self.graph_creator):
                return False
        if mode == 'save' and graph_name == '':
            tk.messagebox.showwarning('Empty name field', 'Graph name is required when saving configuration to a file.',
                                      parent=self.graph_creator)
            return False
        if mode == 'save' and '|' in graph_name:
            tk.messagebox.showwarning('Invalid name', 'Saved graph configuration names may not include the | character.',
                                      parent=self.graph_creator)
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
            with open(r"Graph Config.txt", 'r') as file:
                for line_num, line in enumerate(file):
                    if line.split('|')[0] == graph_name:
                        if not tk.messagebox.askyesno('Overwrite configuration', 'A saved configuration with the same'
                                                      ' name already exists. Would you like to overwrite it?',
                                                      icon='warning', parent=self.graph_creator):
                            return False
                        return int(line_num)
        return True

    def minmax_error_check(self):
        minimum = int(self.min_value_minutes.get()) * 60
        maximum = int(self.max_value_minutes.get()) * 60
        if self.graph_type.get() == "Time":
            minimum += (int(self.min_value_hours.get()) * 3600) + int(self.min_value_seconds.get())
            maximum += (int(self.max_value_hours.get()) * 3600) + int(self.max_value_seconds.get())
        if minimum >= maximum:
            return True

    def graph_config_load(self):
        with open(r"Graph Config.txt", 'r') as file:
            next(file)
            saved_settings = [line.split('|')[0] for line in file]
        if len(saved_settings) == 0:
            tk.messagebox.showwarning('No saved settings', 'No settings to load', parent=self.graph_creator)
            return None
        else:
            self.graph_config_load_window(saved_settings)

    def graph_config_load_window(self, saved):
        config_load_window = tk.Toplevel(self.graph_creator)
        config_load_window.title("Select a graph configuration to load")
        config_load_window.resizable(False, False)
        config_load_window.grab_set()
        config_load_window.protocol('WM_DELETE_WINDOW', lambda: self.__config_load_close(config_load_window))
        scroll = tk.Scrollbar(config_load_window)
        scroll.grid(column=1, sticky='ns')
        load_list = tk.Listbox(config_load_window, font='courier 12', width=40, height=20, yscrollcommand=scroll.set)
        load_list.grid(row=0)
        scroll.config(command=load_list.yview)

        for item in saved:
            load_list.insert('end', item)
        tk.Button(config_load_window, text='Direct graph',
                  command=lambda: self.select_load(config_load_window, load_list, True)).grid(row=1, padx=(0, 200))
        tk.Button(config_load_window, text='Select',
                  command=lambda: self.select_load(config_load_window, load_list)).grid(row=1)
        tk.Button(config_load_window, text='Delete', command=lambda: util.select_delete(load_list, "Graph Config.txt"
                                                                                   )).grid(row=1, padx=(170, 0))

    def select_load(self, window, load_list, direct=False):
        try:
            target, target_num = load_list.get(load_list.curselection()[0]), load_list.curselection()[0]
        except (TypeError, tk.TclError, IndexError):
            return
        load = False
        with open("Graph Config.txt", 'r') as file:
            for line in file:
                if line.split('|')[0] == target:
                    load = line.split('|')
        if load and not direct:  # Closes the file before performing the load or graph creation
            self.full_select_load(window, load, target)
        elif direct:
            load[16] = load[16].split(':')
            load[17] = load[17].split(':')
            self.graph_create(load)

    def full_select_load(self, window, settings, target):
        self.graph_name_entry.delete(0, 'end')
        self.graph_name_entry.insert(0, settings[0])
        self.__set_date('start', settings[1], None)
        self.__set_date('end', settings[2], None)
        self.spin_entry_insert(self.days_ago_field, settings[3])
        self.duration_mode.set(settings[4])
        self.duration_mode_change(self.duration_mode.get())

        self.incoming_graph_type.set(settings[5])
        self.graph_type_switch(settings[5], True)
        self.min_value_mode.set(settings[6])
        if self.min_value_mode.get() != 'Automatic':
            self.spin_entry_insert(self.min_value_minutes, settings[8])
            if self.graph_type.get() == 'Time':
                self.spin_entry_insert(self.min_value_hours, settings[7])
                self.spin_entry_insert(self.min_value_seconds, settings[9])
        self.min_value_mode_toggle(settings[6])

        self.max_value_mode.set(settings[10])
        if self.max_value_mode.get() != 'Automatic':
            self.spin_entry_insert(self.max_value_minutes, settings[12])
            if self.graph_type.get() == 'Time':
                self.spin_entry_insert(self.max_value_hours, settings[11])
                self.spin_entry_insert(self.max_value_seconds, settings[13])
        self.max_value_mode_toggle(settings[10])

        self.chosen_line_styles.delete(0, 'end')
        for mode in settings[14].split(':'):
            self.chosen_line_styles.insert('end', mode)
        self.graph_format.set(settings[15])
        self.graph_format_toggle(settings[15])

        self.chosen_categories.delete(0, 'end')
        for mode in settings[16].split(':'):
            self.chosen_categories.insert('end', mode)

        self.chosen_colors.delete(0, 'end')
        for color in settings[17].split(':'):
            self.chosen_colors.insert('end', color)
            if settings[18] == '': settings[18] = 'None'
            if settings[19] == '': settings[19] = 'None'

        self.spin_entry_insert(self.target_value_box, settings[18], True)
        self.spin_entry_insert(self.target_value_box_two, settings[19], True)

        self.zero_type.set(settings[20])
        self.nil_swap(settings[20])
        if settings[21] == '':
            settings[21] = 'All'
        self.nil_type.set(settings[21])

        if '\n' not in settings[22]:
            self.exclude_today.set(settings[22])
        else:
            self.exclude_today.set(False)

        if len(settings) >= 25:
            self.rolling_average_on.set(settings[23])
            if self.rolling_average_on.get():
                if settings[24] == 0:
                    settings[24] = 'All'
                self.spin_entry_insert(self.rolling_average_interval, settings[24])
        else:
            self.rolling_average_on.set(False)
            self.spin_entry_insert(self.rolling_average_interval, entry='All', state='disabled')
        tk.messagebox.showinfo('Load complete', f"{target} settings loaded successfully.")
        self.__config_load_close(window)

    def __config_load_close(self, window):
        window.destroy()
        self.graph_creator.grab_set()

    def graph_create(self, configuration: list):
        """Plots a graph using values taken from various fields, assigned to a list with the following indices:
        0 = title, 1 = start date, 2 = end date, 3 = days ago, 4 = duration setting, 5 = graph type, 6 = min value type
        7 = min value (in hours, if applicable), 8 = min value (minutes), 9 = min value (seconds), 10 = max value type
        11 = max value (in hours, if applicable), 12 = max value (minutes), 13 = max value (seconds)
        14 = line styles (dot/flat dashed/solid), 15 = graph format (Line or Bar), 16 = selected categories
        17 = corresponding colors, 18 = Target value one, 19 = Target value two, 20 = empty value placeholder
        21 nil type (Keep all nil value, only to left bound, only to right bound, trim both sides), 22 = Exclude today
        23 = plot rolling average, 24 = rolling average section interval (days). Not all values are always used."""
        import matplotlib.pyplot as plt
        plt.title(configuration[0])
        miny = 0
        maxy = None
        exclude_today = ''
        if configuration[5] == 'Time':
            filename = "Dedication Record.txt"
            plt.ylabel('Time (hours)')
            if configuration[6] != 'Automatic':
                miny = int(configuration[7]) + (int(configuration[8]) / 60) + (int(configuration[9]) / 3600)
            if configuration[10] != 'Automatic':
                maxy = int(configuration[11]) + (int(configuration[12]) / 60) + (int(configuration[13]) / 3600)
        else:  # Increment
            filename = "Dedication#Record.txt"
            if configuration[6] != 'Automatic':
                miny = int(configuration[8])
            if configuration[10] != 'Automatic':
                maxy = int(configuration[12])
        plt.ylim(miny, maxy)
        contents = util.prepare_backup(filename)
        if configuration[4] == 'Days ago':
            if int(configuration[3]) >= len(contents) - 2:
                plot_dates = contents[3:]
            else:
                plot_dates = contents[-int(configuration[3]):]
        elif configuration[4] == 'Date range':
            for target_date in enumerate(contents[3:]):
                if target_date[1].split(' ')[0] == configuration[1]:
                    date_one = target_date[0]
                if target_date[1].split(' ')[0] == configuration[2]:
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
        if configuration[22] is True and plot_dates[-1][0:10] == str(datetime.now()).split()[0]:
            del plot_dates[-1]
            exclude_today = " (Today excluded)"

        if configuration[15] == 'Line':
            plt.xlabel(f'Date')
            short_dates = [full_date[5:10] for full_date in plot_dates]
            dots = []
            styles = []
            for entry in configuration[14].split(':'):
                dots.append(entry.split(' ')[0])
                styles.append(entry.split(' ')[1])
        else:
            bar_locations = []
            bar_labels = []
            if configuration[4] == 'Days ago':
                s = '' if len(plot_dates) == 1 else 's'
                plt.xlabel(f'Previous {len(plot_dates)} day{s}')
            elif configuration[4] == 'Date range':
                plt.xlabel(f'{configuration[1]} to {configuration[2]}{exclude_today}')
            else:
                plt.xlabel(f"All recorded dates{exclude_today}")

        plot_points = []
        bar_max = []
        for index, category in enumerate(configuration[16]):
            plot_points.append(self.get_data_points(category, plot_dates, configuration[5],
                                                    configuration[20], configuration[15]))
            if configuration[15] == 'Line':
                if configuration[17][index] == 'Auto':
                    plt.plot(short_dates, plot_points[index], marker=dots[index],
                             linestyle=styles[index], label=category)
                else:
                    plt.plot(short_dates, plot_points[index], color=configuration[17][index],
                             marker=dots[index], linestyle=styles[index], label=category)
            else:
                if configuration[17][index] == 'Auto':
                    plt.bar(int(index), height=sum(plot_points[index]), label=category)
                else:
                    plt.bar(int(index), height=sum(plot_points[index]),
                            color=configuration[17][index], label=category)
                bar_max.append(sum(plot_points[index]))
                bar_locations.append(int(index))
                bar_labels.append(category)

        # Setting X and Y limits (automatic)
        if configuration[10] == 'Automatic':
            if bar_max:
                maxy = max(bar_max)
            else:
                try:
                    maxy = max([item for group in plot_points for item in group if item is not None])
                except (TypeError, ValueError):
                    pass
            if configuration[18] != 'None' and configuration[18] != '' and float(configuration[18]) > maxy:
                maxy = float(configuration[18]) + 0.5
            if maxy == 0:
                maxy = 1
            plt.ylim(miny, maxy)

        second = 'Target'
        if configuration[18] not in ['None', ''] and float(configuration[18]) > 0:
            plt.axhline(y=float(configuration[18]), color='black', label='Target')
            second = None
        if configuration[19] not in ['None', ''] and float(configuration[19]) > 0:
            plt.axhline(y=float(configuration[19]), color='black', label=second)
        if configuration[15] == 'Line':
            if configuration[20] == 'Nil' and configuration[21] != 'Min':
                start = end = None
                if (configuration[21] == 'All' or configuration[21] == 'Left'
                 ) and any(plot[0] is None for plot in plot_points):
                    start = 0
                if (configuration[21] == 'All' or configuration[21] == 'Right'
                 ) and any(plot[-1] is None for plot in plot_points):
                    end = 0
                if start is not None or end is not None:  # Extends Nil graph range
                    invisible_graph_extender = [None for _ in short_dates]
                    invisible_graph_extender[0] = start
                    invisible_graph_extender[-1] = end
                    plt.plot(short_dates, invisible_graph_extender, linestyle='None')
            if configuration[23] is True and configuration[24] != 1:
                from statistics import mean
                if configuration[24] in ('0', 'All'):
                    plt.plot(short_dates, [mean(plot_points[0][:index+1]) for index in range(len(plot_points[0]))],
                             label=f"Rolling average ({configuration[16][0]})", color='#444444')
                else:
                    chunk_size = int(configuration[24])
                    try:
                        plt.plot(short_dates[:chunk_size], [mean(plot_points[0][chunk_size:chunk_size + index + 1])
                                                            for index in range(chunk_size)],
                                 label=f"Rolling average ({configuration[16][0]})", color='#444444')
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
            if configuration[5] == 'Time':
                font_size = int(10 - (len(short_dates)) / 40)
                if font_size < 1:
                    font_size = 1
                plt.xticks(rotation=45, ha='right', fontsize=font_size)
        else:
            plt.xticks(ticks=bar_locations, labels=bar_labels)
        plt.show()

    @staticmethod
    def get_data_points(category: str, dataset: list, graph_type: str, zero_type: str, graph_format: str) -> list:
        """Takes category, dataset (plot_dates (lines from file containing dates to be plotted)),
        graph_type (Time or Increment), zero_type (Zero or Nil) and graph_format (Line or Bar) and processes the
        dataset to return the time/increment values for each date in a list that can be used by pyplot"""
        mode_plot_points = []
        for data_set in dataset:
            for num, data_point in enumerate(data_set.split(' ')):
                if ' ' in category:  # Check if spaced name
                    if data_point == category.split(' ')[0]:
                        index = util.verify_spaced_name(category_list=data_set.split(' ')[:], category=category)
                        if index:
                            if graph_type == 'Time':
                                hours = data_set.split(' ')[index + 2]
                                mode_plot_points.append(hours)
                            else:
                                mode_plot_points.append(float(data_set.split(' ')[index + 2]))
                            break
                elif data_point == category:
                    if graph_type == 'Time':
                        hours = data_set.split(' ')[num + 2]
                        hours = int(hours.split(':')[0]) + (int(hours.split(':')[1]) / 60) + (
                                int(hours.split(':')[2]) / 3600)
                        mode_plot_points.append(hours)
                    else:
                        mode_plot_points.append(float(data_set.split(' ')[num + 2]))
                    break
            else:
                if zero_type == 'Zero' or graph_format == 'Bar':
                    mode_plot_points.append(0)
                else:
                    mode_plot_points.append(None)
        return mode_plot_points


def main():
    util.ensure_data_file_existence(str(str(datetime.now()).split()[0]))
    with open(r"Dedication Record.txt", 'r') as file:
        dedication_mode_file = file.readline()[0:21]
    GraphCreator(all_categories_time=util.get_categories_from_file(filename="Dedication Record.txt"),
                 all_categories_increment=util.get_categories_from_file(filename="Dedication#Record.txt"),
                 dedication_mode_file=dedication_mode_file).mainloop()


if __name__ == "__main__":
    main()

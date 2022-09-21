import dedicationsharedfunctions as util
try:
    import tkinter as tk
    from tkinter import messagebox
    from sys import exit
    from datetime import date, timedelta
    from time import sleep
    from _thread import start_new_thread
    from threading import Event
    from math import log
except ImportError as e:
    util.import_error_message(error=e)


class DedicationTracker(tk.Frame):
    __slots__ = ("all_categories", "timer_is_on", "incoming_category",  "_name", "current_category_time",
                 "current_category", "current_date", "dedication_mode", "widgetName", "master", "tk",
                 "current_date_label", 'dedication_mode_file', "all_categories_number", "root", "timer",
                 "scheduled", "category_entry", "all_categories_time", "dedication_mode_toggle_button",
                 "div1", "div2", "toggle_timer_button", "number_label", "number", "timer_number_label",
                 "number_field", "number_submit", "category_toggle_button", "children", "_w")

    def __init__(self):
        self.root = tk.Tk()
        tk.Frame.__init__(self)
        self.master.title("Dedication Tracker")
        self.master.geometry("500x270")
        self.master.resizable(False, False)
        self.place(relx=0.5, relwidth=1, anchor='n')

        self.current_date = str(date.today())
        self.incoming_category = tk.StringVar()
        self.current_category = tk.StringVar()
        self.number = 0
        self.timer_is_on = False

        util.ensure_data_file_existence(str(self.current_date), "Dedication Record.txt")
        util.ensure_data_file_existence(str(self.current_date), "Dedication#Record.txt")
        self.prepare_file("Dedication Record.txt")
        self.prepare_file("Dedication#Record.txt")

        self.current_date_label = tk.Label(self, text=self.current_date, font='arial 40')
        self.current_date_label.grid(column=1)
        tk.Button(self, text="Create Graph", font='arial 10', takefocus=False, command=self.open_graph_creator).grid(
            row=0, column=1, padx=(380, 0), ipady=5)
        tk.Button(self, text="Basic View", font='arial 10', command=self.basic_view, takefocus=False).grid(
            row=0, column=1, padx=(0, 380), ipady=5)

        tk.Button(self, text='Delete category', takefocus=False, command=lambda: self.load_saved_categories(
            self.dedication_mode_file, self.all_categories)).grid(
            row=2, column=1, padx=(0, 300), pady=(0, 50))
        self.category_entry = tk.Entry(self, width=24)
        self.category_entry.grid(row=2, column=1, padx=(0, 300))
        tk.Button(self, text="Add new category", font='arial 10', command=lambda: self.create_category(
            self.category_entry.get().strip())).grid(row=2, column=1, padx=(0, 300), pady=(55, 0))
        self.dedication_mode_toggle_button = tk.Button(self, font='arial 10')
        self.dedication_mode_toggle_button.grid(row=2, column=1, padx=(310, 0), pady=(0, 50))

        self.timer_number_label = tk.Label(self, font='arial 70', wraplength=500)
        self.timer_number_label.grid(row=1, column=1)
        self.toggle_timer_button = tk.Button(self, text="Start", command=self.start_timer, font='arial 30')
        self.number_field = tk.Entry(self)
        self.number_submit = tk.Button(self, text='Update', font='arial 20',
                                       command=lambda: self.update_number(self.number_field.get().strip()))

        self.category_toggle_button = tk.OptionMenu(self, self.incoming_category, value='')

        with open(r"Dedication Record.txt", 'r') as file:
            self.dedication_mode_file = file.readline()[0:21]

        self.all_categories_time = util.get_categories_from_file(filename="Dedication Record.txt")
        self.all_categories_number = util.get_categories_from_file(filename="Dedication#Record.txt")

        if self.dedication_mode_file == "Dedication Record.txt":
            self.initialize_time_mode(initial=True)
        else:
            self.initialize_number_mode(initial=True)
        today_categories = self.get_current_category_data()[1]
        if today_categories[2]:
            #  Sets category to the words in between the first and second blank spaces in today_categories
            self.incoming_category.set(
                ' '.join(today_categories[2:today_categories[today_categories.index('') + 1:].index('') + 2]))
            self.category_toggle()
        self.root.protocol('WM_DELETE_WINDOW', self.shutdown)  # Enable auto-save on exit

        start_new_thread(self.run_timer, ())
        start_new_thread(self.run_autosaver, ())

    def prepare_file(self, filename: str):
        """Fills in dates since last access with blank entries,
        including the current day, if no entry for the current day exists."""
        try:
            with open(filename, 'r+b') as file:
                file.seek(-2, 2)
                while file.read(1) != b'\n':
                    file.seek(-2, 1)
                read_date = date.fromisoformat(file.readline().decode()[:10])
                while str(read_date) != self.current_date:
                    read_date += timedelta(days=1)
                    file.write(bytes(f"\n{str(read_date).split(' ')[0]} | ", 'utf-8'))
        except PermissionError:
            tk.Label(self, text="Error in reading or creating file.\nIs there another file titled\n"
                                f"{self.dedication_mode_file} \nin the directory?",
                     font='arial 26').grid(padx=(15, 0), pady=(40, 0))
            raise Exception("Error in reading or creating file. "
                            f"Is there another file titled {self.dedication_mode_file} in the directory?")

    def get_current_category_data(self) -> tuple:
        """Reads the last line from the file to see if any categories already have data for the current date.
        Returns category_index (index in today_categories of first active category) and today_categories
        (list of items on last line of file). Time/Number data is two indices after its category name.
        e.g. [date, 'divider', category name, 'divider', time/number data]"""
        with open(self.dedication_mode_file, 'rb') as file:
            file.seek(-2, 2)
            while file.read(1) != b'\n':
                file.seek(-2, 1)
            today_modes = ''.join(''.join(file.readline().decode().split('|')).split('~')).split(' ')
        return self.get_category_index(category_list=today_modes, current_category=self.current_category.get()), today_modes

    def initialize_time_mode(self, initial=False):
        if not initial:
            self.number_field.grid_forget()
            self.number_submit.grid_forget()

            self.number_field.delete(0, 'end')

            self.dedication_mode_file = "Dedication Record.txt"
            with open("Dedication Record.txt", 'r+') as file:
                file.write("Dedication Record.txt")

            if (right_now := str(date.today())) != self.current_date:
                self.date_update(right_now)

        self.dedication_mode_toggle_button.config(
            text="Switch to number mode", command=self.initialize_number_mode)

        self.all_categories = self.all_categories_time
        self.set_up_categories(initial=True)
        self.set_internal_time()
        self.timer_number_label.config(text=str(self.current_category_time).rjust(8, '0'), font='arial 70')

        self.toggle_timer_button.grid(row=2, column=1)

    def set_internal_time(self):
        """Sets self.current_category_time to the time recorded for the current category for the current day in the
        file. If no category is active, or the current category does not have an entry for the current day, sets
        time to 0 hours, 0 minutes, 0 seconds."""
        if self.current_category.get() == '':
            self.current_category_time = timedelta(hours=0, minutes=0, seconds=0)
            return
        category_index, start_time = self.get_current_category_data()
        try:
            hours, minutes, seconds = start_time[category_index + 2].split(':')
            self.current_category_time = timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
        except (IndexError, TypeError):
            self.current_category_time = timedelta(hours=0, minutes=0, seconds=0)

    def start_timer(self):
        if self.current_category.get().strip() == '':
            tk.messagebox.showwarning('No category selected',
                                      'Please select a category from the drop-down menu to start adding time.')
            return
        self.toggle_timer_button.config(text="Pause", command=self.stop_timer, font='arial 25')
        self.timer_is_on = True
        self.timer.set()

    def stop_timer(self):
        self.toggle_timer_button.config(text="Start", command=self.start_timer, font='arial 30')
        self.timer_is_on = False
        self.save_records()

    def run_timer(self):
        self.scheduled = []
        while True:
            self.timer = Event()
            self.timer.wait()
            for _ in range(len(self.scheduled)):
                self.root.after_cancel(self.scheduled.pop())
            sleep(1)
            self.increment_timer()

    def increment_timer(self):
        if not self.timer_is_on:
            return
        self.scheduled.append(self.root.after(1000, self.increment_timer))
        self.current_category_time += timedelta(seconds=1)
        self.timer_number_label.config(text=str(self.current_category_time).rjust(8, '0'))
        if (right_now := str(date.today())) != self.current_date:
            self.date_update(right_now)

    def date_update(self, right_now: str):
        timer = self.timer_is_on
        if number := (self.dedication_mode_file == "Dedication#Record.txt"):
            self.save_records()
        else:  # Time mode
            self.stop_timer()
        self.current_date_label.config(text=right_now)
        self.current_date = right_now
        if self.save_records(number=number, new_day=True):  # Start entry for next day
            self.current_category_time = timedelta(seconds=0, minutes=0, hours=0)
            self.number = 0
            if self.dedication_mode_file == "Dedication Record.txt":
                self.timer_number_label.config(text=str(self.current_category_time).rjust(8, '0'))
            self.set_up_categories(initial=True)
        if self.dedication_mode_file == "Dedication Record.txt" and timer:
            self.start_timer()

    def initialize_number_mode(self, initial=False):
        if not initial:
            self.timer_is_on = False
            self.save_records()

            self.toggle_timer_button.grid_forget()

            with open("Dedication Record.txt", 'r+') as file:
                file.write("Dedication#Record.txt")
            self.dedication_mode_file = "Dedication#Record.txt"
            if (right_now := str(date.today())) != self.current_date:
                self.date_update(right_now)

        self.all_categories = self.all_categories_number
        self.set_up_categories(initial=True)
        self.dedication_mode_toggle_button.config(text="Switch to time mode", command=self.initialize_time_mode)

        self.timer_number_label.config(text="0")
        self.number_field.grid(row=2, column=1, pady=(0, 50))
        self.number_submit.grid(row=2, column=1, pady=(35, 0))

    def update_number(self, number: str):
        if (right_now := str(date.today())) != self.current_date:
            self.date_update(right_now)
        if self.current_category.get().strip() == '':
            tk.messagebox.showwarning('No category selected',
                                      'Please select a category from the drop-down menu to add a value to.')
            return
        if ' ' in number:
            tk.messagebox.showwarning('Invalid entry', 'Values cannot contain empty spaces.')
            return
        try:
            _ = float(number)
        except ValueError:
            tk.messagebox.showwarning('Invalid entry', 'Values can only be integers or decimals.')
            return
        self.number = number
        self.save_records(number=True)
        self.timer_number_label.config(font=('arial', self.text_resize(number)), text=self.number_safeguard(number))
        self.number_field.delete(0, 'end')

    @staticmethod
    def text_resize(number: int, ) -> int:
        """Automatically resizes the text displaying large numbers in number mode."""
        if len(str(number)) < 10:
            return 70
        elif (size := 70 - log((len(str(number)) - 8) ** 15)) < 12:
            return 12
        return round(size)

    @staticmethod
    def number_safeguard(number: str) -> str:
        """Prevents excessively large values in number mode from pushing buttons off the screen."""
        if len(number) > 328:
            return number[:329] + '...'
        return number

    def set_up_categories(self, initial: bool, named_category='', category_num=0):
        """Prepares a list of all categories accessed in the OptionMenu, and sets the OptionMenu options to it. This
        occurs whenever changing modes (Time/Number), and when a category is added or deleted. Sets category back to
        whatever it was before after resetting the OptionMenu, unless the currently active category was deleted."""
        if named_category == self.current_category.get() and category_num != 0:
            initial = 'Remove current category'
        if initial:
            self.current_category.set('')
            self.incoming_category.set('')
            if initial == 'Remove current category':
                self.number = 0
                self.current_category_time = timedelta(seconds=0)
                if self.dedication_mode_file == "Dedication Record.txt":
                    self.stop_timer()
                    self.timer_number_label.config(text=str(self.current_category_time).rjust(8, '0'))
                else:
                    self.timer_number_label.config(text="0")
        if category_num != 0:
            del self.all_categories[category_num]
        self.category_toggle_button.destroy()
        if self.all_categories:
            self.category_toggle_button = tk.OptionMenu(self, self.incoming_category, *self.all_categories, command=self.category_toggle)
        else:
            self.category_toggle_button = tk.OptionMenu(self, self.incoming_category, '', command=self.category_toggle)
        self.category_toggle_button.grid(row=2, column=1, padx=(310, 0), pady=(30, 0))
        self.category_toggle_button.config(width=24)

    @staticmethod
    def get_category_index(category_list: list, current_category: str) -> int | None:
        """Returns the last (and only, in the case of names without spaces) index of the category name from a list
        made from splitting the file line at spaces. This index +2 is used in various places to get the time/number
        data for the given category."""
        if ' ' in current_category:
            return util.verify_spaced_name(category_list=category_list, category=current_category)
        else:
            try:
                return category_list.index(current_category)
            except ValueError:
                pass

    def category_toggle(self, category=None):
        if self.current_category.get() != category:
            self.save_records()
            self.current_category.set(self.incoming_category.get())
            if self.dedication_mode_file == "Dedication Record.txt":
                self.set_internal_time()
                self.timer_number_label.config(text=str(self.current_category_time).rjust(8, '0'))
            else:
                today_categories = self.get_current_category_data()[1]
                if category_index := self.get_category_index(category_list=today_categories,
                                                             current_category=self.current_category.get()):
                    self.number = today_categories[category_index + 2]
                else:
                    self.number = 0
                self.timer_number_label.config(font=('arial', self.text_resize(self.number)),
                                               text=self.number_safeguard(str(self.number)))

    def add_today_category(self, current_category: str):
        """Adds data for a category to the file when that category first saves data for the current date."""
        category_index, today_categories = self.get_current_category_data()
        if current_category not in today_categories[2:-1:4] and current_category != '' and category_index is None:
            with open(self.dedication_mode_file, "r+b") as file:
                file.seek(0, 2)
                if self.dedication_mode_file == "Dedication Record.txt":
                    file.write(bytes(f"{current_category.strip()} ~ 00:00:00 | ", 'utf-8'))
                else:
                    file.write(bytes(f"{current_category.strip()} ~ 0 | ", 'utf-8'))

    def create_category(self, new_category: str):
        if new_category == '' or new_category in self.all_categories:
            return
        if any(char in new_category for char in ('|', '~', '  ')):
            tk.messagebox.showwarning('Invalid category name', "Category names may not contain a bar |"
                                                               " tilde ~ or consecutive empty spaces '  '.")
            return
        if len(new_category) > 24:
            if not tk.messagebox.askyesno('Long category name', 'Long category names may cause display issues.'
                                                                ' Are you sure you wish to proceed?',
                                          icon='warning'):
                return
        new = util.prepare_backup(self.dedication_mode_file)
        new[2] = f"{new[2][:-1]}{new_category} | \n"
        with open(self.dedication_mode_file, 'w') as file:
            file.write(''.join(new))
        self.all_categories.append(new_category)
        self.category_entry.delete(0, 'end')
        self.set_up_categories(initial=False)

    def save_records(self, number=False, new_day=False):
        if (self.dedication_mode_file == "Dedication Record.txt" and str(self.current_category_time) == '0:00:00') or \
                self.current_category.get() == '' or (self.dedication_mode_file == "Dedication#Record.txt" and not number):
            return
        if new_day:
            with open(self.dedication_mode_file, "r+b") as file:
                file.seek(-2, 2)
                while file.read(1) != b'\n':
                    file.seek(-2, 1)
                if file.readline().decode()[:10] != self.current_date:  # Should always proceed
                    file.write(bytes(f"\n{str(self.current_date)} | ", 'utf-8'))
                    tk.messagebox.showinfo('New day notice', "Previous day's results have been saved.\n"
                                           "The timer and categories have been reset for the new day.")
                    return True
            return
        self.add_today_category(self.current_category.get())
        saved_line = util.prepare_backup(self.dedication_mode_file)[-1].split(' ')
        category_index = self.get_category_index(category_list=saved_line, current_category=self.current_category.get())
        if self.dedication_mode_file == "Dedication Record.txt":
            saved_line[category_index + 2] = str(self.current_category_time).rjust(8, '0')
        else:  # Number mode
            saved_line[category_index + 2] = str(self.number)
        saved_line = ' '.join(saved_line)
        with open(self.dedication_mode_file, "r+b") as file:
            file.seek(-2, 2)
            while file.read(1) != b'\n':
                file.seek(-2, 1)
            file.truncate()
            file.write(bytes(saved_line, 'utf-8'))

    def run_autosaver(self):
        while True:
            sleep(300)
            if (right_now := str(date.today())) != self.current_date:
                self.date_update(right_now)
            else:
                self.save_records()

    def basic_view(self):
        if (right_now := str(date.today())) != self.current_date:
            self.date_update(right_now)
        basic_window = tk.Toplevel(self)
        basic_window.resizable(False, False)
        basic_window.grab_set()
        basic_scroll_x = tk.Scrollbar(basic_window, orient='horizontal')
        basic_scroll_y = tk.Scrollbar(basic_window)
        basic_scroll_x.grid(row=1, sticky='ew')
        basic_scroll_y.grid(row=0, column=1, sticky='ns')
        basic_listbox = tk.Listbox(basic_window, height=30, width=60, font='arial 15', bg='#f0f0f0',
                                   yscrollcommand=basic_scroll_y.set, xscrollcommand=basic_scroll_x.set)
        basic_listbox.grid(row=0, column=0)
        basic_scroll_x.config(command=basic_listbox.xview)
        basic_scroll_y.config(command=basic_listbox.yview)
        spacer = '-' if self.dedication_mode_file == "Dedication Record.txt" else ':'
        with open(self.dedication_mode_file, "r") as file:
            next(file)
            basic_window.title(file.readline())
            for line in file:
                basic_listbox.insert('end', (line.replace('~', spacer)).strip())

    def load_saved_categories(self, dedication_mode: str, all_categories: list):
        loaded_categories = tk.Toplevel()
        loaded_categories.title("Delete category")
        loaded_categories.resizable(False, False)
        loaded_categories.grab_set()
        scroll = tk.Scrollbar(loaded_categories)
        main_category_listbox = tk.Listbox(loaded_categories, width=24, font='courier 12', height=20,
                                           yscrollcommand=scroll.set)
        main_category_listbox.grid()
        tk.Button(loaded_categories, text='Delete', command=lambda: util.select_delete(
            target_listbox=main_category_listbox, filename=dedication_mode, dedication_tracker=self)).grid()
        scroll.grid(row=0, column=1, sticky='ns')
        scroll.config(command=main_category_listbox.yview)
        for category in all_categories:
            main_category_listbox.insert('end', category)

    def open_graph_creator(self):
        import Dedication_Graph_Creator as dgc
        dgc.GraphCreator(all_categories_time=self.all_categories_time, all_categories_number=self.all_categories_number,
                         dedication_mode_file=self.dedication_mode_file).tk.mainloop()

    def shutdown(self):
        try:
            self.save_records()
        except Exception as err:
            if not tk.messagebox.askyesno(
                    'Autosave failed', f'An error occurred when attempting to save your work on exit.\n"{err}"\nIt is '
                                       'possible that your work was not recorded properly during this session, so you '
                                       'may wish to record it manually. \nDo you want to quit anyway?', icon='warning'):
                return
        exit()


if __name__ == "__main__":
    DedicationTracker().tk.mainloop()

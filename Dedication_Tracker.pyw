import tkinter as tk
from tkinter import messagebox
from sys import exit
from datetime import datetime, date, timedelta
from time import sleep
from _thread import start_new_thread
from threading import Event
import Dedication_Graph_Creator as dgc
import dedicationsharedfunctions as util


class DedicationTracker(tk.Frame):
    __slots__ = ("all_categories", "timer_is_on", "incoming_category",  "_name", "current_category_time",
                 "current_category", "current_date", "dedication_mode", "widgetName", "master", "tk",
                 "current_date_label", 'dedication_mode_file', "all_categories_increment",
                 "counter_frame", "category_entry", "all_categories_time", "dedication_mode_toggle_button",
                 "div1", "div2", "toggle_timer_button", "increment_label", "increment", "timer_increment_label",
                 "increment_field", "increment_submit", "category_toggle_button", "children", "_w")

    def __init__(self):
        root = tk.Tk()
        tk.Frame.__init__(self)
        self.master.title("Dedication Tracker")
        self.master.geometry("500x270")
        self.master.resizable(False, False)
        self.place(relx=0.5, relwidth=1, anchor='n')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(3, weight=1)
        self.current_date = str(datetime.now()).split()[0]
        self.incoming_category = tk.StringVar()
        self.current_category = tk.StringVar()
        self.increment = 0
        self.timer_is_on = False

        util.ensure_data_file_existence(str(self.current_date))
        self.prepare_file("Dedication Record.txt")
        self.prepare_file("Dedication#Record.txt")

        self.current_date_label = tk.Label(self, text=self.current_date, font='arial 40')
        self.current_date_label.grid(column=1)
        tk.Button(self, text="Create Graph", font='arial 10', takefocus=False, command=lambda: dgc.GraphCreator(
            all_categories_time=self.all_categories_time, all_categories_increment=self.all_categories_increment,
            dedication_mode_file=self.dedication_mode_file).tk.mainloop()).grid(row=0, column=1, padx=(380, 0), ipady=5)
        tk.Button(self, text="Basic View", font='arial 10', command=self.basic_view, takefocus=False).grid(
            row=0, column=1, padx=(0, 380), ipady=5)
        self.counter_frame = tk.Frame(self)
        self.counter_frame.grid(row=1, column=1)
        tk.Button(self, text='Delete category', takefocus=False, command=lambda: self.load_saved_categories(
            self.dedication_mode_file, self.all_categories)).grid(row=2, column=1, padx=(0, 300), pady=(0, 50))
        self.category_entry = tk.Entry(self, width=24)
        self.category_entry.grid(row=2, column=1, padx=(0, 300))
        tk.Button(self, text="Add new category", font='arial 10', command=lambda: self.create_category(
            self.category_entry.get().strip())).grid(row=2, column=1, padx=(0, 300), pady=(55, 0))
        self.dedication_mode_toggle_button = tk.Button(self, font='arial 10')
        self.dedication_mode_toggle_button.grid(row=2, column=1, padx=(310, 0), pady=(0, 50))

        self.timer_increment_label = tk.Label(self.counter_frame, text='0', font='arial 70')
        self.toggle_timer_button = tk.Button(self, text="Start", command=self.timer_on, font='arial 30')

        self.timer_increment_label = tk.Label(self.counter_frame, text=self.increment, font='arial 70')
        self.increment_field = tk.Entry(self)
        self.increment_submit = tk.Button(self, text='Update', font='arial 20',
                                          command=lambda: self.update_increment(self.increment_field.get().strip()))

        self.category_toggle_button = tk.OptionMenu(self, self.incoming_category, value='')

        with open(r"Dedication Record.txt", 'r') as file:
            self.dedication_mode_file = file.readline()[0:21]

        self.all_categories_time = util.get_categories_from_file(filename="Dedication Record.txt")
        self.all_categories_increment = util.get_categories_from_file(filename="Dedication#Record.txt")

        if self.dedication_mode_file == "Dedication Record.txt":
            self.initialize_time_mode(initial=True)
        else:
            self.initialize_increment_mode(initial=True)
        _, today_categories = self.get_current_category_data()
        if today_categories[2]:
            #  Sets category to the words in between the first and second blank spaces in today_categories
            self.incoming_category.set(' '.join(today_categories[2:today_categories[today_categories.index('') + 1:].index('') + 2]))
            self.category_toggle()
        root.protocol('WM_DELETE_WINDOW', self.shutdown)  # Enable auto-save on exit

        start_new_thread(self.run_timer, ())
        start_new_thread(self.run_autosaver, ())

    def prepare_file(self, filename: str):
        try:
            with open(filename, 'r+b') as file:
                file.seek(-2, 2)
                while file.read(1) != b'\n':
                    file.seek(-2, 1)
                read_date = file.readline().decode()[:10]
                read_date = datetime(int(''.join(read_date.split('-')[0])),
                                     int(''.join(read_date.split('-')[1])),
                                     int(''.join(read_date.split('-')[2])))
                while True:
                    if str(read_date).split(' ')[0] != self.current_date:
                        read_date += timedelta(days=1)
                        file.write(bytes(f"\n{str(read_date).split(' ')[0]} | ", 'utf-8'))
                    else:
                        break
        except PermissionError:
            tk.Label(self, text="Error in reading or creating file.\nIs there another file titled\n"
                                f"{self.dedication_mode_file} \nin the directory?",
                     font='arial 26').grid(padx=(15, 0), pady=(40, 0))
            raise Exception("Error in reading or creating file. "
                            f"Is there another file titled {self.dedication_mode_file} in the directory?")

    def get_current_category_data(self) -> tuple:
        """Reads the last line from the file to see if any categories already have progress for the current date.
        Returns category_index (index in today_categories of first progressed category) and today_categories
        (list of items on last line of file). Time/increment data is two indices after its category name."""
        with open(self.dedication_mode_file, 'rb') as file:
            file.seek(-2, 2)
            while file.read(1) != b'\n':
                file.seek(-2, 1)
            today_modes = ''.join(''.join(file.readline().decode().split('|')).split('~')).split(' ')
        return self.get_category_index(category_list=today_modes, current_category=self.current_category.get()), today_modes

    def initialize_time_mode(self, initial=False):
        if not initial:
            self.save_records()

            for target in (self.increment_field, self.increment_submit):
                target.grid_forget()

            self.increment_field.delete(0, 'end')

            self.dedication_mode_file = "Dedication Record.txt"
            with open("Dedication Record.txt", 'r+') as file:
                file.write("Dedication Record.txt")

            if right_now := str(datetime.now()).split()[0] != self.current_date:
                self.date_update(right_now)

        self.dedication_mode_toggle_button.config(
            text="Switch to increment mode", command=self.initialize_increment_mode)

        self.all_categories = self.all_categories_time
        self.set_up_categories(initial=True)
        self.set_internal_time()
        self.set_timer()

        self.timer_increment_label.grid(row=0, column=3, columnspan=3)
        self.toggle_timer_button.grid(row=2, column=1)

    def set_internal_time(self):
        seconds = minutes = hours = 0
        if self.current_category.get() != '':
            category_index, start_time = self.get_current_category_data()
            try:
                start_time = start_time[category_index + 2].split(':')
                if start_time[0].lstrip('0') != '':
                    hours = int(start_time[0])
                else:
                    hours = 0
                if start_time[1].lstrip('0') != '':
                    minutes = int(start_time[1])
                else:
                    minutes = 0
                if start_time[2].lstrip('0') != '':
                    seconds = int(start_time[2])
                else:
                    seconds = 0
            except (IndexError, TypeError):
                pass
        self.current_category_time = timedelta(seconds=seconds, minutes=minutes, hours=hours)

    def set_timer(self):
        self.timer_is_on = False
        self.timer_increment_label.config(text=str(self.current_category_time).rjust(8, '0'))
        self.toggle_timer_button.config(text="Start", command=self.timer_on)

    def timer_on(self):
        if self.current_category.get().strip() == '':
            return tk.messagebox.showwarning('No category selected',
                                             'Please select a category from the drop-down menu to start adding time.')
        self.toggle_timer_button.config(text="Pause", command=self.timer_off, font='arial 25')
        self.timer_is_on = True
        self.timer.set()

    def timer_off(self):
        self.toggle_timer_button.config(text="Start", command=self.timer_on, font='arial 30')
        self.timer_is_on = False
        self.save_records()

    def run_timer(self):
        one_second = timedelta(seconds=1)
        while True:
            self.timer = Event()
            self.timer.wait()
            sleep(1)
            while self.timer_is_on:
                self.current_category_time += one_second
                self.timer_increment_label.config(text=str(self.current_category_time).rjust(8, '0'))
                if (right_now := str(datetime.now()).split()[0]) != self.current_date:
                    self.date_update(right_now)
                sleep(0.992)  # 0.992 seems most accurate relative to system time

    def date_update(self, right_now: str):
        self.save_records()
        self.current_date_label.config(text=right_now)
        self.current_date = right_now
        if self.dedication_mode_file == "Dedication Record.txt":
            self.set_internal_time()
            self.set_timer()
        start_new_thread(self.save_records, (False, True))  # Start entry for next day
        self.set_up_categories(initial=True)

    def initialize_increment_mode(self, initial=False):
        if not initial:
            self.timer_is_on = False
            self.save_records()

            self.toggle_timer_button.grid_forget()

            with open("Dedication Record.txt", 'r+') as file:
                file.write("Dedication#Record.txt")
            self.dedication_mode_file = "Dedication#Record.txt"
            if (right_now := str(datetime.now()).split()[0]) != self.current_date:
                self.date_update(right_now)

        self.all_categories = self.all_categories_increment
        self.set_up_categories(initial=True)
        self.dedication_mode_toggle_button.config(text="Switch to time mode", command=self.initialize_time_mode)

        self.timer_increment_label.grid()
        self.timer_increment_label.config(text="0", wraplength=500)
        self.increment_field.grid(row=2, column=1, pady=(0, 50))
        self.increment_submit.grid(row=2, column=1, pady=(35, 0))

    def update_increment(self, increment: str):
        if (right_now := str(datetime.now()).split()[0]) != self.current_date:
            self.date_update(right_now)
        if self.current_category.get().strip() == '':
            tk.messagebox.showwarning('No category selected',
                                      'Please select a category from the drop-down menu to add a value to.')
            return
        if ' ' in increment:
            tk.messagebox.showwarning('Invalid entry', 'Values cannot contain empty spaces.')
            return
        try:
            _ = float(increment)
        except ValueError:
            tk.messagebox.showwarning('Invalid entry', 'Values can only be integers or decimals.')
            return
        self.increment = increment
        self.save_records(increment=True)
        self.text_resize()
        self.increment_field.delete(0, 'end')

    def text_resize(self):
        if len(str(self.increment)) < 10:
            size = 70
        else:
            size = 70 - log((len(str(self.increment)) - 8) ** 15)
        if size < 9:
            size = 9
        self.timer_increment_label.config(font=('arial', round(size)), text=self.increment)

    def set_up_categories(self, initial: bool, named_category='', category_num=0):
        """Prepares a list of all categories accessed in the OptionMenu, and sets the OptionMenu options to it. This
        occurs whenever changing modes (time/increment), and when a category is added or deleted. Sets category back to
        whatever it was before after resetting the OptionMenu, unless the currently active category was deleted."""
        if named_category == self.current_category.get() and category_num != 0:
            initial = 'Remove current category'
        if initial:
            self.current_category.set('')
            self.incoming_category.set('')
            if initial == 'Remove current category':
                self.increment = 0
                self.current_category_time = timedelta(seconds=0)
                if self.dedication_mode_file == "Dedication Record.txt":
                    self.timer_off()
                    self.set_timer()
                else:
                    self.timer_increment_label.config(text="0")
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
        made from splitting the file line at spaces. This index +2 is used in various places to get the time/increment
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
                self.set_timer()
            else:
                _, today_categories = self.get_current_category_data()
                if category_index := self.get_category_index(category_list=today_categories, current_category=self.current_category.get()):
                    print(category_index)
                    self.increment = today_categories[category_index + 2]
                else:
                    self.increment = 0
                self.text_resize()

    def add_today_category(self, current_category: str):
        category_index, today_categories = self.get_current_category_data()
        if current_category not in today_categories[2:-1:4] and current_category != '' and category_index is None:
            with open(self.dedication_mode_file, "r+b") as file:
                file.seek(0, 2)
                if self.dedication_mode_file == "Dedication Record.txt":
                    file.write(bytes(f"{current_category.strip()} ~ 00:00:00 | ", 'utf-8'))
                else:
                    file.write(bytes(f"{current_category.strip()} ~ 0 | ", 'utf-8'))

    def create_category(self, new_category: str):
        if new_category != '' and new_category not in self.all_categories:
            if not any(char in new_category for char in (':', '|', '~', '  ')):
                if len(new_category) > 24:
                    if not tk.messagebox.askyesno('Long category name', 'Long category names may cause display issues.'
                                                                        ' Are you sure you wish to proceed?',
                                                  icon='warning'):
                        return None
                new = util.prepare_backup(self.dedication_mode_file)
                new[2] = f"{new[2][:-1]}{new_category} : \n"
                with open(self.dedication_mode_file, 'w') as file:
                    file.write(''.join(new))
                self.all_categories.append(new_category)
                self.category_entry.delete(0, 'end')
                self.set_up_categories(initial=False)
            else:
                tk.messagebox.showwarning('Invalid category name', "Category names may not contain a colon : bar |"
                                                                   " tilde ~ or consecutive empty spaces '  '.")

    def save_records(self, increment=False, new_day=False):
        if (self.dedication_mode_file == "Dedication Record.txt" and str(self.current_category_time) == '0:00:00') or \
                self.current_category.get() == '' or (self.dedication_mode_file == "Dedication#Record.txt" and not increment):
            return
        if new_day:
            with open(self.dedication_mode_file, "r+b") as file:
                file.seek(-2, 2)
                while file.read(1) != b'\n':
                    file.seek(-2, 1)
                if file.readline().decode()[:10] != self.current_date:  # Should always proceed
                    file.write(bytes(f"\n{str(self.current_date)} | ", 'utf-8'))
                    self.increment = 0
                    self.current_category_time = timedelta(seconds=0)
                    if self.dedication_mode_file == "Dedication Record.txt":
                        self.set_timer()
                    return tk.messagebox.showinfo('New day notice', "Previous day's results have been saved.\n"
                                                  "The timer and categories have been reset for the new day.")
        self.add_today_category(self.current_category.get())
        saved_line = util.prepare_backup(self.dedication_mode_file)[-1].split(' ')
        category_index = self.get_category_index(category_list=saved_line, current_category=self.current_category.get())
        if self.dedication_mode_file == "Dedication Record.txt":
            saved_line[category_index + 2] = str(self.current_category_time).rjust(8, '0')
        else:
            saved_line[category_index + 2] = str(self.increment)
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
            if (right_now := str(datetime.now()).split()[0]) != self.current_date:
                self.date_update(right_now)
            else:
                self.save_records()

    def basic_view(self):
        if (right_now := str(datetime.now()).split()[0]) != self.current_date:
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
        tk.Button(loaded_categories, text='Delete', command=lambda: util.select_delete(target_listbox=main_category_listbox,
                                                              filename=dedication_mode, dedication_tracker=self)).grid()
        scroll.grid(row=0, column=1, sticky='ns')
        scroll.config(command=main_category_listbox.yview)
        for category in all_categories:
            main_category_listbox.insert('end', category)

    def shutdown(self):
        try:
            self.save_records()
        except Exception as e:
            if not tk.messagebox.askyesno('Autosave failed', 'An error occurred when attempting to save your work on '
                                          f'exit.\n"{e}"\nDo you wish to quit anyway?', icon='warning'): return
        exit()


if __name__ == "__main__":
    dedication_tracker = DedicationTracker()
    dedication_tracker.tk.mainloop()

import tkinter as tk
from os.path import exists


def prepare_backup(filename: str):
    with open(filename, 'r') as file:
        file_contents = file.readlines()
    with open(f"{filename}.bak", 'w+') as file:
        file.write(''.join(file_contents))
    return file_contents


def verify_spaced_name(category_list: list, category: str):
    """Splits a given string containing spaces (generally a line from a file), and compares it piecewise against a list
    of known category names. If a match is found, returns the index of the split list corresponding to the end of the
    spaced category name."""
    if category not in ' '.join(category_list):
        return
    current_category_list_form = category.split(' ')
    for index, category_name in enumerate(category_list):
        if current_category_list_form[0] == category_name:
            for num, word in enumerate(current_category_list_form):
                if word != category_list[index + num]:
                    break
                if current_category_list_form[-1] == category_list[index + num] and category_list[index + num + 1] == '':
                    return index + num


def select_delete(target_listbox: tk.Listbox, filename: str, dedication_tracker):
    try:
        target, target_num = target_listbox.get(target_listbox.curselection()[0]), target_listbox.curselection()[0]
    except (tk.TclError, IndexError):
        return
    if not target:
        return
    name = 'Config' if filename == "Graph Config.txt" else 'Category'
    if not tk.messagebox.askyesno(f'{name} deletion', f"Are you sure you want to delete {target} ?"):
        return
    new = prepare_backup(filename)
    if filename == "Graph Config.txt":
        del new[target_num + 1]
        with open("Graph Config.txt", "w+") as file:
            file.write(''.join(new))
    else:
        category_line = new[2].split(':')
        del category_line[target_num + 1]
        category_line = ''.join(category_line) + ' : \n' if len(category_line) == 1 else ':'.join(category_line)
        new[2] = category_line
        with open(filename, "w+") as file:
            file.write(''.join(new))
    target_listbox.delete(target_num)
    if filename != "Graph Config.txt":
        from Dedication_Tracker import DedicationTracker
        DedicationTracker.set_up_categories(dedication_tracker, initial=False, named_category=target, category_num=target_num)
    tk.messagebox.showinfo('Deletion complete', f"{target} deleted successfully.")


def get_categories_from_file(filename: str) -> list:
    with open(filename, 'r') as file:
        next(file)
        next(file)
        categories = file.readline().split(':')[1:-1]
    return [category_name.strip() for category_name in categories]


def ensure_data_file_existence(current_date: str):
    if not exists("Dedication Record.txt"):
        with open(r"Dedication Record.txt", 'a') as file:
            file.write("Dedication Record.txt -"
                       "Modifying this file directly may render it unreadable to the program.\nDedication tracking"
                       f"started on {current_date}\nSaved categories include: \n{current_date} | ")
    if not exists("Dedication#Record.txt"):
        with open(r"Dedication#Record.txt", 'a') as file:
            file.write("Modifying this file directly may render it unreadable to the program.\nDedication tracking"
                       f"started on {current_date}\nSaved categories include: \n{current_date} | ")

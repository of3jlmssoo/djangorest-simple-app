import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox, ttk
from tkinter.messagebox import showinfo

from refs import DEFAULT_DIR, DEFAULT_FILE

# DEFAULT_DIR = '/'

# create the root window
root = tk.Tk()
root.title('Tkinter File Dialog')
# root.resizable(False, False)
root.geometry('300x150+100+100')


def select_files():
    filetypes = (
        # ('text files', '*.txt'),
        ('html files', '*.html'),
        ('All files', '*.*')
    )

    filenames = fd.askopenfilename(
        title='Open files',
        initialdir=DEFAULT_DIR,
        # initialfile="'" + DEFAULT_FILE + "'",
        initialfile=DEFAULT_FILE,
        filetypes=filetypes)

    showinfo(
        title='Selected Files',
        message=filenames
    )

    print(f'{filenames}')
    display_result(filenames)


def display_result(filenames):
    Txt = tk.Text(root, height=5, width=200)
    lbl = tk.Label(root, text="配当情報")

    message = filenames + 'is selected to process.'

    exitb = tk.Button(root, text="Exit",
                      command=root.destroy)

    root.geometry('1000x150+100+100')

    open_button.pack_forget()
    lbl.pack()
    Txt.pack()
    # exitb.pack(pady=2)
    exitb.pack()
    Txt.insert(tk.END, message)


open_button = ttk.Button(
    root,
    text='Open Files',
    command=select_files
)


open_button.pack(expand=True)

root.mainloop()

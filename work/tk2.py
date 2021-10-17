import tkinter as tk
import tkinter.filedialog
from input_files import Input_files

INITIAL_DIR = "/home/hiroshisakuma/Downloads/"
INITIAL_FILE1 = "/home/hiroshisakuma/Downloads/Dividend Calendar - Investing.com.html"
INITIAL_FILE2 = "/home/hiroshisakuma/Downloads/portf.txt"
GEOMETRY1 = "700x600"


class windowclass():
    def __init__(self, master, input_class):
        self.master = master

        frame_1 = tk.Frame(root, width=700, height=80, bd=4, relief=tk.GROOVE)
        frame_2 = tk.Frame(root, width=700, height=80, bd=4, relief=tk.GROOVE)
        frame_3 = tk.Frame(root, width=700, height=80, bd=4, relief=tk.GROOVE)

        """ frame_1 """
        button = tk.Button(
            # root,
            frame_1,
            text='ファイルダイアログを開く',
            font=(
                '',
                10),
            width=24,
            height=1,
            bg='#999999',
            activebackground="#aaaaaa")
        button.bind('<ButtonPress>', self.file_dialog)
        # button.pack(pady=0)
        frame_1.grid(row=0, column=0, columnspan=2, sticky=tk.W)  # + tk.E)
        # frame_2.grid(row=1, column=0)
        # frame_3.grid(row=1, column=1, sticky=N + S)
        # button.pack(anchor=tk.W)

        self.file_name = tk.StringVar()
        # self.file_name.set('未選択です')
        self.file_name.set(INITIAL_FILE1)
        label = tk.Label(frame_1, textvariable=self.file_name, font=('', 12))
        input_class.div_info = self.file_name.get()
        # label.pack(pady=10)
        frame_1.propagate(0)
        # label.pack(anchor=tk.W)
        # button.pack(anchor=tk.W)
        label.pack(fill=tk.X)
        button.pack()

        """ frame_2 """
        button = tk.Button(
            # root,
            frame_2,
            text='ファイルダイアログを開く',
            font=(
                '',
                10),
            width=24,
            height=1,
            bg='#999999',
            activebackground="#aaaaaa")
        button.bind('<ButtonPress>', self.file_dialog2)
        # button.bind(
        #     '<ButtonPress>',
        #     # self.file_dialogX(
        #     #     INITIAL_DIR,
        #     #     INITIAL_FILE2))
        # lambda event: self.file_dialogX(event, INITIAL_DIR, INITIAL_FILE2))
        # button.pack(pady=0)
        frame_2.grid(row=2, column=0, columnspan=2, sticky=tk.W)  # + tk.E)
        # button.pack()

        self.file_name2 = tk.StringVar()
        # self.file_name2.set('未選択です')
        self.file_name2.set(INITIAL_FILE2)
        # label = tk.Label(textvariable=self.file_name2, font=('', 12))
        label = tk.Label(frame_2, textvariable=self.file_name2, font=('', 12))
        input_class.port_info = self.file_name2.get()
        # label.pack(pady=40)
        frame_2.propagate(0)
        label.pack(fill=tk.X)
        button.pack()

        # self.btn = tk.Button(master, text="Button", command=self.command)
        self.btn = tk.Button(frame_3, text="Button", command=self.command)
        # self.btn.pack()
        frame_3.grid(row=3, column=0, columnspan=2, sticky=tk.W + tk.E)
        self.btn.pack()

    def command(self):
        self.master.withdraw()
        toplevel = tk.Toplevel(self.master)
        # toplevel.geometry("350x350")
        toplevel.geometry(GEOMETRY1)
        # print(self.file_name, self.file_name2)
        app = Demo2(toplevel)

    def file_dialog(self, event):
        fTyp = [("", "*")]
        # iDir = os.path.abspath(os.path.dirname(__file__))
        file_name = tk.filedialog.askopenfilename(
            filetypes=fTyp, initialdir=INITIAL_DIR, initialfile=INITIAL_FILE1)
        if len(file_name) == 0:
            self.file_name.set('選択をキャンセルしました')
        else:
            self.file_name.set(file_name)

    def file_dialog2(self, event):
        fTyp = [("", "*")]
        # iDir = os.path.abspath(os.path.dirname(__file__))
        file_name2 = tk.filedialog.askopenfilename(
            filetypes=fTyp, initialdir=INITIAL_DIR, initialfile=INITIAL_FILE2)
        if len(file_name2) == 0:
            self.file_name2.set('選択をキャンセルしました')
        else:
            self.file_name2.set(file_name2)


class Demo2:
    def __init__(self, master):

        self.master = master
        self.frame = tk.Frame(self.master)
        self.quitButton = tk.Button(
            self.frame,
            text='Quit',
            width=25,
            command=self.close_windows)
        self.quitButton.pack()
        self.frame.pack()

    def close_windows(self):
        self.master.destroy()
        root.quit()
        root.destroy()


root = tk.Tk()
root.title("window")
# root.geometry("700x1000")
root.geometry(GEOMETRY1)

i = Input_files()

cls = windowclass(root, i)
root.mainloop()

print(f'{i.div_info=} {i.port_info=}')
# def main():
#     root = tk.Tk()
#     app = Demo1(root)
#     root.mainloop()


# if __name__ == '__main__':
#     main()

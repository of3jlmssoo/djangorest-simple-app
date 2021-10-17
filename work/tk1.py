import os
import tkinter as tk
import tkinter.filedialog

INITIAL_DIR = "/home/hiroshisakuma/ダウンロード/"
INITIAL_FILE1 = "/home/hiroshisakuma/ダウンロード/Dividend Calendar - Investing.com.html"
INITIAL_FILE2 = "/home/hiroshisakuma/ダウンロード/portf.txt"


class TkinterClass:
    def __init__(self):
        root = tk.Tk()
        root.geometry("500x350")

        button = tk.Button(
            root,
            text='ファイルダイアログを開く',
            font=(
                '',
                20),
            width=24,
            height=1,
            bg='#999999',
            activebackground="#aaaaaa")
        button.bind('<ButtonPress>', self.file_dialog)
        button.pack(pady=40)

        self.file_name = tk.StringVar()
        self.file_name.set('未選択です')
        label = tk.Label(textvariable=self.file_name, font=('', 12))
        label.pack(pady=0)

        button = tk.Button(
            root,
            text='ファイルダイアログを開く',
            font=(
                '',
                20),
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

        button.pack(pady=40)

        self.file_name2 = tk.StringVar()
        self.file_name2.set('未選択です')
        label = tk.Label(textvariable=self.file_name2, font=('', 12))
        label.pack(pady=0)

        root.mainloop()

    # def file_dialogX(self, event, inidir, inifile):
    #     fTyp = [("", "*")]
    #     # iDir = os.path.abspath(os.path.dirname(__file__))
    #     file_name = tk.filedialog.askopenfilename(
    #         filetypes=fTyp, initialdir=inidir, initialfile=inifile)
    #     if len(file_name) == 0:
    #         self.file_name.set('選択をキャンセルしました')
    #     else:
    #         self.file_name.set(file_name)

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


if __name__ == '__main__':
    TkinterClass()

import tkinter as tk
import tkinter.filedialog

from div_mgmt import Div_Mgmt
from tkiwin import Secondwindow, windowclass

# """ config.pyに移す """
# INITIAL_DIR = "/home/hiroshisakuma/Downloads/"
# INITIAL_FILE1 = "/home/hiroshisakuma/Downloads/Dividend Calendar - Investing.com.html"
# INITIAL_FILE2 = "/home/hiroshisakuma/Downloads/portf.txt"
# GEOMETRY1 = "700x600"


# class windowclass():

#     def __init__(
#             self,
#             master: tk.Tk,
#             input_class: Input_files) -> None:
#         self.master = master

#         frame_1 = tk.Frame(root, width=700, height=80, bd=4, relief=tk.GROOVE)
#         frame_2 = tk.Frame(root, width=700, height=80, bd=4, relief=tk.GROOVE)
#         frame_3 = tk.Frame(root, width=700, height=80, bd=4, relief=tk.GROOVE)

#         """ frame_1 """
#         button = tk.Button(
#             # root,
#             frame_1,
#             text='対象ファイルを変更',
#             font=(
#                 '',
#                 8),
#             width=24,
#             height=1,
#             bg='#999999',
#             activebackground="#aaaaaa")
#         # button.bind('<ButtonPress>', self.file_dialog)
#         button.bind(
#             '<ButtonPress>',
#             lambda event: self.file_dialog1(event, input_class))

#         frame_1.grid(row=0, column=0, columnspan=2, sticky=tk.W)  # + tk.E)

#         self.file_name = tk.StringVar()
#         self.file_name.set(INITIAL_FILE1)
#         label = tk.Label(frame_1, textvariable=self.file_name, font=('', 12))
#         """ デフォルトファイル名をセット """
#         input_class.div_info = self.file_name.get()
#         frame_1.propagate(0)
#         label.pack(fill=tk.X)
#         button.pack()

#         """ frame_2 """
#         button = tk.Button(
#             # root,
#             frame_2,
#             text='対象ファイルを変更',
#             font=(
#                 '',
#                 8),
#             width=24,
#             height=1,
#             bg='#999999',
#             activebackground="#aaaaaa")

#         # button.bind('<ButtonPress>', self.file_dialog2)
#         button.bind(
#             '<ButtonPress>',
#             lambda event: self.file_dialog2(event, input_class))
#         frame_2.grid(row=2, column=0, columnspan=2, sticky=tk.W)  # + tk.E)

#         self.file_name2 = tk.StringVar()
#         self.file_name2.set(INITIAL_FILE2)
#         label = tk.Label(frame_2, textvariable=self.file_name2, font=('', 12))
#         """ デフォルトファイル名をセット """
#         input_class.port_info = self.file_name2.get()
#         frame_2.propagate(0)
#         label.pack(fill=tk.X)
#         button.pack()

#         """ frame_3 """
#         self.btn = tk.Button(frame_3, text="Button", command=self.command)
#         frame_3.grid(row=3, column=0, columnspan=2, sticky=tk.W + tk.E)
#         self.btn.pack()

#     def command(self) -> None:
#         self.master.withdraw()
#         toplevel = tk.Toplevel(self.master)
#         toplevel.geometry(GEOMETRY1)
#         app = Secondwindow(toplevel)

#     def file_dialog1(self, event: tk.Event, input_class: Input_files) -> None:
#         # print(f'{type(event)=}')

#         fTyp = [("", "*")]
#         file_name = tk.filedialog.askopenfilename(
#             filetypes=fTyp, initialdir=INITIAL_DIR, initialfile=INITIAL_FILE1)
#         if len(file_name) == 0:
#             self.file_name.set('選択をキャンセルしました')
#         else:
#             self.file_name.set(file_name)
#         i.div_info = file_name

# def file_dialog2(self, event: tk.Event, input_class: Input_files) ->
# None:

#         fTyp = [("", "*")]
#         file_name2 = tk.filedialog.askopenfilename(
#             filetypes=fTyp, initialdir=INITIAL_DIR, initialfile=INITIAL_FILE2)
#         if len(file_name2) == 0:
#             self.file_name2.set('選択をキャンセルしました')
#         else:
#             self.file_name2.set(file_name2)
#         i.port_info = file_name2


# class Secondwindow:
#     def __init__(self, master: tk.Tk) -> None:

#         self.master = master
#         self.frame = tk.Frame(self.master)
#         self.quitButton = tk.Button(
#             self.frame,
#             text='Quit',
#             width=25,
#             command=self.close_windows)
#         self.quitButton.pack()
#         self.frame.pack()

#     def close_windows(self) -> None:
#         self.master.destroy()
#         root.quit()
#         root.destroy()


root = tk.Tk()
# root.title("window")
i = Div_Mgmt()

cls = windowclass(root, i)


root.mainloop()

print(f'{i.div_info=} {i.port_info=}')

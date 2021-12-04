"""
クラス構成はhttps://python-textbok.readthedocs.io/en/1.0/Introduction_to_GUI_Programming.htmlを参考にしている。

export DJA_UI='admin'
export DJA_PW='amincs8000'
export DJA_URL='http://127.0.0.1:8000/'
export PYTHONPATH='../:../api_client/:../client/'


"""
import tkinter as tk
# from tkinter import messagebox, ttk
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showinfo
import os
import sys
from bs import parser
from refs import DEFAULT_DIR, DEFAULT_FILE

from api_client.client_requests import client_requests
print(sys.path)
# DEFAULT_DIR = '/'

# create the root window


class GUI4Ticker():

    def __init__(self, root) -> None:

        self.DJA_UI = os.environ['DJA_UI']
        self.DJA_PW = os.environ['DJA_PW']
        self.DJA_URL = os.environ['DJA_URL']
        self.content_type = {'content-type': 'application/json'}

        self.app = 'tickers'
        self.ticker_requests = client_requests(
            self.DJA_UI,
            self.DJA_PW,
            self.DJA_URL,
            self.content_type,
            self.app)

        self.psr = parser()

        self.open_button = ttk.Button(
            root,
            text='Open Files',
            command=self.select_files
        )
        self.open_button.pack(expand=True)

        root.title('Tkinter File Dialog')
        # root.resizable(False, False)
        root.geometry('300x150+100+100')

    def select_files(self):
        filetypes = (
            # ('text files', '*.txt'),
            ('html files', '*.html'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open files',
            initialdir=DEFAULT_DIR,
            # initialfile="'" + DEFAULT_FILE + "'",
            initialfile=DEFAULT_FILE,
            filetypes=filetypes)

        showinfo(
            title='Selected Files',
            message=filename
        )

        print(f'{filename}')

        """ TODO: get portfolio """
        # get_portfolio()

        txt = self.prepare_result_display(filename)
        self.get_portfolio()
        self.get_and_put_content(filename, txt)

    """ TODO: needs to call client_requests """
    # def get_portfolio(self)

    def get_portfolio(self):
        # TODO: get portfolio information from django server by getdataall
        self.ticker_requests.getAllData()
        self.psr.portf = [
            'KHC',
            'VOD',
            'NUS',
            'LUMN',
            'XPER',
            'BLX',
            'DOW',
            'TFSL',
            'O',
            'HD',
            'QCOM',
            'UBSI',
            'PEP',
            'HRB']

    def get_and_put_content(self, filename, txt):

        print(f'portfolio set {self.psr.portf=}')
        for line in self.psr.read_and_filter_html(filename):
            # TODO: POST line
            txt.insert(tk.END, line + '\n')
            root.update_idletasks()

    def prepare_result_display(self, filename):
        """ root.geometryで外枠が作られ、その中にtk.Textのテキストエリアが作成される。
        その際、外枠の中でTextのオプションのheiht分テキストエリア用にスペースが確保
        される。heightを短くするとテキストエリアの下に余白が広がることになる。
        長くするとexitボタンが犠牲になる(表示されなくなる) """
        txt = tk.Text(root, height=22, width=200)
        # txt = tk.Text(root, width=200)
        lbl = tk.Label(root, text="配当情報")

        # message = filename + 'is selected to process.\n'

        exitb = tk.Button(root, text="Exit",
                          command=root.destroy)

        """ サイズ + 位置 """
        root.geometry('1000x500+100+100')

        self.open_button.pack_forget()
        lbl.pack()
        txt.pack()
        # exitb.pack(pady=2)
        exitb.pack()
        # for i in range(10):
        #     msg = str(i) + ' ' + message
        #     txt.insert(tk.END, msg)
        """ 画面を切り替える """
        root.update_idletasks()

        return txt


root = tk.Tk()
gui = GUI4Ticker(root)
root.mainloop()

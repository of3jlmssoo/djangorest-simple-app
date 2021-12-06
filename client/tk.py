"""
クラス構成はhttps://python-textbok.readthedocs.io/en/1.0/Introduction_to_GUI_Programming.htmlを参考にしている。

export DJA_UI='admin'
export DJA_PW='amincs8000'
export DJA_URL='http://127.0.0.1:8000/'
export PYTHONPATH='../:../api_client/:../client/'


"""
import logging
import os
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showinfo

from api_client.client_requests import client_requests

from bs import parser
from refs import DEFAULT_DIR, DEFAULT_FILE

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.propagate = False
# DEBUG INFO WARNIG ERROR CRTICAL
logger.setLevel(logging.DEBUG)
ch.setLevel(logging.DEBUG)
logger.disabled = False


class GUI4Ticker():

    def __init__(self, root) -> None:

        # djangoアクセスのための準備
        self.DJA_UI = os.environ['DJA_UI']
        self.DJA_PW = os.environ['DJA_PW']
        self.DJA_URL = os.environ['DJA_URL']
        self.content_type = {'content-type': 'application/json'}

        # REST　API準備
        self.app = 'tickers'
        self.ticker_requests = client_requests(
            self.DJA_UI,
            self.DJA_PW,
            self.DJA_URL,
            self.content_type,
            self.app)

        self.app = 'dividends'
        self.dividends_requests = client_requests(
            self.DJA_UI,
            self.DJA_PW,
            self.DJA_URL,
            self.content_type,
            self.app)

        # パーサー準備
        self.psr = parser()

        # 初期画面作成(参照URLのまま)
        # この先はself.select_files()に依存
        self.open_button = ttk.Button(root, text='Open Files', command=self.select_files)
        self.open_button.pack(expand=True)

        root.title('Tkinter File Dialog')
        # root.resizable(False, False)
        root.geometry('300x150+100+100')

    def select_files(self):

        # 参照URLの流れのまま
        filetypes = (
            # ('text files', '*.txt'),
            ('html files', '*.html'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open files',
            initialdir=DEFAULT_DIR,
            initialfile=DEFAULT_FILE,
            filetypes=filetypes)

        showinfo(
            title='Selected Files',
            message=filename
        )

        logger.debug(f'tk.select_files{filename=}')

        """ DONE: get portfolio """
        # 次の画面を準備
        txt = self.prepare_result_display(filename)
        # ポートフォリオ情報取得
        self.get_portfolio()
        # self.get_and_put_content経由でパーサーを呼び出す
        self.get_and_put_content(filename, txt)
        # 終了メッセージを表示
        txt.insert(tk.END, '   --- 今回は以上です --- ' + '\n')

    def get_portfolio(self):
        """ REST経由でポートフォリオ情報を取得の上パーサーのportfにセットする """
        # DONE: get portfolio information from django server by getdataall
        logger.debug(f'tk.get_portfolio. {self.ticker_requests.getAllData()=}')
        if (result := self.ticker_requests.getAllData()):
            portf = [t['ticker'] for t in result]
        else:
            print('tk.get_portfolio. No portfolio available...')

        logger.debug(f'tk.get_portfolio. {portf=}')
        self.psr.portf = portf
        # ['BLX', 'KHC', 'VOD', 'NUS', 'LUMN', 'XPER', 'DOW', 'TFSL', 'O', 'HD', 'QCOM', 'UBSI', 'PEP', 'HRB', 'MC']

    def get_and_put_content(self, filename, txt):
        """ ポートフォリオ銘柄でのフィルタリングはread_and_filter_html()に任せている """
        logger.debug(f'tk.get_and_put_contet. portfolio == {self.psr.portf=}')
        for line in self.psr.read_and_filter_html(filename):

            # 画面に表示
            txt.insert(tk.END, line + '\n')

            # postData
            line = line.replace(' ', '').split(',')
            logger.debug(
                f"tk.get_and_put_contet.  'ticker': {line[0]}, 'ex_date': {line[1]}, 'pay_date': {line[3]}, 'div_val': {line[2]}, 'div_rat': {line[4]}")
            # DONE: POST line
            self.dividends_requests.postData({
                'ticker': line[0],
                'ex_date': line[1],
                'pay_date': line[3],
                'div_val': line[2],
                'div_rat': line[4]
            })

            # 画面更新
            root.update_idletasks()

    def prepare_result_display(self, filename):
        """ root.geometryで外枠が作られ、その中にtk.Textのテキストエリアが作成される。
        その際、外枠の中でTextのオプションのheiht分テキストエリア用にスペースが確保
        される。heightを短くするとテキストエリアの下に余白が広がることになる。
        長くするとexitボタンが犠牲になる(表示されなくなる) """
        txt = tk.Text(root, height=22, width=200)
        lbl = tk.Label(root, text="配当情報")

        exitb = tk.Button(root, text="Exit",
                          command=root.destroy)

        """ サイズ + 位置 """
        root.geometry('1000x500+100+100')

        self.open_button.pack_forget()
        lbl.pack()
        txt.pack()
        exitb.pack()

        """ 画面を切り替える """
        root.update_idletasks()

        return txt


root = tk.Tk()
gui = GUI4Ticker(root)
root.mainloop()

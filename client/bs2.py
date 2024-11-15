"""refs.htmlはgitにアップロードしない。中身は以下.

    DEFAULT_DIR = '/dir/'
    DEFAULT_FILE = '配当情報のhtmlファイル名'
    portf = ['stock1ticker', 'stock2ticker'].


実行時の環境変数
export DJA_UI='admin'
export DJA_PW='amincs8000'
export DJA_URL='http://127.0.0.1:8000/'
export PYTHONPATH='../:../api_client/:../client/'

"""

from __future__ import annotations

import datetime
import logging
import re
from enum import Enum
from typing import Generator

# do not use from typing import Union
from bs4 import BeautifulSoup

"""
# from refs import DEFAULT_DIR, DEFAULT_FILE, portf
# from refs import DEFAULT_DIR, DEFAULT_FILE
"""

DEFAULT_DIR = "/home/hiroshisakuma/docs/"
DEFAULT_FILE = "Dividend Calendar - Investing.com.html"
DATA2_LENGTH = 4

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.propagate = False
# DEBUG INFO WARNIG ERROR CRTICAL
logger.setLevel(logging.INFO)
ch.setLevel(logging.DEBUG)
logger.disabled = False


DEFAULT_DATE = "Jan 01, 2000"


class R(Enum):
    ERROR1 = 1
    ERROR2 = 2
    ERROR3 = 3
    ERROR4 = 4
    ERROR5 = 5
    ERROR6 = 6
    ERROR7 = 7


# def check_ticker(ticker: str) -> Union[str, R]:
def check_ticker(ticker: str) -> str | R:
    """長さチェック."""
    if len(ticker) == 0:
        return R.ERROR1

    """ アンダーバーを除いたらアルファベットのみ """
    result = re.sub(r"_", "", ticker)
    if not result.isalnum():
        return R.ERROR2

    """ アルファベットを除いて長さが1(を含む)大きい """
    result = re.sub(r"[a-zA-Z]", "", result)
    if len(result) > 0:
        # do not use print(f"{R.ERROR3=} {result=}")
        logger.info("R.ERROR3=%s result=%s", R.ERROR3, result)
        return R.ERROR3

    # return ticker  # noqa: ERA001
    return ticker


# def check_date(date: str) -> Union[str, R]:
def check_date(date: str) -> str | R:
    """htmlファイルの日付フォーマットはJan 03, 2022."""
    logger.info("date=%s", date)
    month_short = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    data_list = date.split()

    if data_list[0] not in month_short:
        return R.ERROR1

    data_list[1] = data_list[1].replace(",", "")
    if data_list[1].isdecimal() is False:
        return R.ERROR2

    logger.info("data_list[2]=%s", data_list[2])
    if data_list[2].isdecimal() is False or len(data_list[2]) != DATA2_LENGTH:
        return R.ERROR3

    return date
    # pass


def check_val() -> None:
    pass


def check_data(ticker: str, exdate: str, divval: str, paydate: str, yieldratio: str) -> None:
    """check_data データフォーマットを確認.

    ticker: アルファベット大文字小文字、数字、アンダーバー
            最低1文字
    exdate: Month Date, Year。Oct 28, 2021 の12文字
            Month: 3文字    Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec
            Date: 2文字 数字のみ
            Year: 4文字 数字のみ
            "--" のケースあり
    divval: 5文字か1文字    x.xx% or "-"
    paydate: exdateと同じ。
    yieldratio: 5文字か1文字    x.xx% or "-"

    "--"の場合"Dec 31, 2222"に置き換える
    "-"の場合"0"に置き換える
    """
    # do not use format_error = 0

    """ ticker確認 """

    """ exdate確認 """
    """ paydate確認 """
    """ divval確認 """
    """ yieldratio確認 """


class Parser:
    def __init__(self) -> None:
        """ポートフォリオ情報の取得、self._portfへの設定はparserクラス利用者がsetterを使って行う."""
        self._portf = []

    @property
    def portf(self) -> list:
        return self._portf

    @portf.setter
    def portf(self, val: list) -> None:
        self._portf = val

    def read_and_filter_html(self, html_file: str) -> Generator[str]:
        soup = BeautifulSoup(open(html_file), "html.parser")

        for link in soup.find_all("td", "left noWrap"):
            """ ("td", "left noWrap")以外で配当情報以外を含めずに絞り込みができない(と判断)
                そのため、find_all("td", "left noWrap")した後にnext_を使ってフィールドを特定
                ticker : ティッカー                 テキストで保持
                exdate : 配当確定日(配当落ち日)     日付フォーマットに変換
                divval : 配当額(ドル)               floatに変換
                paydate : 配当支払日(現地)          日付フォーマットに変換
                yieldratio : 配当率                 floatに変換
            """
            ticker = link.next_element.next_element.next_element.next_element.next_element
            exdate = link.find_next_sibling("td").get_text()
            divval = link.find_next_sibling("td").find_next_sibling("td").get_text()
            paydate = (
                link.find_next_sibling("td")
                .find_next_sibling("td")
                .find_next_sibling("td")
                .find_next_sibling("td")
                .get_text()
            )
            yieldratio = (
                link.find_next_sibling("td")
                .find_next_sibling("td")
                .find_next_sibling("td")
                .find_next_sibling("td")
                .find_next_sibling("td")
                .get_text()
            )
            # do not use logger.debug(f"bs.read_and_filter_html. {ticker=}, {exdate=}, {divval=}, {paydate=}, {yieldratio=}")
            logger.debug(
                "bs.read_and_filter_html. ticker=%s, exdate=%s, divval=%s, paydate=%s, yieldratio=%s",
                ticker,
                exdate,
                divval,
                paydate,
                yieldratio,
            )

            """ 変換 """
            try:
                exdate = datetime.datetime.strptime(exdate, "%b %d, %Y").astimezone(datetime.timezone.utc)
            except ValueError:
                exdate = datetime.datetime.strptime(DEFAULT_DATE, "%b %d, %Y").astimezone(datetime.timezone.utc)

            try:
                paydate = datetime.datetime.strptime(paydate, "%b %d, %Y").astimezone(datetime.timezone.utc)
            except ValueError:
                paydate = datetime.datetime.strptime(DEFAULT_DATE, "%b %d, %Y").astimezone(datetime.timezone.utc)

            divval = float(divval)

            exdate = exdate.strftime("%Y-%m-%d")
            paydate = paydate.strftime("%Y-%m-%d")

            yieldratio = yieldratio.replace("%", "").replace("-", "0")

            """ yield """
            if ticker in self.portf:
                yield f"{ticker}, {exdate}, {divval}, {paydate}, {yieldratio}"


if __name__ == "__main__":
    """
    # print(check_ticker('abc'))
    # print(check_ticker(''))
    # print(check_ticker('ab_c'))

    # print(check_date('Mar 20, 2021'))
    # print(check_date('Ma 20, 2021'))
    # print(check_date('Mar 20s, 2021'))
    # print(check_date('Mar 20, a2021'))
    # print(check_date('Mar 20, 21'))
    """
    psr = Parser()
    psr.portf = [
        "KHC",
        "VOD",
        "NUS",
        "LUMN",
        "XPER",
        "BLX",
        "DOW",
        "TFSL",
        "O",
        "HD",
        "QCOM",
        "UBSI",
        "PEP",
        "HRB",
        "MKTX",
    ]

    for line in psr.read_and_filter_html(DEFAULT_DIR + DEFAULT_FILE):
        # do not use print(line)
        logger.info(line)

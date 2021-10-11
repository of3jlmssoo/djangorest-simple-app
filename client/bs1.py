import bs4
import requests
import csv  # モジュール"CSV"の呼び出し

# スクレイピング対象のhtmlファイルからsoupを作成
soup = bs4.BeautifulSoup(
    open('Dividend Calendar - Investing.com.html'),
    'html.parser')

# for link in soup.find_all("a", "bold"):
for link in soup.find_all("td", "left noWrap"):
    # print(link.get('href'))
    # print(link.next_element.next_element.next_element.next_element.next_element, end="")
    # print(" ")
    # print(link.find_next_sibling("td").get_text(), end="")
    # print(" ")
    # print(link.find_next_sibling("td").find_next_sibling("td").get_text())
    ticker = link.next_element.next_element.next_element.next_element.next_element
    exdate = link.find_next_sibling("td").get_text()
    divval = link.find_next_sibling("td").find_next_sibling("td").get_text()
    print(ticker, exdate, divval)


with open('./tickers.txt') as f:
    l = [s.strip() for s in f.readlines()]
print(l)
# <class '_io.TextIOWrapper'>


# for link in soup.find_all("td", "left noWrap"):
#     print(link.get('a'))

# print(soup.find_all("td", "left noWrap"))


# eth_bal = soup.find('td', text='left noWrap').find_next('td').text.strip()
# print(eth_bal)
# prints '0 Ether'

# tag_items = soup.select('td:soup-contains("left noWrap") ~ td')
# print([t.get_text(strip=True) for t in tag_items])

# links = soup.find_all('a')  # 全てのaタグ要素を取得

# csvlist = []  # 配列を作成

# for link in links:  # aタグのテキストデータを配列に格納
#     sample_txt = link.text
#     csvlist.append(sample_txt)
#     print(f'{sample_txt=}')

# # CSVファイルを開く。ファイルがない場合は新規作成
# f = open("output_sample.csv", "w")
# writecsv = csv.writer(f, lineterminator='\n')

# writecsv.writerow(csvlist)  # 出力

# f.close()  # CSVファイルを閉じる

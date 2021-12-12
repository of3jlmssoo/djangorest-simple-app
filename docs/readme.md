# 配当情報管理

ポートフォリオの銘柄で、指定期間内に ex-date を迎える銘柄をリストアップする。

## 全体像

<img width="3000" src="./outlinechart.drawio.svg">

## モジュール構成

<img width="3000" src="./modOverview.drawio.svg">

## 機能

入力 A : 事前に登録されたポートフォリオ情報
入力 B : ある期間に ex-Date をむかえる銘柄情報(保存された html ファイル)
入力 B から入力 A の銘柄を抜出し、その銘柄の配当情報(アウトプット)を画面に表示すると共に django に記録する

### tk.py
- tkinter で入力 B のファイルを指定する
- REAT API で django から入力 B のポートフォリオ情報を取得しフィルタリング
- アウトプットを tkinter で出力すると共に REST API で django に post

### bs.py
- Beautiful Soup で入力 B のファイルを解析

### client_request.py
- Python Requests で REST API

### check_ticker.py
- REST APIテストプログラム
### register_ticker
- tickerとvol(vol1/vol2)を登録
  
### resultenum.py
- 列挙値

### refs.py/refs.md
- 定数定義。アップロードせず。refs.mdに定義だけを記載
### ci.py
tkinterで画面に表示(行単位)の間隔を調整

## 機能要件

- html ファイルに保管された、ある期間の配当情報を抽出
- 保有銘柄だった場合画面に表示
- 画面表示をコピーできる
- 抽出された配当情報を django に記録

<!-- ## 流れ

1. 使用する機能を単体でコーディング
   - Beautiful Soup
     - 始めて使う。保存した html ファイルから必要な情報を抽出する
   - tkinter
     - 初めて使う。ファイル指定を GUI で行う
   - rest
     - 始めて使う。配当情報や銘柄情報を保管し、抽出
2. ドキュメント作成
3. インテグレーション -->

## 非機能要件

今の所無し

## epic

- ユーザーとして、保有銘柄の配当確定日を知りたい
- ユーザーとして、該当銘柄の前年実績をあわせて知りたい

## ユースケース

```plantuml
@startuml
left to right direction
actor "ユーザー" as user
rectangle {
usecase "銘柄ファイル登録(事前)" as UC1
usecase "htmlファイル指定" as UC2
usecase "結果確認" as UC3

}
user --> UC1
user --> UC2
user --> UC3
@enduml
```

<!-- ### モジュール

当初は以下の図の上半分を想定していたが、bs.py(read_html())を置き換えることを想定すると下図下半分が良いと判断。bs.py(read_html())は対象 HTML に大きく依存し、変更が必要になる可能性が高いためできるだけ余計なことはさせない。

<img width="3000" src="./modules.drawio.svg"> -->

## データベース

```plantuml
@startuml
entity "ティッカー" as ticker {
  * ティッカー [PK]
  --
  数量1
  数量2
  数量合計
  前年実績
  id
  owner
}
entity "配当" as dividend {
  * ティッカー [FK]
  --
  確定日
  支払日
  配当額
  配当率
  id
  owner
}
ticker -|{ dividend
' - --で並びが変わる
@enduml
```

### クラス

<!--
- private
# protected
~ package private
+ public
+ -->

```plantuml
@startuml
class GUI4Ticker  {
   +django関連
   +rest関連
   +rest api - tickers
   +rest api - dividends
   +parse関連
   +画面表示関連
   +select_files()
   +get_portfolio()
   +get_and_put_content()
   +prepare_result_display()
}
class ControlInterval {
  +前回の時刻
  +インターバル値
  +check_interval()
}
class client_requests {
  +django関連
  +rest api関連
  +deleteAllData()
  +deleteData()
  +postData()
  +patchData()
  +getIdOfTicker()
  +isThisTickerExist()
  +getAllData()
  +pop_id_from_POST_data()
  +pop_id_from_GET_data()
}
class parser {
   +ポートフォリオ
   +read_and_filter_html()
}
class RegisterTicker {
  +django関連
  +rest api関連
  +read_csv()
  +post_patch_ticker()

}

GUI4Ticker - ControlInterval
GUI4Ticker -- client_requests
RegisterTicker - client_requests
GUI4Ticker -- parser
@enduml
```

## 起動

django を起動した状態で、python tk.py

### 結果確認

1. 結果確認イメージ@1st ステージ

```
MSS 2021-10-18 3.1%
MC  2021-10-20 3.0%
```

2. 結果確認イメージ@2nd ステージ

```
MSS 2021-10-18 3.1%   |  昨年実績 10.2
MC  2021-10-20 3.0%   |  昨年実績 3.5
```

## 処理の流れ

<img width="3000" src="./activity2.drawio.svg">

<!-- #### GUI 呼出

#### ウィンドウ 1(ファイル指定)

#### ウィンドウ 2(パーサー呼出)

#### パーサー呼出

#### ファイル読込

#### 配当情報

#### 配当情報登録

#### 銘柄情報取得

#### 結果準備

#### ウィンドウ 2(結果表示)

## 1 -->

<!-- ```plantuml
@startuml
|メイン|
start
:GUI呼出;
|GUI|
:ウィンドウ1
(ファイル指定);
:ウィンドウ2
(パーサー呼出);

|x|
while (配当情報あり?)
  :配当情報読み込み;
  if ("保有銘柄") then
  else
    |as|
    :登録;
    |x|
    :結果準備;

  ' else
  endif
endwhile
:結果準備;
stop
@enduml
``` -->

<!-- ## エラー処理

配当ファイルが存在しない
銘柄ファイルが存在しない
レストでエラー
銘柄情報が登録されていない

## メモ

ポートフォリオファイル選択
配当ファイル選択
ポートフォリオファイル読込み
配当ファイル読込み
　配当情報取得(ジェネレーター)
　配当情報登録
　配当情報表示準備
該当配当情報表示

リコンサイル
銘柄バッチ登録
銘柄バックアップ
配当情報バックアップ -->

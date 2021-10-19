# 配当管理

## 流れ
1. 使用する機能を単体でコーディング
   - Beautiful Soup
   - tkinter
   - rest
2. ドキュメント作成
3. インテグレーション

## データベース
```plantuml
@startuml
entity "ティッカー" as ticker {
  * ティッカー [PK]
  --
  数量1
  数量2
  数量(1+2)
  前年実績
}
entity "配当" as dividend {
  * ティッカー [FK]
  --
  確定日
  支払日
  配当額
  配当率
}
ticker -|{ dividend
' - --で並びが変わる
@enduml
```

## ユースケース

```plantuml
@startuml
left to right direction
actor "ユーザー" as user
rectangle {
usecase "銘柄ファイル指定" as UC1
usecase "htmlファイル指定" as UC2
usecase "結果確認" as UC3
}
user --> UC1
user --> UC2
user --> UC3
@enduml
```

### クラス
- ウィンドウ
- 配当管理
- パーサー
- レストクライアント


```plantuml
@startuml 
class Window  {
   -field1 
   #field2 
   ~vmethod1() 
   +method2() 
} 
class DivMgmt {
   -field1 
   #field2 
   ~vmethod1() 
   +method2() 
} 
class Parser {
   -field1 
   #field2 
   ~vmethod1() 
   +method2() 
}
class RestClient {
   -field1 
   #field2 
   ~vmethod1() 
   +method2() 
} 

Window - DivMgmt
DivMgmt -- Parser
DivMgmt -- RestClient
@enduml
```

- [ ] ウィンドウインスタンスを呼び出す際、配当管理インスタンスを引数として渡す
- [ ] ウィンドウインスタンスは、配当ファイルセット、銘柄ファイルセット、配当処理の3メソッドを利用
- [ ] 配当管理はパーサーに配当ファイル名を渡して配当情報を受取る(get_div_info)
- [ ] 配当管理はレストクライアントのrecord_div_infoを利用する

## エラー処理
配当ファイルが存在しない
銘柄ファイルが存在しない
レストでエラー


### 結果確認

1. 結果確認イメージ@1st ステージ

```
MSS 2021-10-18 3.1%
MC  2021-10-20 3.0%
```

2. 結果確認イメージ@2nd ステージ

```
MSS 2021-10-18 3.1%   |  昨年実績 3.5%
MC  2021-10-20 3.0%   |  昨年実績 2.0%
```

## 処理の流れ
<img width="3000" src="./activity.drawio.svg">
<!-- 
```plantuml
@startuml
:htmlファイル指定 & 銘柄ファイル指定;
:フォーマットチェック;
note right
日付
配当額
end note
repeat
:配当情報登録;
:銘柄チェック;
repeat while (more data?)
:結果表示;
@enduml
``` -->
<!-- 
```plantuml
@startuml
|メイン|
start
:GUI呼出;
|GUI|
:ウィンドウ1
(ファイル指定);
:ウィンドウ2
(パーサー呼出);
|パーサー|

:配当情報取得;
if (保有銘柄？) then (yes)
|django|
:配当情報登録;
|パーサー|
:結果準備;
' repeat while (more data?)
|GUI|
:ウィンドウ2
(結果表示);

|メイン|
stop
@enduml
```

```plantuml
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

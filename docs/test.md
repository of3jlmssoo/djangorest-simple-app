## テスト

### ticker

| ticker | vol1  | vol2  | accum | total_vol | owner | result |
| :----: | :---: | :---: | :---: | --------- | ----- | ------ |
|   O    |   O   |   O   |   O   |           |       |        |
|   -    |   -   |   -   |   -   |           |       |        |
| ticker | vol1  | vol2  | accum | total_vol | owner | result |
|   O    |   -   |   -   |   -   |           |       |        |
|   O    |   O   |   -   |   -   |           |       |        |
|   O    |   -   |   O   |   -   |           |       |        |
|   O    |   -   |   -   |   O   |           |       |        |
|   O    |   O   |   O   |   -   |           |       |        |
|   O    |   O   |   -   |   O   |           |       |        |
|   O    |   -   |   O   |   O   |           |       |        |
| ticker | vol1  | vol2  | accum | total_vol | owner | result |
|   -    |   -   |   -   |   -   |           |       |        |
|   -    |   O   |   -   |   -   |           |       |        |
|   -    |   -   |   O   |   -   |           |       |        |
|   -    |   -   |   -   |   O   |           |       |        |
|   -    |   O   |   O   |   -   |           |       |        |
|   -    |   O   |   -   |   O   |           |       |        |
|   -    |   -   |   O   |   O   |           |       |        |
|   -    |   O   |   O   |   O   |           |       |        |

- 2つ(複数)登録
- 全query
- 1つずつquery
- 1つずつ削除
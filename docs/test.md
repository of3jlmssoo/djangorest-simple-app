## テスト

### ticker

|       | ticker | vol1  | vol2  | accum | total_vol | owner |
| :---: | :----: | :---: | :---: | :---: | --------- | ----- |
|   1   |   O    |   O   |   O   |   O   |           |       |
|   2   |   -    |   -   |   -   |   -   |           |       |
|       | ticker | vol1  | vol2  | accum | total_vol | owner |
|   3   |   O    |   -   |   -   |   -   |           |       |
|   4   |   O    |   O   |   -   |   -   |           |       |
|   5   |   O    |   -   |   O   |   -   |           |       |
|   6   |   O    |   -   |   -   |   O   |           |       |
|   7   |   O    |   O   |   O   |   -   |           |       |
|   8   |   O    |   O   |   -   |   O   |           |       |
|   9   |   O    |   -   |   O   |   O   |           |       |
|  10   | ticker | vol1  | vol2  | accum | total_vol | owner |
|  11   |   -    |   -   |   -   |   -   |           |       |
|  12   |   -    |   O   |   -   |   -   |           |       |
|  13   |   -    |   -   |   O   |   -   |           |       |
|  14   |   -    |   -   |   -   |   O   |           |       |
|  15   |   -    |   O   |   O   |   -   |           |       |
|  16   |   -    |   O   |   -   |   O   |           |       |
|  17   |   -    |   -   |   O   |   O   |           |       |
|  18   |   -    |   O   |   O   |   O   |           |       |

- 2つ(複数)登録
- 全query
- 1つずつquery
- 1つずつ削除
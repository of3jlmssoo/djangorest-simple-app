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

    ticker = models.CharField(
        max_length=10,
        blank=False,
        null=False,
        unique=True,
    )
    # default='someerror')
    vol1 = models.IntegerField(
        validators=[
            MinValueValidator(0)],
        blank=False,
        null=False,
        default=0
    )
    vol2 = models.IntegerField(validators=[MinValueValidator(0)],
                               blank=False,
                               null=False,
                               default=0)
    total_vol = models.IntegerField(validators=[MinValueValidator(0)],
                                    blank=False,
                                    null=False,
                                    default=0)
    accum = models.IntegerField(validators=[MinValueValidator(0)],
                                blank=False,
                                null=False,
                                default=0)

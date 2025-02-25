class CoordinateSystem:
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    @classmethod
    def index_to_symbols(cls, index: int) -> str:
        if index == 0:
            return 'A'
        symbol = cls.alphabet[index % len(cls.alphabet)]
        index = index // len(cls.alphabet)
        if index == 0:
            return symbol
        return symbol + cls.index_to_symbols(index)

    @classmethod
    def range_format(
            cls,
            start_row_index: int,
            end_row_index: int,
            start_column_index: int,
            end_column_index: int,
    ):
        start_cord = f'{cls.index_to_symbols(start_column_index)}{start_row_index}'
        end_cord = f'{cls.index_to_symbols(end_column_index)}{end_row_index}'
        return f'{start_cord}:{end_cord}'

    @classmethod
    def excretion_row_index(cls, ranges: str) -> int:
        coordinate = ranges.split(':')[1]
        while coordinate[0] in cls.alphabet:
            coordinate = coordinate[1:]
        return int(coordinate)

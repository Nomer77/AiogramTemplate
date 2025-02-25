import gspread
import json
from .coordinates import CoordinateSystem
from . import colors


class GWorker:
    def __init__(
            self,
            gclient: gspread.Client,
            spreadsheet_key: str,
            worksheet_id: int
    ):
        self.gclient = gclient
        self.spreadsheet = gclient.open_by_key(spreadsheet_key)
        self.worksheet = self.spreadsheet.get_worksheet_by_id(worksheet_id)

        self.last_index = self.worksheet.row_count
        self.last_value_index = len(self.worksheet.get_all_values())

        self.formats = []
        self.valueRanges = []
        self.valueAppend = []

    def pre_format_borders(
            self,
            start_row_index: int,
            end_row_index: int | None = None,
            start_column_index: int = 0,
            end_column_index: int = 6
    ) -> None:
        if end_row_index is None:
            end_row_index = start_row_index

        with open('Google/requests/borders.json', 'r') as file:
            cell_format = {
                'borders': json.load(file)
            }

        self.formats.append(
            {
                'range': CoordinateSystem.range_format(
                    start_row_index=start_row_index,
                    end_row_index=end_row_index,
                    start_column_index=start_column_index,
                    end_column_index=end_column_index
                ),
                'format': cell_format
            }
        )

    def pre_format_color(
            self,
            start_row_index: int,
            color: colors.Color,
            end_row_index: int | None = None,
            start_column_index: int = 0,
            end_column_index: int = 6,
    ) -> None:
        if end_row_index is None:
            end_row_index = start_row_index

        with open(f'Google/requests/colors/{str(color)}', 'r') as file:
            cell_format = json.load(file)

        self.formats.append(
            {
                'range': CoordinateSystem.range_format(
                    start_row_index=start_row_index,
                    end_row_index=end_row_index,
                    start_column_index=start_column_index,
                    end_column_index=end_column_index
                ),
                'format': cell_format
            }
        )

    def pre_value_range_row_update(
            self,
            values: list,
            index: int
    ) -> None:
        self.valueRanges.append(
            {
                'range': CoordinateSystem.range_format(
                    start_row_index=index,
                    end_row_index=index,
                    start_column_index=0,
                    end_column_index=len(values)
                ),
                'values': [values]
            }
        )

    def pre_value_range_cell_update(
            self,
            values: list,
            start_row_index: int,
            end_row_index: int,
            start_column_index: int,
            end_column_index: int
    ) -> None:
        self.valueRanges.append(
            {
                'range': CoordinateSystem.range_format(
                    start_row_index=start_row_index,
                    end_row_index=end_row_index,
                    start_column_index=start_column_index,
                    end_column_index=end_column_index
                ),
                'values': values
            }
        )

    def append_row(self, values: list) -> int:
        self.pre_value_range_row_update(
            values=values,
            index=self.last_value_index + 1
        )
        self.last_value_index += 1
        return self.last_value_index

    def add_row(self) -> int:
        self.worksheet.insert_row(
            values=(),
            index=self.last_index - 1
        )
        self.last_index += 1
        return self.last_index

    def run_pre_updates(self):
        upd1Res = {'replies': []}
        upd2Res = {'responses': []}
        try:
            if len(self.formats) > 0:
                upd1Res = self.worksheet.batch_format(self.formats)
            if len(self.valueRanges) > 0:
                upd2Res = self.worksheet.batch_update(self.valueRanges)

        finally:
            self.formats = []
            self.valueRanges = []
        return upd1Res['replies'], upd2Res['responses']

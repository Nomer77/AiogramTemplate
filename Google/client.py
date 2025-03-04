from .worker import GWorker
import gspread
import os


class GSheets:

    months = [
        'Январь', 'Февраль', 'Март', 'Апрель',
        'Май', 'Июнь', 'Июль', 'Август',
        'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
    ]

    def __init__(self, path_to_credentials: str):

        self.gclient = gspread.service_account(filename=path_to_credentials)

        self.common: GWorker = GWorker(
            gclient=self.gclient,
            spreadsheet_key=os.getenv("GOOGLE_COMMON_SPREADSHEET_KEY"),
            worksheet_id=int(os.getenv("GOOGLE_COMMON_WORKSHEET_ID"))
        )

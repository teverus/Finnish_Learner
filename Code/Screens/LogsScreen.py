from pathlib import Path

from Code.TeverusSDK.DataBase import DataBase
from Code.TeverusSDK.Screen import (
    Screen,
    SCREEN_WIDTH,
    GO_BACK_ACTION,
    THIRD_COLUMN as THIRD,
    ACTIONS_STUB,
)
from Code.TeverusSDK.Table import Table


class LogsScreen(Screen):
    def __init__(self):
        self.database = DataBase(Path("Files/Logs.db"))
        self.df = self.database.read_table()

        if len(self.df):
            df_rows = [list(list(self.df.loc[index])) for index in range(len(self.df))]
            rows = [" | ".join([c.center(THIRD) for c in df_row]) for df_row in df_rows]
        else:
            rows = ["No records so far..."]

        self.table = Table(
            table_title="Logs",
            rows=rows,
            rows_bottom_border="-",
            table_width=SCREEN_WIDTH,
            footer=[GO_BACK_ACTION],
        )

        super(LogsScreen, self).__init__(self.table, ACTIONS_STUB)

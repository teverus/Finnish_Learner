from pathlib import Path

from Code.TeverusSDK.DataBase import DataBase
from Code.TeverusSDK.Screen import (
    Screen,
    ACTIONS_STUB,
    SCREEN_WIDTH,
    GO_BACK_ACTION,
    HALF,
)
from Code.TeverusSDK.Table import Table


class BaseStatisticsScreen(Screen):
    def __init__(self, table_title, database_path, unit_name):
        self.database = DataBase(Path(database_path))
        self.dataframe = self.database.read_table()
        self.statistics = dict(self.dataframe.groupby(by="Score").size())

        self.rows = [
            f"{f'Tier [{key}] '.rjust(HALF)}-->{f' {str(value).rjust(3)} {unit_name}(s)'.ljust(HALF)}"
            for key, value in self.statistics.items()
        ]

        self.table = Table(
            table_title=table_title,
            rows=self.rows,
            rows_bottom_border="-",
            table_width=SCREEN_WIDTH,
            footer=[GO_BACK_ACTION],
        )

        super(BaseStatisticsScreen, self).__init__(self.table, ACTIONS_STUB)

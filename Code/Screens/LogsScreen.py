from pathlib import Path

from Code.TeverusSDK.DataBase import DataBase
from Code.TeverusSDK.Screen import (
    Screen,
    Action,
    SCREEN_WIDTH,
    GO_BACK_ACTION,
    do_nothing,
)
from Code.TeverusSDK.Table import Table


class LogsScreen(Screen):
    def __init__(self):
        self.database = DataBase(Path("Files/Logs.db"))
        self.df = self.database.read_table()

        if len(self.df):
            ...
        else:
            self.actions = [Action(name="No records so far...", function=do_nothing)]

        self.table = Table(
            table_title="Logs",
            rows=[action.name for action in self.actions],
            rows_bottom_border="-",
            table_width=SCREEN_WIDTH,
            footer=[GO_BACK_ACTION],
        )

        super(LogsScreen, self).__init__(self.table, self.actions)

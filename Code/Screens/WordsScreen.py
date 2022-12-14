from pathlib import Path

from Code.Modules.PracticeSingleUnit import PracticeSingleUnit
from Code.Screens.BasePracticeScreen import BasePracticeScreen
from Code.Screens.BaseStatisticsScreen import BaseStatisticsScreen
from Code.TeverusSDK.Screen import (
    Screen,
    SCREEN_WIDTH,
    Action,
    GO_BACK_ACTION,
)
from Code.TeverusSDK.Table import Table


class WordsScreen(Screen):
    def __init__(self):
        self.actions = [
            Action(
                name="Practice a single word",
                function=BasePracticeScreen,
                arguments={
                    "function": PracticeSingleUnit,
                    "unit_name": "word",
                    "database_base": Path("Files/Words.db"),
                    "exercise_name": "Single word practice",
                },
            ),
            Action(
                name="See statistics",
                function=BaseStatisticsScreen,
                arguments={
                    "table_title": "Words statistics",
                    "database_path": "Files/Words.db",
                },
            ),
        ]

        self.table = Table(
            table_title="Words",
            rows=[action.name for action in self.actions],
            rows_bottom_border="-",
            table_width=SCREEN_WIDTH,
            footer=[GO_BACK_ACTION],
        )

        super(WordsScreen, self).__init__(self.table, self.actions)

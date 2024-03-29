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


class PhrasesScreen(Screen):
    def __init__(self):
        self.actions = [
            Action(
                name="Practice phrases",
                function=BasePracticeScreen,
                arguments={
                    "function": PracticeSingleUnit,
                    "unit_name": "phrase",
                    "database_base": Path("Files/Phrases.db"),
                    "exercise_name": "Phrase practice",
                },
            ),
            Action(
                name="See statistics",
                function=BaseStatisticsScreen,
                arguments={
                    "table_title": "Phrases statistics",
                    "database_path": "Files/Phrases.db",
                    "unit_name": "phrase",
                },
            ),
        ]

        self.table = Table(
            table_title="Phrases",
            rows=[action.name for action in self.actions],
            rows_bottom_border="-",
            table_width=SCREEN_WIDTH,
            footer=[GO_BACK_ACTION],
        )

        super(PhrasesScreen, self).__init__(self.table, self.actions)

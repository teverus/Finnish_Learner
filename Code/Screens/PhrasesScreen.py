from pathlib import Path

from Code.Modules.PracticeSingleUnit import PracticeSingleUnit
from Code.Screens.BasePracticeScreen import BasePracticeScreen
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

from Code.Screens.PracticeWordSingleScreen import PracticeWordSingleScreen
from Code.TeverusSDK.Screen import (
    Screen,
    SCREEN_WIDTH,
    Action,
    do_nothing,
    GO_BACK_ACTION,
)
from Code.TeverusSDK.Table import Table


class WordsScreen(Screen):
    def __init__(self):
        self.actions = [
            Action(
                name="Practice a single word",
                function=PracticeWordSingleScreen,
            ),
            Action(
                name="Practice word combinations",
                function=do_nothing,
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

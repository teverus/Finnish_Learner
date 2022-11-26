from Code.Screens.PracticePhrasesScreen import PracticePhrasesScreen
from Code.TeverusSDK.Screen import (
    Screen,
    SCREEN_WIDTH,
    Action,
    do_nothing,
    GO_BACK_ACTION,
)
from Code.TeverusSDK.Table import Table


class PhrasesScreen(Screen):
    def __init__(self):
        self.actions = [
            Action(
                name="Practice phrases",
                function=PracticePhrasesScreen,
            ),
            Action(
                name="See all phrases",
                function=do_nothing,
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

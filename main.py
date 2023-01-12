from datetime import datetime

from Code.Screens.ExitScreen import ExitScreen
from Code.Screens.LogsScreen import LogsScreen
from Code.Screens.PhrasesScreen import PhrasesScreen
from Code.Screens.SettingsScreen import SettingsScreen
from Code.Screens.WordsScreen import WordsScreen
from Code.TeverusSDK.Screen import Screen, Action, SCREEN_WIDTH, Key
from Code.TeverusSDK.Table import Table


class WelcomeScreen(Screen):
    def __init__(self):
        self.start_time = datetime.now()

        self.actions = [
            Action(name="Words", function=WordsScreen),
            Action(name="Phrases", function=PhrasesScreen),
            Action(name="Logs", function=LogsScreen),
            Action(name="Settings", function=SettingsScreen),
        ]

        self.table = Table(
            table_title="Finnish Learner",
            rows=[action.name for action in self.actions],
            rows_bottom_border="-",
            table_width=SCREEN_WIDTH,
            footer=[
                Action(
                    name="[Q] Exit application",
                    function=ExitScreen,
                    arguments={"main": self},
                    go_back=True,
                    shortcut=[Key.Q, Key.Q_RU],
                )
            ],
        )

        super(WelcomeScreen, self).__init__(self.table, self.actions)


if __name__ == "__main__":
    WelcomeScreen()

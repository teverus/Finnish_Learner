from Code.Screens.PhrasesScreen import PhrasesScreen
from Code.Screens.SettingsScreen import SettingsScreen
from Code.Screens.WordsScreen import WordsScreen
from Code.TeverusSDK.Screen import Screen, Action, SCREEN_WIDTH
from Code.TeverusSDK.Table import Table


class WelcomeScreen(Screen):
    def __init__(self):
        self.actions = [
            Action(name="Words", function=WordsScreen),
            Action(name="Phrases", function=PhrasesScreen),
            Action(name="Settings", function=SettingsScreen),
        ]

        self.table = Table(
            table_title="Finnish Learner",
            rows=[action.name for action in self.actions],
            rows_bottom_border=False,
            table_width=SCREEN_WIDTH,
        )

        super(WelcomeScreen, self).__init__(self.table, self.actions)


if __name__ == "__main__":
    WelcomeScreen()

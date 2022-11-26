from pathlib import Path

from Code.Modules.ChangeSetting import ChangeSetting
from Code.TeverusSDK.ConfigTool import ConfigTool
from Code.TeverusSDK.Screen import (
    Screen,
    Action,
    SCREEN_WIDTH,
    GO_BACK_ACTION,
)
from Code.TeverusSDK.Table import Table


class SettingsScreen(Screen):
    def __init__(self):
        name = 0
        value = 1

        settings = ConfigTool(Path("config.ini")).get_settings()

        self.settings = [[key.capitalize(), value] for key, value in settings.items()]

        width_1 = max([len(setting[name]) for setting in self.settings])
        width_2 = max([len(setting[value]) for setting in self.settings])

        self.actions = [
            Action(
                name=setting[name],
                function=ChangeSetting,
                arguments={"name": setting[name], "main": self},
            )
            for setting in self.settings
        ]

        self.table = Table(
            table_title="Settings",
            rows=[
                f"{setting[name].center(width_1)} | {setting[value].ljust(width_2)}"
                for setting in self.settings
            ],
            rows_bottom_border="-",
            table_width=SCREEN_WIDTH,
            footer=[GO_BACK_ACTION],
        )

        super(SettingsScreen, self).__init__(self.table, self.actions)

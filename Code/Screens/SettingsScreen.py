from pathlib import Path

from Code.Modules.ChangeSetting import ChangeSetting
from Code.TeverusSDK.Screen import (
    Screen,
    Action,
    SCREEN_WIDTH,
    GO_BACK_ACTION,
    HALF,
)
from Code.TeverusSDK.Table import Table
from Code.TeverusSDK.YamlTool import YamlTool


class SettingsScreen(Screen):
    def __init__(self):
        # settings = ConfigTool(Path("config.ini")).get_settings()
        settings = YamlTool(Path("config.yaml")).get_settings()

        self.actions = [
            Action(
                name=setting,
                function=ChangeSetting,
                arguments={"name": setting, "main": self},
            )
            for setting in settings.keys()
        ]

        self.table = Table(
            table_title="Settings",
            rows=[
                [f"{k.capitalize().rjust(HALF)} | {str(v).ljust(HALF)}"]
                for k, v in settings.items()
            ],
            rows_bottom_border="-",
            rows_centered=False,
            table_width=SCREEN_WIDTH,
            footer=[GO_BACK_ACTION],
        )

        super(SettingsScreen, self).__init__(self.table, self.actions)

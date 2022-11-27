from pathlib import Path

import bext

from Code.TeverusSDK.ConfigTool import ConfigTool
from Code.TeverusSDK.Screen import show_message, HALF_COLUMN
from Code.TeverusSDK.Table import GREEN


class ChangeSetting:
    def __init__(self, name, main):
        self.name = name.capitalize()
        self.main = main
        self.user_input = None

        self.main.table.show_cursor = True
        self.main.table.print_table()

        self.get_user_input()
        self.update_settings()
        self.update_table()

    ####################################################################################
    #    PRIMARY ACTIONS                                                               #
    ####################################################################################

    def get_user_input(self):
        self.user_input = input(f' New value for "{self.name}"\n >>> ')
        bext.hide()
        show_message(("Success", GREEN), upper=False)

    def update_settings(self):
        ConfigTool(Path("config.ini")).update_a_setting(self.name, self.user_input)

    def update_table(self):
        rows = self.main.table.rows
        target_row = [[i, row] for i, row in enumerate(rows) if self.name in row[0]][0]
        target_index = target_row[0]
        target_line = target_row[1][0]
        name, _ = [e.strip() for e in target_line.split("|")]
        new_line = f"{name.capitalize().rjust(HALF_COLUMN)} | {self.user_input.ljust(HALF_COLUMN)}"
        self.main.table.rows[target_index][0] = new_line

        self.main.table.show_cursor = False

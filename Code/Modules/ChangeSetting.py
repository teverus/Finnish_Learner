from pathlib import Path

import bext

from Code.TeverusSDK.Screen import show_message, HALF
from Code.TeverusSDK.Table import GREEN
from Code.TeverusSDK.YamlTool import YamlTool


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
        user_input = input(f' New value for "{self.name}"\n >>> ').lower()
        user_input = int(user_input) if user_input.isdigit() else user_input
        user_input = True if user_input == "true" else user_input
        user_input = False if user_input == "false" else user_input

        self.user_input = user_input
        bext.hide()
        show_message(("Success", GREEN), upper=False)

    def update_settings(self):
        YamlTool(Path("config.yaml")).update_a_setting(self.name, self.user_input)

    def update_table(self):
        rows = self.main.table.rows
        target_row = [[i, row] for i, row in enumerate(rows) if self.name in row[0]][0]
        target_index = target_row[0]
        target_line = target_row[1][0]
        name, _ = [e.strip() for e in target_line.split("|")]
        line = f"{name.capitalize().rjust(HALF)} | {str(self.user_input).ljust(HALF)}"
        self.main.table.rows[target_index][0] = line

        self.main.table.show_cursor = False

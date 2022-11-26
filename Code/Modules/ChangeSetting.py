from pathlib import Path

import bext

from Code.TeverusSDK.ConfigTool import ConfigTool
from Code.TeverusSDK.Screen import show_message
from Code.TeverusSDK.Table import GREEN


class ChangeSetting:
    def __init__(self, name, main):
        self.name = name
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
        # TODO X        Нужно подстраховать ширину, если изменилась ширина числа

        rows = self.main.table.rows
        target_row = [[i, row] for i, row in enumerate(rows) if self.name in row[0]][0]
        target_index = target_row[0]
        target_line = target_row[1][0]
        current_number = target_line.split("|")[-1].strip()
        new_line = rows[target_index][0].replace(current_number, self.user_input)
        self.main.table.rows[target_index][0] = new_line

        self.main.table.show_cursor = False

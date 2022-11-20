from pathlib import Path

import bext

from Code.TeverusSDK.DataBase import DataBase
from Code.TeverusSDK.Screen import SCREEN_WIDTH, show_message, wait_for_enter

PASS = "PASS"
FAIL = "FAIL"
DONE = "DONE"


class PracticeSingleWord:
    def __init__(self, main):
        self.statistics = {PASS: 0, FAIL: 0, DONE: 0}

        self.total_words = 2

        self.column_width = int((SCREEN_WIDTH - 3 - 2) / 2)
        self.database = DataBase(Path("Files/Words.db"))
        self.df = self.database.read_table()

        # TODO XXX      Брать случайно в группе по Score
        for index in range(len(self.df)):
            if index:
                self.update_table(main)
                main.table.print_table()

            finnish = self.df.loc[index, "Finnish"]
            english = self.df.loc[index, "English"]

            user_input = self.get_input(f" {english.center(self.column_width)} | >>> ")

            if user_input == finnish:
                # TODO XXXX     Брать delta из настроек
                delta = 1
                message = "Success :)"
                self.statistics[PASS] += 1

            else:
                # TODO XXXX     Брать delta из настроек
                delta = -2
                message = f"""Sorry, it's '{finnish}', not '{user_input}'"""
                self.statistics[FAIL] += 1

            self.df.loc[index, "Score"] += delta
            # self.database.write_to_table(self.df)
            self.statistics[DONE] += 1

            confirmation = True if delta > 0 else False
            [bext.show if not confirmation else bext.hide][0]()
            show_message(message, upper=False, need_confirmation=confirmation)

            if delta < 0:
                correct = 0
                # TODO XXXX     Брать correct_answers из настроек
                need_correct = 3
                while correct != need_correct:
                    times_left = need_correct - correct
                    plural = "s" if times_left > 1 else ""
                    msg = f'\nPlease type "{finnish}" {times_left} time{plural}\n>>> '
                    new_input = self.get_input(msg)
                    if new_input == finnish:
                        correct += 1
                    else:
                        msg = f'Sorry, you need to type "{finnish}"'
                        show_message(msg, upper=False, need_confirmation=False)
                bext.hide()
                show_message("Success :)", upper=False)

        self.update_table(main)
        main.table.table_title = "Results"
        main.table.show_cursor = False
        main.table.print_table()

        if self.statistics[FAIL]:
            # TODO XX       Показывать ошибки если они были
            ...

        wait_for_enter()

    ####################################################################################
    #    HELPERS                                                                       #
    ####################################################################################
    def update_table(self, main):
        CHARS = ["O", "X", "I"]
        TICKS = 1
        PERCENTAGE = 2

        current_pass = int(self.statistics[PASS] / self.statistics[DONE] * 100)
        current_fail = int(self.statistics[FAIL] / self.statistics[DONE] * 100)
        current_done = int(self.statistics[DONE] / self.total_words * 100)
        stats = [current_pass, current_fail, current_done]

        for row, stat, char in zip(main.table.rows, stats, CHARS):
            result = f"{char * stat}{'-' * (100 - stat)}"
            row[TICKS] = result
            row[PERCENTAGE] = f"{str(stat).rjust(3)} %"

    @staticmethod
    def get_input(message):
        user_input = input(message)
        user_input = user_input.strip().replace("a:", "ä").replace("o:", "ö")

        return user_input

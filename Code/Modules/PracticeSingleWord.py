from pathlib import Path

from Code.TeverusSDK.DataBase import DataBase
from Code.TeverusSDK.Screen import SCREEN_WIDTH, show_message, wait_for_enter

PASS = "PASS"
FAIL = "FAIL"
DONE = "DONE"
CHARS = ["O", "X", "I"]
TICKS = 1
PERCENTAGE = 2


# TODO 1    Написать три раза
# TODO 2    Показывать ошибки если они были
# TODO 3    Брать delta из настроек
# TODO 4    Брать случайно в группе по Score


class PracticeSingleWord:
    def __init__(self, main):
        self.statistics = {PASS: 0, FAIL: 0, DONE: 0}

        self.total_words = 2

        self.column_width = int((SCREEN_WIDTH - 3 - 2) / 2)
        self.database = DataBase(Path("Files/Words.db"))
        self.df = self.database.read_table()

        for index in range(len(self.df)):
            if index:
                self.update_table(main)
                main.table.print_table()

            finnish = self.df.loc[index, "Finnish"]
            english = self.df.loc[index, "English"]

            user_input = input(f" {english.center(self.column_width)} | >>> ")
            user_input = user_input.strip().replace("a:", "ä").replace("o:", "ö")

            if user_input == finnish:
                delta = 1
                message = "Pass"
                self.statistics[PASS] += 1

            else:
                delta = -2
                message = "Fail"
                self.statistics[FAIL] += 1

            self.statistics[DONE] += 1

            self.df.loc[index, "Score"] += delta
            # self.database.write_to_table(self.df)
            show_message(message)

        self.update_table(main)
        main.table.table_title = "Results"
        main.table.print_table()
        if self.statistics[FAIL]:
            ...

        wait_for_enter()

    ####################################################################################
    #    HELPERS                                                                       #
    ####################################################################################
    def update_table(self, main):
        current_pass = int(self.statistics[PASS] / self.statistics[DONE] * 100)
        current_fail = int(self.statistics[FAIL] / self.statistics[DONE] * 100)
        current_done = int(self.statistics[DONE] / self.total_words * 100)
        stats = [current_pass, current_fail, current_done]

        for row, stat, char in zip(main.table.rows, stats, CHARS):
            result = f"{char * stat}{'-' * (100 - stat)}"
            row[TICKS] = result
            row[PERCENTAGE] = f"{str(stat).rjust(3)} %"

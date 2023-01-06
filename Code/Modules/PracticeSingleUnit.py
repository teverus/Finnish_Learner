import random
from copy import copy
from datetime import datetime
from pathlib import Path

import bext

from Code.TeverusSDK.DataBase import DataBase
from Code.TeverusSDK.Screen import (
    SCREEN_WIDTH,
    show_message,
    wait_for_enter,
    HALF,
)
from Code.TeverusSDK.Table import RED, END_HIGHLIGHT, GREEN, Table
from Code.TeverusSDK.YamlTool import YamlTool

PASS = "PASS"
FAIL = "FAIL"
DONE = "DONE"
ARROW_UP = "↑"
ARROW_DOWN = "↓"
WALL = 3
SIDE_PADDING = 2


class Unit:
    def __init__(self, finnish, english, tier, index):
        self.finnish = finnish
        self.english = english
        self.tier = tier
        self.index = index
        self.delta = 0
        self.wrong_answer = ""


class PracticeSingleUnit:
    def __init__(self, main):
        # === Variables ================================================================

        self.start_time = datetime.now()
        self.time_elapsed = None
        self.unit_name = main.unit_name.upper()
        self.statistics = {PASS: 0, FAIL: 0, DONE: 0}
        self.message = None
        self.user_input = None
        self.known_scores = None
        self.words_for_this_run = None
        self.used_words = []

        self.unit = None
        self.units_done = []

        self.settings = YamlTool(Path("config.yaml")).get_settings()
        self.total_words = self.settings[Settings.WORDS_PER_RUN]

        self.database = DataBase(main.database_path)
        self.df = self.database.read_table()

        self.get_words_for_this_run()

        # === Main loop ================================================================

        for _ in range(self.total_words):

            self.get_random_word()

            self.update_table(main)
            main.table.print_table()

            self.ask_user_to_type_the_finnish_word()
            if self.user_input == "q":
                break
            self.evaluate_answer()
            self.record_result_to_database_and_statistics()
            self.show_message_after_input()
            self.practice_the_word_if_needed()

        # === Finish ===================================================================

        self.record_activity_to_logs(main)
        self.show_results_table(main)

        wait_for_enter()

    ####################################################################################
    #    HELPERS                                                                       #
    ####################################################################################
    def update_table(self, main):
        CHARS = [
            f"{GREEN} {END_HIGHLIGHT}",
            f"{RED} {END_HIGHLIGHT}",
            "#",
        ]
        TICKS = 1
        PERCENTAGE = 2

        safe_statistics = 1 if not self.statistics[DONE] else self.statistics[DONE]
        current_pass = int(self.statistics[PASS] / safe_statistics * 100)
        current_fail = int(self.statistics[FAIL] / safe_statistics * 100)
        if (current_pass and current_fail) and current_pass + current_fail != 100:
            current_pass += 1
        current_done = int(self.statistics[DONE] / self.total_words * 100)
        stats = [current_pass, current_fail, current_done]

        for row, stat, char in zip(main.table.rows, stats, CHARS):
            result = f"{char * stat}{'-' * (100 - stat)}"
            row[TICKS] = result
            row[PERCENTAGE] = f"{str(stat).rjust(3)} %"

        done = self.statistics[DONE] + 1
        words = f"{self.unit_name} [{done:02}/{self.total_words:02}]"

        tier = f"TIER [{self.unit.tier}]"

        left = self.total_words - done
        left_units = f"LEFT [{left}]"

        elapsed = str(datetime.now() - self.start_time)
        time_elapsed = f'TIME [{elapsed.split(".")[0][2:]}]'

        left_part = f"{words} | {tier}".rjust(HALF)
        right_part = f"{left_units} | {time_elapsed}".ljust(HALF)
        main.table.table_title = f"{left_part} | {right_part}"

    @staticmethod
    def get_input(message):
        user_input = input(message)
        user_input = user_input.strip().replace("a:", "ä").replace("o:", "ö")

        return user_input

    def evaluate_answer(self):
        if self.user_input == self.unit.finnish:
            self.unit.delta = self.settings[Settings.POSITIVE_CHANGE]
            self.statistics[PASS] += 1
            self.message = ("Success :)", GREEN)

        else:
            self.unit.delta = self.settings[Settings.NEGATIVE_CHANGE]
            self.statistics[FAIL] += 1
            not_part = "" if not self.user_input else f', not "{self.user_input}"'
            wrong = f"""Sorry, it's "{self.unit.finnish}"{not_part}"""
            self.message = (wrong, RED)
            self.unit.wrong_answer = "?" if not self.user_input else self.user_input

        self.units_done.append(copy(self.unit))

    def show_results_table(self, main):
        self.update_results_table_head(main)
        self.show_results()

    def update_results_table_head(self, main):
        self.update_table(main)
        finish_time = datetime.now()
        self.time_elapsed = str(finish_time - self.start_time).split(".")[0]
        main.table.table_title = f"Results [{self.time_elapsed}]"
        main.table.show_cursor = False
        main.table.print_table()

    def show_results(self):
        if not self.units_done:
            return

        rows = [
            [
                unit.english,
                f"{unit.tier: 2} => {(unit.tier + unit.delta): 2} {ARROW_UP if unit.delta > 0 else ARROW_DOWN}",
                unit.finnish,
                unit.wrong_answer,
            ]
            for unit in self.units_done
        ]

        Table(
            rows=rows,
            rows_top_border=False,
            clear_console=False,
            highlight=False,
            table_width=SCREEN_WIDTH,
            headers=["English", "Change", "Finnish", "Incorrect"]
            # column_widths={
            #     0: ColumnWidth.FULL,
            #     1: ColumnWidth.FIT,
            #     2: ColumnWidth.FULL,
            #     3: ColumnWidth.FIT,
            # }
        ).print_table()
        # widths = {i: max([len(r[i]) for r in rows]) for i in range(len(rows[0]))}
        # rows_fixed = [[e.center(widths[i]) for i, e in enumerate(r)] for r in rows]
        # length_taken = sum(widths.values()) + ((len(widths) - 1) * WALL) + SIDE_PADDING
        # length_available = SCREEN_WIDTH - length_taken
        # front = False
        # while length_available:
        #     for ind_col in [0, 2, 3]:
        #         if length_available:
        #             for r in rows_fixed:
        #                 r[ind_col] = f" {r[ind_col]}" if front else f"{r[ind_col]} "
        #             length_available -= 1
        #     front = not front
        #
        # widths_ = {i: max([len(r[i]) for r in rows_fixed]) for i in range(len(rows[0]))}
        # names = ["English", "Change", "Finnish", "Incorrect"]
        # headers = [name.center(widths_[i]).upper() for i, name in enumerate(names)]
        # delimiter = [f"{'-' * width}" for width in widths_.values()]
        #
        # print(f" {' | '.join(headers)} ")
        # print(f"-{'-+-'.join(delimiter)}-")
        #
        # rows_fixed_line = [" | ".join(row) for row in rows_fixed]
        # rows_fixes_color = [
        #     [f"{GREEN if ARROW_UP in row else RED}{row}{END_HIGHLIGHT}"]
        #     for row in rows_fixed_line
        # ]
        #
        # Table(
        #     rows=rows_fixes_color,
        #     rows_top_border=False,
        #     clear_console=False,
        #     highlight=False,
        #     table_width=SCREEN_WIDTH,
        # ).print_table()

    def practice_the_word_if_needed(self):
        if self.unit.delta < 0:
            correct = 0
            need_correct = self.settings[Settings.NEED_CORRECT]
            while correct != need_correct:
                left = need_correct - correct
                plur = "s" if left > 1 else ""
                msg = f'\nPlease type "{self.unit.finnish}" {left} time{plur}\n>>> '
                new_input = self.get_input(msg)
                if new_input == self.unit.finnish:
                    correct += 1
                else:
                    msg = (f'Sorry, you need to type "{self.unit.finnish}"', RED)
                    show_message(msg, upper=False, need_confirmation=False)
            bext.hide()
            show_message(("Success :)", GREEN), upper=False)

    def ask_user_to_type_the_finnish_word(self):
        change = '"a:" -> "ä", "o:" -> "ö"'.rjust(HALF)
        type_to_exit = '"q" + Enter -> quit'.ljust(HALF)
        print(f"{change} | {type_to_exit}".center(SCREEN_WIDTH))
        print(f"-{'-' * HALF}-+-{'-' * HALF}-")
        prompt = f" {self.unit.english.center(HALF)} | >>> "
        user_input = input(prompt)
        user_input = user_input.strip().replace("a:", "ä").replace("o:", "ö")

        self.user_input = user_input

    def show_message_after_input(self):
        confirmation = True if self.unit.delta > 0 else False
        [bext.show if not confirmation else bext.hide][0]()
        show_message(self.message, upper=False, need_confirmation=confirmation)

    def record_result_to_database_and_statistics(self):
        self.df.loc[self.unit.index, "Score"] += self.unit.delta
        self.df.sort_values(by="Score", inplace=True)

        if self.settings[Settings.RECORD_ANSWERS]:
            self.database.write_to_table(self.df)

        self.statistics[DONE] += 1

    def get_words_for_this_run(self):
        self.df.sort_values(by="Score", inplace=True)
        self.df.reset_index(drop=True, inplace=True)
        self.words_for_this_run = self.df.loc[0 : self.total_words - 1]
        self.known_scores = sorted(set(self.words_for_this_run.Score.values))

    def get_random_word(self):
        for score in self.known_scores:
            words = self.words_for_this_run.loc[self.words_for_this_run.Score == score]
            english_words = list(words.English)
            proper_words = [w for w in english_words if w not in self.used_words]

            if len(proper_words):
                random_word = random.choice(proper_words)
                self.used_words.append(random_word)

                word = self.df.loc[self.df.English == random_word]
                self.unit = Unit(
                    finnish=word.Finnish.values[0],
                    english=word.English.values[0],
                    tier=word.Score.values[0],
                    index=word.index.values[0],
                )
                break

    def record_activity_to_logs(self, main):
        logs_database = DataBase(Path("Files/Logs.db"))
        logs_df = logs_database.read_table()
        date = datetime.today().strftime("%d %B %Y")
        logs_df.loc[len(logs_df)] = [date, main.exercise_name, self.time_elapsed]
        logs_database.write_to_table(logs_df)


########################################################################################
#    SETTINGS                                                                          #
########################################################################################


class Settings:
    WORDS_PER_RUN = "Words per run"
    POSITIVE_CHANGE = "Positive change"
    NEGATIVE_CHANGE = "Negative change"
    NEED_CORRECT = "How many times practice a word with an error"
    RECORD_ANSWERS = "Record answers to database"

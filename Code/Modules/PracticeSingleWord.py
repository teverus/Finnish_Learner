import random
from pathlib import Path

import bext

from Code.TeverusSDK.DataBase import DataBase
from Code.TeverusSDK.Screen import SCREEN_WIDTH, show_message, wait_for_enter
from Code.TeverusSDK.Table import Table

PASS = "PASS"
FAIL = "FAIL"
DONE = "DONE"

# TODO X        Показывать столько осталось


class PracticeSingleWord:
    def __init__(self, main):
        self.statistics = {PASS: 0, FAIL: 0, DONE: 0}
        self.wrong_answers = {}
        self.delta = 0
        self.message = None
        self.user_input = None
        self.known_scores = None
        self.words_for_this_run = None
        self.used_words = []

        self.finnish = None
        self.english = None
        self.word_index = None

        # TODO XXXX     Брать total_words из настроек
        self.total_words = 10

        self.column_width = int((SCREEN_WIDTH - 3 - 2) / 2)
        self.database = DataBase(Path("Files/Words.db"))
        self.df = self.database.read_table()

        self.get_words_for_this_run()

        for _ in range(self.total_words):
            if _:
                self.update_table(main)
                main.table.print_table()

            self.get_random_word()

            self.ask_user_to_type_the_finnish_word()
            self.evaluate_answer()
            self.record_result_to_database_and_statistics()
            self.show_message_after_input()
            self.practice_the_word_if_needed()

        self.show_results_table(main)
        self.show_wrong_answers_if_any()

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

    def evaluate_answer(self):
        if self.user_input == self.finnish:
            # TODO XXXX     Брать delta из настроек
            self.delta = 1
            self.message = "Success :)"
            self.statistics[PASS] += 1

        else:
            # TODO XXXX     Брать delta из настроек
            self.delta = -2
            wrong = f"""Sorry, it's '{self.finnish}', not '{self.user_input}'"""
            self.message = wrong
            self.statistics[FAIL] += 1
            # TODO X        Показывать перевод слова
            self.wrong_answers[self.finnish] = self.user_input

    def show_results_table(self, main):
        self.update_table(main)
        main.table.table_title = "Results"
        main.table.show_cursor = False
        main.table.print_table()

    def show_wrong_answers_if_any(self):
        if self.wrong_answers:
            answers = [[right, wrong] for right, wrong in self.wrong_answers.items()]
            width = self.column_width
            columns = f"{'CORRECT'.center(width)} | {'INCORRECT'.center(width)}"
            wrong_table = Table(
                table_title=f" {columns} ",
                table_title_top_border=False,
                rows=answers,
                rows_top_border="-",
                table_width=SCREEN_WIDTH,
                clear_console=False,
            )
            wrong_table.print_table()

    def practice_the_word_if_needed(self):
        if self.delta < 0:
            correct = 0
            # TODO XXXX     Брать correct_answers из настроек
            need_correct = 3
            while correct != need_correct:
                times_left = need_correct - correct
                plural = "s" if times_left > 1 else ""
                msg = f'\nPlease type "{self.finnish}" {times_left} time{plural}\n>>> '
                new_input = self.get_input(msg)
                if new_input == self.finnish:
                    correct += 1
                else:
                    msg = f'Sorry, you need to type "{self.finnish}"'
                    show_message(msg, upper=False, need_confirmation=False)
            bext.hide()
            show_message("Success :)", upper=False)

    def ask_user_to_type_the_finnish_word(self):
        prompt = f" {self.english.center(self.column_width)} | >>> "
        user_input = input(prompt)
        user_input = user_input.strip().replace("a:", "ä").replace("o:", "ö")

        self.user_input = user_input

    def show_message_after_input(self):
        confirmation = True if self.delta > 0 else False
        [bext.show if not confirmation else bext.hide][0]()
        show_message(self.message, upper=False, need_confirmation=confirmation)

    def record_result_to_database_and_statistics(self):
        self.df.loc[self.word_index, "Score"] += self.delta
        # self.database.write_to_table(self.df)  # TODO вернуть
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
                word = self.df.loc[self.df.English == random_word]

                self.finnish = word.Finnish.values[0]
                self.english = word.English.values[0]
                self.word_index = word.index.values[0]
                self.used_words.append(random_word)

                break

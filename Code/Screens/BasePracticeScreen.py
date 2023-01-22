from pathlib import Path

from Code.TeverusSDK.Screen import Screen, Action, SCREEN_WIDTH
from Code.TeverusSDK.Table import Table, ColumnWidth


class BasePracticeScreen(Screen):
    def __init__(self, function, unit_name, database_base: Path, exercise_name):
        self.unit_name = unit_name
        self.database_path = database_base
        self.exercise_name = exercise_name

        self.actions = [
            Action(
                name="",
                function=function,
                arguments={"main": self},
                immediate_action=True,
                go_back=True,
            )
        ]

        self.table = Table(
            table_title=" ",
            rows=[
                ["        PASS", f"{'-' * 100}", "  0 %"],
                ["        FAIL", f"{'-' * 100}", "  0 %"],
                ["        DONE", f"{'-' * 100}", "  0 %"],
            ],
            rows_centered=False,
            column_widths={0: ColumnWidth.FIT, 1: ColumnWidth.FIT, 2: ColumnWidth.FIT},
            highlight=False,
            show_cursor=True,
            table_width=SCREEN_WIDTH,
        )

        super(BasePracticeScreen, self).__init__(self.table, self.actions)

from Code.Modules.PracticeSingleWord import PracticeSingleWord
from Code.TeverusSDK.Screen import Screen, Action
from Code.TeverusSDK.Table import Table, ColumnWidth


class PracticeSingleWordScreen(Screen):
    def __init__(self):
        self.actions = [
            Action(
                name="",
                function=PracticeSingleWord,
                arguments={"main": self},
                immediate_action=True,
                go_back=True,
            )
        ]

        self.table = Table(
            table_title="Practice a single word",
            rows=[
                ["PASS", f"{'-' * 100}", "  0 %"],
                ["FAIL", f"{'-' * 100}", "  0 %"],
                ["DONE", f"{'-' * 100}", "  0 %"],
            ],
            column_widths={0: ColumnWidth.FIT, 1: ColumnWidth.FIT, 2: ColumnWidth.FIT},
            highlight=False,
            show_cursor=True,
        )

        super(PracticeSingleWordScreen, self).__init__(self.table, self.actions)

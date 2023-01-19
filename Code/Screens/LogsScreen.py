from datetime import datetime, timedelta
from pathlib import Path

from Code.TeverusSDK.DataBase import DataBase
from Code.TeverusSDK.Screen import (
    Screen,
    SCREEN_WIDTH,
    GO_BACK_ACTION,
    ACTIONS_STUB,
    THIRD,
)
from Code.TeverusSDK.Table import Table


class LogsScreen(Screen):
    def __init__(self):
        self.max_rows = 36

        self.database = DataBase(Path("Files/Logs.db"))
        self.df = self.database.read_table()

        rows = self.get_records() if len(self.df) else ["No records so far..."]

        self.table = Table(
            table_title="Logs",
            rows=rows,
            max_rows=self.max_rows,
            rows_bottom_border="-",
            table_width=SCREEN_WIDTH,
            footer=[GO_BACK_ACTION],
            highlight=False,
        )

        super(LogsScreen, self).__init__(self.table, ACTIONS_STUB)

    def get_records(self):
        df_rows = [list(list(self.df.loc[index])) for index in range(len(self.df))]
        logs = self.get_logs_as_dict(df_rows)
        unique_dates = self.get_unique_dates(df_rows)
        total_day_time = self.get_total_day_times(unique_dates, df_rows)
        rows = self.get_rows(logs, unique_dates, total_day_time)

        return rows

    @staticmethod
    def get_logs_as_dict(df_rows):
        logs = {}
        for row in df_rows:
            date = row[0]
            if date not in logs.keys():
                logs[date] = []
            logs[date].append(row)

        return logs

    @staticmethod
    def get_unique_dates(df_rows):
        unique_dates = []
        for recorded_date in [r[0] for r in df_rows]:
            if recorded_date not in unique_dates:
                unique_dates.append(recorded_date)

        return unique_dates

    @staticmethod
    def get_total_day_times(unique_dates, df_rows):
        total_day_time = {}
        UNIX_START = datetime(1970, 1, 1)
        for date in unique_dates:
            total = timedelta()
            for row in df_rows:
                if date in row:
                    total += datetime.strptime(row[2], "%H:%M:%S") - UNIX_START
            total_day_time[date] = str(total).split(", ")[-1]

        return total_day_time

    def get_rows(self, logs, unique_dates, total_day_time):
        unique_dates.reverse()

        rows = []
        SEE_NEXT_PAGE = " MORE ON THE NEXT PAGE ".center(SCREEN_WIDTH - 2, ">")
        # SEE_PREV_PAGE = " MORE ON THE PREVIOUS PAGE ".center(SCREEN_WIDTH - 2, "-")

        for unique_date in unique_dates:
            selection = logs[unique_date]
            need_total_time = len(selection) > 1
            selection += ["border"]

            for index, row in enumerate(selection):
                projected_length = len(rows) + 1
                is_last_index = index == len(selection) - 1

                # TODO вот тут надо считать с учетом страниц
                if projected_length == self.max_rows:
                    rows.append(SEE_NEXT_PAGE)

                if need_total_time and index == 1:
                    row[0] = f"[{total_day_time[unique_date]}]"

                elif need_total_time and index > 1 and not is_last_index:
                    row[0] = ""

                if is_last_index:
                    rows.append(f"{'-' * THIRD}-+-{'-' * THIRD}-+-{'-' * THIRD}")
                else:
                    rows.append(" | ".join([c.center(THIRD) for c in row]))

        return rows

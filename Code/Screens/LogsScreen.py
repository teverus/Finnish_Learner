from datetime import datetime, timedelta
from pathlib import Path

from Code.TeverusSDK.DataBase import DataBase
from Code.TeverusSDK.Screen import (
    Screen,
    SCREEN_WIDTH,
    GO_BACK_ACTION,
    THIRD_COLUMN as THIRD,
    ACTIONS_STUB,
)
from Code.TeverusSDK.Table import Table


class LogsScreen(Screen):
    def __init__(self):
        self.database = DataBase(Path("Files/Logs.db"))
        self.df = self.database.read_table()

        rows = self.get_records() if len(self.df) else ["No records so far..."]

        self.table = Table(
            table_title="Logs",
            rows=rows,
            rows_bottom_border="-",
            table_width=SCREEN_WIDTH,
            footer=[GO_BACK_ACTION],
        )

        super(LogsScreen, self).__init__(self.table, ACTIONS_STUB)

    def get_records(self):
        df_rows = [list(list(self.df.loc[index])) for index in range(len(self.df))]
        unique_dates = self.get_unique_dates(df_rows)
        total_day_time = self.get_total_day_times(unique_dates, df_rows)
        rows = self.get_rows(df_rows, total_day_time)

        return rows

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

    @staticmethod
    def get_rows(df_rows, total_day_time):
        rows = []
        already_used = False
        current_date = None

        for row in df_rows:
            date = row[0]
            if not current_date:
                current_date = date
            elif date != current_date:
                rows.append(f"{'-' * THIRD}-+-{'-' * THIRD}-+-{'-' * THIRD}")
                current_date = date
                already_used = False
            known_date = bool([r for r in rows if date in r])
            if known_date and not already_used:
                row[0] = f"[{total_day_time[date]}]"
                already_used = True
            elif known_date and already_used:
                row[0] = ""
            rows.append(" | ".join([c.center(THIRD) for c in row]))

        return rows

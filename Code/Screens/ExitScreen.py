from datetime import datetime

from Code.TeverusSDK.Screen import SCREEN_WIDTH
from Code.TeverusSDK.Table import Table


class ExitScreen:
    def __init__(self, main):
        time_elapsed = str(datetime.now() - main.start_time).split(".")[0]
        Table(
            table_title=f"TIME SPENT IN THE APPLICATION: {time_elapsed}",
            table_width=SCREEN_WIDTH,
            rows_bottom_border=False,
        ).print_table()

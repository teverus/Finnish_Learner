from pathlib import Path

from Code.Modules.PracticeSingleUnit import PracticeSingleUnit
from Code.Screens.PracticeBaseScreen import BasePracticeScreen


class PracticeWordSingleScreen(BasePracticeScreen):
    def __init__(self):
        super(PracticeWordSingleScreen, self).__init__(
            function=PracticeSingleUnit,
            unit_name="word",
            database_base=Path("Files/Words.db"),
        )

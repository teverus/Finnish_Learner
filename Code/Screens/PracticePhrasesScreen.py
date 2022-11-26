from pathlib import Path

from Code.Modules.PracticeSingleUnit import PracticeSingleUnit
from Code.Screens.PracticeBaseScreen import BasePracticeScreen


class PracticePhrasesScreen(BasePracticeScreen):
    def __init__(self):
        super(PracticePhrasesScreen, self).__init__(
            function=PracticeSingleUnit,
            unit_name="phrase",
            database_base=Path("Files/Phrases.db"),
        )

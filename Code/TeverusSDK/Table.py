import os
from math import ceil
from typing import Union

import bext
from colorama import Back, Fore

WHITE = Back.WHITE + Fore.BLACK
RED = Back.RED + Fore.WHITE
GREEN = Back.GREEN + Fore.WHITE
BLUE = Back.BLUE + Fore.WHITE

END_HIGHLIGHT = Back.BLACK + Fore.WHITE


class ColumnWidth:
    FULL = "Full"
    FIT = "Fit"


class Table:
    def __init__(
        self,
        # Rows
        rows: Union[list[str] | list[list[str]]] = None,
        rows_top_border="=",
        rows_bottom_border="=",
        rows_centered=True,
        # Table title
        table_title="",
        table_title_centered=True,
        table_title_caps=True,
        table_title_top_border="=",
        # Footer
        footer=None,
        footer_centered=True,
        footer_bottom_border="=",
        # General table
        table_width=None,
        highlight=None,
        current_page=1,
        max_rows=None,
        max_columns=None,
        column_widths=None,
        clear_console=True,
        show_cursor=False,
    ):
        # Internal use only
        self.side_padding_length = 2
        self.wall_length = 3

        # Table title
        self.table_title = table_title
        self.table_title_top_border = table_title_top_border
        self.table_title_centered = table_title_centered
        self.table_title_caps = table_title_caps

        # Rows
        self.rows = self.get_rows(rows)
        self.rows_top_border = rows_top_border
        self.rows_bottom_border = rows_bottom_border
        self.rows_centered = rows_centered

        # Footer
        self.footer = footer
        self.footer_bottom_border = footer_bottom_border
        self.footer_centered = footer_centered

        # General table
        self.highlight = highlight
        self.clear_console = clear_console
        self.show_cursor = show_cursor
        self.current_page = current_page
        self.max_rows = self.get_max_rows(max_rows)
        self.max_columns = self.get_max_columns(max_columns)
        self.has_multiple_pages = self.get_multiple_pages()
        self.max_page = self.get_max_page()
        self.cage = self.get_cage()

        # Calculated values
        self.walls_length = self.get_walls_length()
        self.visible_rows = self.get_visible_rows()
        self.table_width = self.get_table_width(table_width)
        self.column_widths = self.get_column_widths(column_widths)

    ####################################################################################
    #    PRINT TABLE                                                                   #
    ####################################################################################
    def print_table(self):

        # Clear the console
        if self.clear_console:
            os.system("cls")

        [bext.show if self.show_cursor else bext.hide][0]()

        # Print table title if any
        if self.table_title:
            if self.table_title_top_border:
                print(self.table_title_top_border * self.table_width)

            tt = self.table_title
            tt = tt.upper() if self.table_title_caps else tt
            tt = tt.center(self.table_width) if self.table_title_centered else tt
            print(tt)

        # TODO XXXXX    ?????????????? headers

        # Print rows top border if any
        if self.rows_top_border:
            print(self.rows_top_border * self.table_width)

        # Print rows, highlighting them if necessary
        self.visible_rows = self.get_visible_rows()
        for x, row in enumerate(self.visible_rows):
            line = []
            for y, cell in enumerate(row):
                target_width = self.column_widths[y]
                cell = cell.center(target_width) if self.rows_centered else cell
                highlighted = f"{WHITE}{cell}{END_HIGHLIGHT}"
                data = highlighted if [x, y] == self.highlight else cell
                line.append(data)
            line = " | ".join(line)
            print(f" {line} ")

        # Print rows bottom border if any
        if self.rows_bottom_border:
            print(self.rows_bottom_border * self.table_width)

        # Print footer if any
        if self.footer:
            for action in self.footer:
                line = action.name
                line = line.center(self.table_width) if self.footer_centered else line
                print(line)

        # Print pagination is needed
        if self.has_multiple_pages:
            arrow_l = "        " if self.current_page == 1 else "[Z] <<< "
            arrow_r = "        " if self.current_page == self.max_page else " >>> [X]"

            pag = f"{arrow_l}[{self.current_page:02}/{self.max_page:02}]{arrow_r}"
            pag = pag.center(self.table_width)

            print(pag)

    ####################################################################################
    #    TABLE CALCULATIONS                                                            #
    ####################################################################################
    @staticmethod
    def get_rows(rows):
        rows = [""] if not rows else rows
        rows = [rows] if not isinstance(rows, list) else rows
        result = [[r] if not isinstance(r, list) else r for r in rows]

        result = [["Nothing to show"]] if not result else result

        return result

    def get_max_rows(self, max_rows):
        result = max_rows if max_rows else len(self.rows)

        return result

    def get_max_columns(self, max_columns=None):
        result = max_columns if max_columns else max([len(r) for r in self.rows])

        return result

    def get_table_width(self, expected_width):
        if expected_width:
            return expected_width

        # TODO If no expected width
        known_lengths = []

        # Calculate the widest possible title length
        title_width = len(self.table_title) + self.side_padding_length
        known_lengths.append(title_width)

        # Calculate the widest possible row length
        max_row = max([sum([len(e) for e in row]) for row in self.visible_rows])
        max_row_length = max_row + self.walls_length + self.side_padding_length
        known_lengths.append(max_row_length)

        table_width = max(known_lengths)

        return table_width

    def get_column_widths(self, target_widths=None):
        actual_width = self.table_width - self.walls_length - self.side_padding_length
        column_widths = {}

        if not target_widths or len(target_widths) > self.max_columns:
            target_widths = {i: ColumnWidth.FULL for i in range(self.max_columns)}

        fit_cols = {k: v for k, v in target_widths.items() if v == ColumnWidth.FIT}
        full_cols = {k: v for k, v in target_widths.items() if v == ColumnWidth.FULL}
        expected_widths = {**fit_cols, **full_cols}

        full_target_length = None
        number_of_full_cols = len(full_cols)

        for col_index, width_type in expected_widths.items():
            if self.table_width:
                if width_type == ColumnWidth.FIT:
                    target_length = max(
                        [
                            len(row[col_index]) if isinstance(row, list) else len(row)
                            for row in self.visible_rows
                        ]
                    )
                else:
                    if not full_target_length:
                        already_used = sum([v for v in column_widths.values()])
                        remaining = actual_width - already_used
                        if remaining % number_of_full_cols == 0:
                            full_target_length = int(remaining / number_of_full_cols)
                        else:
                            extra = remaining % number_of_full_cols
                            proper_width = self.table_width - extra
                            raise Exception(f"Please use table_width = {proper_width}")
                    target_length = full_target_length

                column_widths[col_index] = target_length
            else:
                raise NotImplementedError("\n\nUse table_width!")

        return column_widths

    def get_visible_rows(self):
        previous_page = self.current_page - 1
        start = self.max_rows * previous_page
        end = self.max_rows * self.current_page

        pack = self.rows[start:end]

        if len(pack) != self.max_rows:
            diff = self.max_rows - len(pack)
            for _ in range(diff):
                dummy = ["" for __ in range(self.max_columns)]
                pack.append(dummy)

        return pack

    def get_cage(self):
        x_axis = [number for number in range(self.max_rows)]
        y_axis = [number for number in range(self.max_columns)]

        coordinates = []
        for x in x_axis:
            for y in y_axis:
                coordinates.append([x, y])

        return coordinates

    def get_max_page(self):
        if self.has_multiple_pages:
            max_page = ceil(len(self.rows) / self.max_rows)

            return max_page

    def get_multiple_pages(self):
        is_multiple_pages = bool(len(self.rows) > self.max_rows)

        return is_multiple_pages

    def get_walls_length(self):
        result = (self.max_columns - 1) * self.wall_length

        return result

    def set_nothing_to_show_state(self):
        self.rows = [["Nothing to show"]]
        self.max_columns = 1
        self.walls_length = self.get_walls_length()
        self.column_widths = self.get_column_widths()

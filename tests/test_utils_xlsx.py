from os import close
from os import unlink
from os.path import getsize
from random import choice
from random import randint
from tempfile import mkstemp
from unittest import TestCase

from pandas import read_excel
from courtbot.xlsx import xlsx_file


class TestEvents(TestCase):
    """
    Test court events
    """

    def test_xlsx_file_writes_to_file(self):
        """
        Given a file to write to, when xlsx_file() is called
        then generated entries should be added to the file in xlsx format.
        """

        file_descriptor, filename = mkstemp()
        close(file_descriptor)

        # The size, in bytes, of the newly created file should be zero.
        file_size = getsize(filename)
        assert file_size == 0

        rows_to_write = 100
        rows = [["X"]] * rows_to_write
        xlsx_file(filename, rows)

        # xlsx_file should have written bytes
        file_size = getsize(filename)
        assert file_size > 0

        unlink(filename)

    def test_xlsx_file_writes_expected_number_of_rows(self):
        """
        Given a file to write and a number of rows to generate,
        when xlsx_file() is called,
        then the file should be populated with a number of rows equal to the argument supplied.
        """
        rows_to_write = randint(0, 100)
        rows = ["X"] * rows_to_write
        file_descriptor, filename = mkstemp()
        close(file_descriptor)

        # Add rows to file
        xlsx_file(filename, rows)

        # Read the excel file
        dataframe = read_excel(filename, header=None)

        excel_rows_read = len(dataframe)

        # The number of rows in the Excel file should be equal to the number_of_rows value

        assert excel_rows_read == rows_to_write

        unlink(filename)

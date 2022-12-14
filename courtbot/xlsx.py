from xlsxwriter import Workbook
from courtbot.model.events import event_document


def court_schedule_file(filename, attorneys, cases, court_divisions, judges, litigants):
    rows = list()
    event_document = event_document(attorneys, cases, court_divisions, judges, litigants)
    row = event_document_as_court_schedule_file_row(event_document)
    rows.append(row)
    xlsx_file(filename, rows)


def xlsx_file(filename, rows):
    """
    :param filename: {str} the full path and filename to write an xlsx file.
    :param rows: {List<List>} A list the rows
    """
    row_count = len(rows)
    # Create an xlsx workbook and worksheet
    workbook = Workbook(filename)
    worksheet = workbook.add_worksheet()
    # Populate xlsx cells
    for row_index in range(row_count):
        row = rows[row_index]
        column_count = len(row)
        for column_index in range(column_count):
            worksheet.write(row_index, column_index, row[column_index])
    workbook.close()

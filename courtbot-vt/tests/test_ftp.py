"""
Pytest test spans tests for the ftp functionality of the courtbot-vt project.
"""

from io import StringIO
from logging import getLogger
from logging import error
from os import getenv
from os import close
from os import unlink
from pathlib import Path
from tempfile import mkstemp
from unittest import TestCase

from pandas import read_excel
from paramiko.client import AutoAddPolicy
from paramiko import RSAKey
from paramiko import SSHClient
from src.ftp import ftp
from courtbot.model.events import event_document
from courtbot.model.events import event_document_as_court_schedule_file_row
from courtbot.xlsx import xlsx_file


class TestFtp(TestCase):
    """
    Test cases for SSH FTP file transfers and MongoDB document upload processes.
    """

    def test_file_retrieved_from_ftp_is_removed(self):
        log = getLogger("events")
        SFTP_PRIVATE_KEY = getenv("SFTP_PRIVATE_KEY")
        SFTP_HOST = getenv("SFTP_HOST")
        SFTP_PORT = int(getenv("SFTP_PORT", "22"))
        SFTP_USERNAME = getenv("SFTP_USERNAME")
        RESOURCE_DIRECTORY = getenv("RESOURCE_DIRECTORY")
        resources = Path(RESOURCE_DIRECTORY)

        # Create a new temporary file.
        file_descriptor, filename = mkstemp()
        close(file_descriptor)

        # Create an XLSX file
        attorneys = resources / "json/attorneys.json"
        cases = resources / "json/cases.json"
        court_divisions = resources / "json/court_divisions.json"
        judges = resources / "json/judges.json"
        litigants = resources / "json/litigants.json"
        rows = list()
        event = event_document(attorneys, cases, court_divisions, judges, litigants)
        row = event_document_as_court_schedule_file_row(event)
        rows.append(row)
        xlsx_file(filename, rows)
        try:
            # Initialize an SSH client for an SFTP connection
            ssh = SSHClient()
            ssh.set_missing_host_key_policy(AutoAddPolicy)
            key = RSAKey.from_private_key(
                StringIO(SFTP_PRIVATE_KEY.replace("\\n", "\n"))
            )
            ssh.connect(SFTP_HOST, port=SFTP_PORT, username=SFTP_USERNAME, pkey=key)

            with ssh.open_sftp() as sftp:
                # Add the file to the server.
                sftp.put(filename, f"test.xlsx")

                # The file should exist and be the only file on the server.
                files = sftp.listdir()
                assert len(files) == 1

            ftp()

            with ssh.open_sftp() as sftp:

                # The file should have been removed

                files = sftp.listdir()
                assert len(files) == 0
        except Exception as e:
            log.error(e)
            exit(1)
        finally:
            unlink(filename)
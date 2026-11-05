from pathlib import Path
import pytest
import sys

src_path = Path(__file__).resolve().parent.parent / 'src'
sys.path.append(str(src_path))
from Database.databaseManager import DatabaseManager

@pytest.fixture()
def testDBManager():
    testDB = DatabaseManager("Test_DB")
    yield testDB
    testDB.deleteDatabase()

@pytest.fixture()
def tableNames():
    return ["EventRounds", "TeamData", "DriverData"]
    
def testDropTables(testDBManager, tableNames):
    # ACT
    testDBManager.dropAllTables()
    # ASSERT
    for table in tableNames:
        assert testDBManager.checkTableExists(table) is False
from pathlib import Path
import pytest
import sys

src_path = Path(__file__).resolve().parent.parent / 'src'
sys.path.append(str(src_path))
from Database.databaseManager import DatabaseManager

@pytest.fixture()
def testDBManager():
    testDB = DatabaseManager("Test_DB.db")
    yield testDB
    testDB.deleteDatabase()

@pytest.fixture()
def tableNames():
    return ["EventRounds", "TeamData", "DriverData"]
    
def testCreateDatabase(testDBManager, tableNames):
    # ACT
    # None - database are created in __init__
    # ASSERT
    for table in tableNames:
        assert testDBManager.checkTableExists(table) is True

    assert testDBManager.checkTableExists("NonexistentTable") is False

def testDropTables(testDBManager, tableNames):
    # ACT
    testDBManager.dropAllTables()
    # ASSERT
    for table in tableNames:
        assert testDBManager.checkTableExists(table) is False
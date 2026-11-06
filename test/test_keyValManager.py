from operator import not_
from pathlib import Path
import pytest
import sys

src_path = Path(__file__).resolve().parent.parent / 'src'
db_path = src_path / 'Database'
class_path = src_path / 'Classes'
sys.path.append(str(src_path))
sys.path.append(str(db_path))
sys.path.append(str(class_path))

from Database.databaseManager import DatabaseManager
from Database.keyValManager import KeyValManager

@pytest.fixture()
def testKeyValManager():
    
    testDB = DatabaseManager("Test_DB.db")
    testKVManager = KeyValManager(testDB.databaseConnection)
    yield testKVManager
    testDB.deleteDatabase()

def testInsertAndGetKeyVal(testKeyValManager):

    # ACT
    testKeyValManager.insertKeyVal("Key", "value")
    testKeyValManager.insertKeyVal("Number", 44)
    firstValue = testKeyValManager.getKeyVal("Key")
    secondValue = testKeyValManager.getKeyVal("Number")
    # Assert
    assert firstValue == "value"
    assert secondValue == 44

def testUpdateKeyVal(testKeyValManager):

    # ACT
    testKeyValManager.insertKeyVal("Key", "aValue")
    testKeyValManager.updateKeyVal("Key", "aNewValue")
    newValue = testKeyValManager.getKeyVal("Key")
    # ASSERT
    assert newValue == "aNewValue"

def testDeleteKeyVal(testKeyValManager):

    # ACT
    testKeyValManager.insertKeyVal("Key", "Delete me")
    testKeyValManager.insertKeyVal("Number", 12)
    testKeyValManager.deleteKeyVal("Key")
    deletedValue = testKeyValManager.getKeyVal("Key")
    notDeletedValue = testKeyValManager.getKeyVal("Number")
    # ASSERT
    assert deletedValue is None
    assert notDeletedValue == 12

def testGetAndIterateKeyVal(testKeyValManager):

    # ACT
    testKeyValManager.insertKeyVal("Key", 4)
    uniteratedValue = testKeyValManager.getAndIterateKeyVal("Key")
    iteratedValue = testKeyValManager.getKeyVal("Key")
    # ASSERT
    assert uniteratedValue == 4
    assert iteratedValue == 5
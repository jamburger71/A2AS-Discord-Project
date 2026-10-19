from pathlib import Path
import pytest
import sys

src_path = Path(__file__).resolve().parent.parent / 'src'
db_path = src_path / 'Database'
class_path = src_path / 'Classes'
sys.path.append(str(src_path))
sys.path.append(str(db_path))
sys.path.append(str(class_path))

from databaseManager import DatabaseManager
from keyValManager import KeyValManager

@pytest.fixture()
def testKeyValManager():
    testDB = DatabaseManager("Test_DB.db")
    testKVManager = KeyValManager(testDB.DatabaseConnection)
    yield testKVManager
    testDB.deleteDatabase()
import pytest
import sys
sys.path.insert("../src") #add src to path for moduke search
from databaseManager import DatabaseManager
import testdata

@pytest.fixture()
def testDBManager():

    testDB = databaseManager("TestDB")
    yield testDB
    testDB.deleteDatabase()

@pytest.fixture()
def tableNames():
    return ["TeamData", "DriverData", "KeyVal"]

@pytest.fixture()
def driverDataSample():
    return testdata.drivers
    
def testCreateDatabase(testDBManager, tableNames):
    # ACT
    # None - database are created in __init__
    # ASSERT
    for table in tableNames:
        assert testDBManager.checkTableExists(table) is True

    assert testDBManager.checkTableExists("NonexistentTable") is False

def testDropTables(testDBManager):
    # ACT
    testDBManager.dropAllTables()
    # ASSERT
    for table in tableNames:
        assert testDBManager.checkTableExists(table) is False

def testAddDriverToDatabase(testDBManager, driverDataSample):
    # ACT
    for driver in driverDataSample:
        testDBManager.insertDriver(*driver)
    allDrivers = testDBManager.getAllDrivers()
    # ASSERT
    assert len(allDrivers) == 6
    assert allDrivers[0] == (0, *driverDataSample[0]) # Adds expected driver ID
    assert allDrivers[1] == (1, *driverDataSample[1])
    assert allDrivers[2] == (2, *driverDataSample[2])
    assert allDrivers[3] == (3, *driverDataSample[3])
    assert allDrivers[4] == (4, *driverDataSample[4])
    assert allDrivers[5] == (5, *driverDataSample[5])
    
def testRemoveDriverFromDatabase(testDBManager, driverDataSample):
    # ACT
    for driver in driverDataSample:
        testDBManager.insertDriver(*driver)
    driverCountBefore = len(testDBManager.getAllDrivers())
    testDBManager.removeDriver("MSC")
    testDBManager.removeDriver(5)
    driverCountAfter = len(testDBManager.getAllDrivers())
    # ASSERT
    assert driverCountBefore - 1 = driverCountAfter
    assert testDBManager.getDriver("MSC") is None
    assert testDBManager.getDriver("TES") is not None
    assert testDBManager.getDriver(4) is not None
    assert testDBManager.getDriver(5) is None
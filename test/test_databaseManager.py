from pathlib import Path

import pytest
import sys
src_path = Path(__file__).resolve().parent.parent / 'src'
sys.path.append(str(src_path))
from databaseManager import DatabaseManager
import testdata

@pytest.fixture()
def testDBManager():

    testDB = DatabaseManager("Test_DB")
    yield testDB
    testDB.deleteDatabase()

@pytest.fixture()
def tableNames():
    return ["EventRounds", "TeamData", "DriverData"]

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

def testDropTables(testDBManager, tableNames):
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
    print(allDrivers[0])
    print(driverDataSample[0])
    assert allDrivers[0] == (0, *driverDataSample[0], 0, 0, 0) # Adds expected driver ID
    assert allDrivers[1] == (1, *driverDataSample[1], 0, 0, 0)
    assert allDrivers[2] == (2, *driverDataSample[2], 0, 0, 0)
    assert allDrivers[3] == (3, *driverDataSample[3], 0, 0, 0)
    assert allDrivers[4] == (4, *driverDataSample[4], 0, 0, 0)
    assert allDrivers[5] == (5, *driverDataSample[5], 0, 0, 0)

def testGetDriverByIDAndCode(testDBManager, driverDataSample):
    # ACT
    for driver in driverDataSample:
        testDBManager.insertDriver(*driver)
    driverByID = testDBManager.getDriver(2)
    driverByCode = testDBManager.getDriver("ALO")
    # ASSERT
    assert driverByID == (2, *driverDataSample[2], 0, 0, 0)
    assert driverByCode == (2, *driverDataSample[2], 0, 0, 0)

def testRemoveDriverFromDatabase(testDBManager, driverDataSample):
    # ACT
    for driver in driverDataSample:
        testDBManager.insertDriver(*driver)
    driverCountBefore = len(testDBManager.getAllDrivers())
    testDBManager.removeDriver("MSC")
    testDBManager.removeDriver(5)
    driverCountAfter = len(testDBManager.getAllDrivers())
    # ASSERT
    assert driverCountBefore - 2 == driverCountAfter
    assert testDBManager.getDriver("MSC") is None
    assert testDBManager.getDriver(5) is None
    assert testDBManager.getDriver("DRI") is not None
    assert testDBManager.getDriver(4) is not None

def testUpdateDriverInDatabase(testDBManager, driverDataSample):
    # ACT
    for driver in driverDataSample:
        testDBManager.insertDriver(*driver)
    testDBManager.updateDriver(3, "UpdatedFirstName", "UpdatedLastName", "UPD", 99, 99, 99)
    updatedDriver = testDBManager.getDriver(3)
    # ASSERT
    assert updatedDriver == (3, "UpdatedFirstName", "UpdatedLastName", "UPD", 99, 99, 99)
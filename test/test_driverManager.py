from pathlib import Path

import pytest
import sys
src_path = Path(__file__).resolve().parent.parent / 'src' / 'Database'
sys.path.append(str(src_path))
from databaseManager import DatabaseManager
from driverManager import DriverManager
import testdata

@pytest.fixture()
def testDriverManager():
    testDB = DatabaseManager("Test_DB")
    testDrvrManager = DriverManager(testDB.DatabaseConnection)
    yield testDrvrManager
    testDB.deleteDatabase()

@pytest.fixture()
def driverDataSample():
    return testdata.drivers

def testAddDriverToDatabase(testDriverManager, driverDataSample):
    # ACT
    for driver in driverDataSample:
        testDriverManager.insertDriver(*driver)
    allDrivers = testDriverManager.getAllDrivers()
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

def testGetDriverByIDAndCode(testDriverManager, driverDataSample):
    # ACT
    for driver in driverDataSample:
        testDriverManager.insertDriver(*driver)
    driverByID = testDriverManager.getDriver(2)
    driverByCode = testDriverManager.getDriver("ALO")
    # ASSERT
    assert driverByID == (2, *driverDataSample[2], 0, 0, 0)
    assert driverByCode == (2, *driverDataSample[2], 0, 0, 0)

def testRemoveDriverFromDatabase(testDriverManager, driverDataSample):
    # ACT
    for driver in driverDataSample:
        testDriverManager.insertDriver(*driver)
    driverCountBefore = len(testDriverManager.getAllDrivers())
    testDriverManager.removeDriver("MSC")
    testDriverManager.removeDriver(5)
    driverCountAfter = len(testDriverManager.getAllDrivers())
    # ASSERT
    assert driverCountBefore - 2 == driverCountAfter
    assert testDriverManager.getDriver("MSC") is None
    assert testDriverManager.getDriver(5) is None
    assert testDriverManager.getDriver("DRI") is not None
    assert testDriverManager.getDriver(4) is not None

def testUpdateDriverInDatabase(testDriverManager, driverDataSample):
    # ACT
    for driver in driverDataSample:
        testDriverManager.insertDriver(*driver)
    testDriverManager.updateDriverStats(3, True, True)
    updatedDriver = testDriverManager.getDriver(3)
    # ASSERT
    assert updatedDriver == (3, *driverDataSample[3], 1, 1, 1)
    
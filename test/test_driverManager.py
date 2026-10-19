from discordLogger import DiscordLogger
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
from driverManager import DriverManager
import testdata
from Classes.driver import Driver

@pytest.fixture()
def testDriverManager():
    testDB = DatabaseManager("Test_DB.db")
    testDrvrManager = DriverManager(testDB.DatabaseConnection)
    yield testDrvrManager
    testDB.deleteDatabase()

@pytest.fixture()
def driverDataSample():
    return testdata.drivers

def testAddDriverToDatabase(testDriverManager, driverDataSample):
    # ACT
    for driver in driverDataSample:
        testDriverManager.insertDriverFromClass(driver)
    allDrivers: list[Driver] = testDriverManager.getAllDrivers()
    # ASSERT
    assert len(allDrivers) == 6
    assert allDrivers[0].firstName == driverDataSample[0].firstName
    assert allDrivers[1].firstName == driverDataSample[1].firstName
    assert allDrivers[2].firstName == driverDataSample[2].firstName
    assert allDrivers[3].firstName == driverDataSample[3].firstName
    assert allDrivers[4].firstName == driverDataSample[4].firstName
    assert allDrivers[5].firstName == driverDataSample[5].firstName

def testGetDriverByIDAndCode(testDriverManager, driverDataSample):
    # ACT
    for driver in driverDataSample:
        testDriverManager.insertDriverFromClass(driver)
    driverByID: Driver = testDriverManager.getDriver(2)
    driverByCode: Driver = testDriverManager.getDriver("ALO")
    # ASSERT
    assert driverByID.firstName == driverDataSample[2].firstName
    assert driverByCode.firstName == driverDataSample[2].firstName

def testRemoveDriverFromDatabase(testDriverManager, driverDataSample):
    # ACT
    for driver in driverDataSample:
        testDriverManager.insertDriverFromClass(driver)
    driverCountBefore: int = len(testDriverManager.getAllDrivers())
    testDriverManager.removeDriver("MSC")
    testDriverManager.removeDriver(5)
    driverCountAfter: int = len(testDriverManager.getAllDrivers())
    # ASSERT
    assert driverCountBefore - 2 == driverCountAfter
    assert testDriverManager.getDriver("MSC") is None
    assert testDriverManager.getDriver(5) is None
    assert testDriverManager.getDriver("DRI") is not None
    assert testDriverManager.getDriver(4) is not None

def testUpdateDriverInDatabase(testDriverManager, driverDataSample):
    # ACT
    for driver in driverDataSample:
        testDriverManager.insertDriverFromClass(driver)
    testDriverManager.updateDriverStats(1, won=False, podium=False)
    testDriverManager.updateDriverStats(2, won=False, podium=True)
    testDriverManager.updateDriverStats(3, won=True, podium=True)
    updatedDriverFinished: Driver = testDriverManager.getDriver(1)
    updatedDriverPodium: Driver = testDriverManager.getDriver(2)
    updatedDriverWinner: Driver = testDriverManager.getDriver(3)
    # ASSERT
    assert updatedDriverFinished.races == 1
    assert updatedDriverFinished.podiums == 0
    assert updatedDriverFinished.wins == 0
    assert updatedDriverPodium.races == 1
    assert updatedDriverPodium.podiums == 1
    assert updatedDriverPodium.wins == 0
    assert updatedDriverWinner.races == 1
    assert updatedDriverWinner.podiums == 1
    assert updatedDriverWinner.wins == 1
    assert updatedDriverWinner.isAvailable == True

def testToggleDriverAvailability(testDriverManager, driverDataSample):
    # ACT
    for driver in driverDataSample:
        testDriverManager.insertDriverFromClass(driver)
    testDriverManager.setDriverAvailability(1, False)
    testDriverManager.setDriverAvailability(2, False)
    availableDrivers: list[Driver] = testDriverManager.getAllDrivers(availableOnly=True)
    # ASSERT
    assert len(availableDrivers) == 4
    assert all(driver.id not in [1, 2] for driver in availableDrivers)

def testAgeAllDrivers(testDriverManager, driverDataSample):
    # ACT
    for driver in driverDataSample:
        testDriverManager.insertDriverFromClass(driver)
    testDriverManager.ageAllDrivers(DiscordLogger(None, "Testing", None))
    agedDrivers: list[Driver] = testDriverManager.getAllDrivers()
    # ASSERT
    assert all(driver.age == driverDataSample[index].age + 1 for index, driver in enumerate(agedDrivers))
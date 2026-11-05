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

from Database.databaseManager import DatabaseManager
from Database.driverManager import DriverManager
import testdata
from Classes.driver import Driver

@pytest.fixture()
def testDriverManager():
    testDB = DatabaseManager("Test_DB")
    testDrvrManager = DriverManager(testDB.DatabaseConnection)
    yield testDrvrManager
    testDB.deleteDatabase()

def testInsertGetDrivers(testDriverManager):
    # ACT
    localDrivers: list[Driver] = []
    for id in range(10):
        newDriver = Driver.randomDriver(id)
        localDrivers.append(newDriver)
        testDriverManager.insertDriver(newDriver)
    allDrivers: list[Driver] = testDriverManager.getDrivers()
    print(allDrivers)
    # ASSERT
    assert len(allDrivers) == 10
    for id in range(10):
        assert allDrivers[id].firstName == localDrivers[id].firstName

def testInsertGetDriver(testDriverManager):
    # ACT
    newDriver = Driver.randomDriver(0)
    testDriverManager.insertDriver(newDriver)
    fetchedDriver: Driver = testDriverManager.getDriver(0)
    # ASSERT
    assert newDriver.firstName == fetchedDriver.firstName

def testRemoveDriver(testDriverManager):
    # ACT
    for id in range(10):
        newDriver = Driver.randomDriver(id)
        testDriverManager.insertDriver(newDriver)
    driverCountBefore: int = len(testDriverManager.getDrivers())
    testDriverManager.removeDriver(5)
    driverCountAfter: int = len(testDriverManager.getDrivers())
    # ASSERT
    assert driverCountBefore - 1 == driverCountAfter
    print(testDriverManager.getDriver(5))
    assert testDriverManager.getDriver(5) == None

def testUpdateDriver(testDriverManager):
    # ACT
    testDriverManager.insertDriver(Driver.randomDriver(0))
    driverToUpdate: Driver = testDriverManager.getDriver(0)
    driverToUpdate.firstName = "NewName"
    driverToUpdate.qualiPace = 22
    testDriverManager.updateDriver(driverToUpdate)
    driverUpdated = testDriverManager.getDriver(0)
    print(driverUpdated.firstName+driverUpdated.lastName)
    # ASSERT
    assert driverUpdated.firstName == "NewName"
    assert driverUpdated.qualiPace == 22

def testAgeAllDrivers(testDriverManager):
    # ACT
    localDrivers = []
    for id in range(10):
        newDriver = Driver.randomDriver(id)
        localDrivers.append(newDriver)
        testDriverManager.insertDriver(newDriver)
    testDriverManager.ageAllDrivers()
    agedDrivers: list[Driver] = testDriverManager.getDrivers()
    # ASSERT
    assert all(driver.age == localDrivers[index].age + 1 for index, driver in enumerate(agedDrivers))
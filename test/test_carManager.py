import inspect
from pathlib import Path

import pytest
import sys
import random
src_path = Path(__file__).resolve().parent.parent / 'src'
db_path = src_path / 'Database'
class_path = src_path / 'Classes'
sys.path.append(str(src_path))
sys.path.append(str(db_path))
sys.path.append(str(class_path))

from Database.databaseManager import DatabaseManager
from Database.carManager import CarManager
from Classes.car import Car

@pytest.fixture()
def testCarManager():
    testDB = DatabaseManager("Test_DB")
    testcarmanager = CarManager(testDB.databaseConnection)
    yield testcarmanager
    testDB.deleteDatabase()

@pytest.fixture()
def carSampleSet() -> list[Car]:
    set = []
    set.append(Car(("car_tst_01", "Test", "Description", "Test", 2000, "tst_class", 10, 800, 820, 2.5, 10, 1.07, 0.01, 10)))
    set.append(Car(("car_tst_02", "Test2", "Description", "Test", 2000, "tst_class", 10, 800, 820, 2.5, 10, 1.07, 0.01, 10)))
    set.append(Car(("car_tst_03", "Test3", "Description", "Test", 2000, "tst_class", 10, 800, 820, 2.5, 10, 1.07, 0.01, 10)))
    set.append(Car(("car_tst_04", "Test4", "Description", "Test", 2000, "tst_class_2", 10, 800, 820, 2.5, 10, 1.07, 0.01, 10)))
    set.append(Car(("car_tst_05", "Test5", "Description", "Test", 2000, "tst_class_2", 10, 800, 820, 2.5, 10, 1.07, 0.01, 10)))
    set.append(Car(("car_tst_06", "Test6", "Description", "Test", 2000, "tst_class_3", 10, 800, 820, 2.5, 10, 1.07, 0.01, 10)))
    return set

def testInsertAndGetCar(testCarManager, carSampleSet):

    # ACT
    testCar = random.choice(carSampleSet)
    testCarManager.insertCar(testCar)
    fetchedCar = testCarManager.getCar(testCar.ID)
    # ASSERT
    assert testCar.toTuple() == fetchedCar.toTuple()

def testGetCars(testCarManager, carSampleSet):

    # ACT
    for car in carSampleSet:
        testCarManager.insertCar(car)
    fetchedCars = testCarManager.getCars()
    # ASSERT
    assert len(fetchedCars) == 6
    for i in range(6):
        assert fetchedCars[i].toTuple() == carSampleSet[i].toTuple()

def testGetCarsInClass(testCarManager, carSampleSet):

    # ACT
    for car in carSampleSet:
        testCarManager.insertCar(car)
    carClass = carSampleSet[3].carClass
    fetchedCars = testCarManager.getCarsInClass(carClass)
    # ASSERT
    assert len(fetchedCars) == 2
    assert fetchedCars[0].toTuple() == carSampleSet[3].toTuple()
    assert fetchedCars[1].toTuple() == carSampleSet[4].toTuple()

def testUpdateCar(testCarManager, carSampleSet):

    # ACT
    for car in carSampleSet:
        testCarManager.insertCar(car)
    originalCar = testCarManager.getCar(carSampleSet[5].ID)
    originalCar.name = "UpdatedName"
    testCarManager.updateCar(originalCar)
    fetchedCar = testCarManager.getCar(originalCar.ID)
    # ASSERT
    assert fetchedCar.toTuple() == originalCar.toTuple()

def testDeleteCar(testCarManager, carSampleSet):

    # ACT
    for car in carSampleSet:
        testCarManager.insertCar(car)
    testCarManager.deleteCar(carSampleSet[2].ID)
    deletedCar = testCarManager.getCar(carSampleSet[2].ID)
    remainingCars = testCarManager.getCars()
    # ASSERT
    assert deletedCar is None
    assert len(remainingCars) == len(carSampleSet) - 1
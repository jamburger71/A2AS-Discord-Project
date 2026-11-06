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
from Database.carClassManager import CarClassManager
from Classes.carClass import CarClass

@pytest.fixture()
def testCarClassManager():
    testDB = DatabaseManager("Test_DB")
    testcarclassmanager = CarClassManager(testDB.DatabaseConnection)
    yield testcarclassmanager
    testDB.deleteDatabase()

def testInsertAndGetCarClass(testCarClassManager):

    # ACT
    testCarClass = CarClass((0, "TestClass", "Description"))
    testCarClassManager.insertCarClass(testCarClass)
    fetchedCarClass = testCarClassManager.getCarClass(testCarClass.id)
    # ASSERT
    assert isinstance(fetchedCarClass, CarClass)
    assert isinstance(testCarClass, CarClass)
    assert fetchedCarClass.id == testCarClass.id
    assert fetchedCarClass.name == testCarClass.name
    assert fetchedCarClass.description == testCarClass.description

def testGetAllCarClasses(testCarClassManager):

    # ACT
    for i in range(10):
        testCarClass = CarClass.new((i, f"test{i}", f"description {i}"))
        testCarClassManager.insertCarClass(testCarClass)
    allClasses = testCarClassManager.getCarClasses()
    # ASSERT
    assert len(allClasses) == 10
    assert allClasses[0].name == "test0"

def testUpdateCarClass(testCarClassManager):

    # ACT
    testCarClassManager.insertCarClass(CarClass.new((5, "original", "words")))
    fetchedCarClass = testCarClassManager.getCarClass(5)
    fetchedCarClass.name = "Edited"
    testCarClassManager.updateCarClass(fetchedCarClass)
    editedCarClass = testCarClassManager.getCarClass(5)
    # ASSERT
    assert editedCarClass.name == "Edited"

def testDeleteCarClass(testCarClassManager):

    # ACT
    testCarClassManager.insertCarClass(CarClass.new((21, "original", "words")))
    testCarClassManager.insertCarClass(CarClass.new((5, "original", "words")))
    testCarClassManager.deleteCarClass(21)
    deletedClass = testCarClassManager.getCarClass(21)
    notDeletedClass = testCarClassManager.getCarClass(5)
    # ASSERT
    assert deletedClass is None
    assert notDeletedClass is not None
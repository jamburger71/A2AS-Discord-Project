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
from Database.engineManager import EngineManager
from Classes.engine import Engine

@pytest.fixture()
def testEngineManager():
    testDB = DatabaseManager("Test_DB")
    testEngManager = EngineManager(testDB.databaseConnection)
    yield testEngManager
    testDB.deleteDatabase()

@pytest.fixture()
def engineSampleSet():
    set = []
    set.append(Engine(("E1", "Ferrari", 2006, 600, 65, 2500000)))
    set.append(Engine(("RB12", "Honda", 2005, 575, 80, 1400000)))
    set.append(Engine(("F106V8", "Toyota", 2007, 750, 85, 3000000)))
    set.append(Engine(("Engine", "Maker", 2010, 999, 100, 100)))
    set.append(Engine(("EcoBoom", "Ford", 2010, 230, 5, 10000)))
    return set

def testInsertAndGetEngine(testEngineManager, engineSampleSet):

    # ACT
    for engine in engineSampleSet:
        testEngineManager.insertEngine(engine)
    fetchedEngine = testEngineManager.getEngine(engineSampleSet[1].model)
    # ASSERT
    assert fetchedEngine.toTuple() == engineSampleSet[1].toTuple()

def testGetEngines(testEngineManager, engineSampleSet):

    # ACT
    for engine in engineSampleSet:
        testEngineManager.insertEngine(engine)
    fetchedEngines = testEngineManager.getEngines()
    # ASSERT
    for i in range(len(fetchedEngines)):
        assert fetchedEngines[i].toTuple() == engineSampleSet[i].toTuple()

def testGetEnginesFromYear(testEngineManager, engineSampleSet):

    # ACT
    for engine in engineSampleSet:
        testEngineManager.insertEngine(engine)
    fetchedEngines = testEngineManager.getEnginesByYear(2010)
    # ASSERT
    assert len(fetchedEngines) == 2
    assert fetchedEngines[0].toTuple() == engineSampleSet[3].toTuple()
    assert fetchedEngines[1].toTuple() == engineSampleSet[4].toTuple()

def testUpdateEngine(testEngineManager, engineSampleSet):

    # ACT
    for engine in engineSampleSet:
        testEngineManager.insertEngine(engine)
    originalEngine = testEngineManager.getEngine("E1")
    unchangedEngine = testEngineManager.getEngine("RB12")
    originalEngine.manufacturer = "Lamborghini"
    originalEngine.year = 2019
    testEngineManager.updateEngine(originalEngine)
    changedEngine = testEngineManager.getEngine("E1")
    unchangedEngine2 = testEngineManager.getEngine("RB12")
    # ASSERT
    assert originalEngine.toTuple() == changedEngine.toTuple()
    assert unchangedEngine.toTuple() == unchangedEngine2.toTuple()

def testDeleteEngine(testEngineManager, engineSampleSet):

    # ACT
    for engine in engineSampleSet:
        testEngineManager.insertEngine(engine)
    testEngineManager.deleteEngine("E1")
    remainingEngines = testEngineManager.getEngines()
    missingEngine = testEngineManager.getEngine("E1")
    # ASSERT
    assert len(remainingEngines) == len(engineSampleSet) - 1
    assert missingEngine is None
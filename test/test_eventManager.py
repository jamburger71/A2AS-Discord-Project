from pathlib import Path
from datetime import datetime
import pytest
import sys

src_path = Path(__file__).resolve().parent.parent / 'src'
db_path = src_path / 'Database'
class_path = src_path / 'Classes'
sys.path.append(str(src_path))
sys.path.append(str(db_path))
sys.path.append(str(class_path))

from Database.databaseManager import DatabaseManager
from Database.eventManager import EventManager
from Classes.event import Event


@pytest.fixture()
def testEventManager():
    testDB = DatabaseManager("Test_DB")
    testEvntManager = EventManager(testDB.databaseConnection)
    yield testEvntManager
    testDB.deleteDatabase()


@pytest.fixture()
def eventSampleSet():
    set = []
    set.append(Event.create(1, 1, "Race 1", datetime.today(), "long-beach_gp", None, 15, 80))
    set.append(Event.create(1, 2, "Race 2", datetime.today(), "nurburgring_gp", None, 15, 62))
    set.append(Event.create(1, 3, "Race 3", datetime.today(), "silverstone_2010-gp", None, 15, 55))
    set.append(Event.create(1, 4, "Race 4", datetime.today(), "monaco_gp", None, 15, 79))
    set.append(Event.create(2, 1, "Race 1", datetime.today(), "interlagos_gp", None, 15, 59))
    set.append(Event.create(2, 2, "Race 2", datetime.today(), "long-beach_gp", None, 15, 80))
    set.append(Event.create(2, 3, "Race 3", datetime.today(), "watkins-glen_gp", None, 15, 67))
    set.append(Event.create(3, 1, "Race 1", datetime.today(), "monaco_gp", None, 15, 79))

    return set


def testInsertAndGetEvent(testEventManager, eventSampleSet):

    # ACT
    for event in eventSampleSet:
        testEventManager.insertEvent(event)
    fetchedEvent = testEventManager.getEvent(2, 3)
    # ASSERT
    assert fetchedEvent.toTuple() == eventSampleSet[6].toTuple()


def testGetEvents(testEventManager, eventSampleSet):

    # ACT
    for event in eventSampleSet:
        testEventManager.insertEvent(event)
    fetchedEvents = testEventManager.getEvents()
    # ASSERT
    for i in range(len(eventSampleSet)):
        assert fetchedEvents[i].toTuple() == eventSampleSet[i].toTuple()


def testGetEventsFromSeason(testEventManager, eventSampleSet):

    # ACT
    for event in eventSampleSet:
        testEventManager.insertEvent(event)
    fetchedEvents = testEventManager.getEventsFromSeason(2)
    # ASSERT
    assert len(fetchedEvents) == 3
    assert fetchedEvents[0].toTuple() == eventSampleSet[4].toTuple()
    assert fetchedEvents[1].toTuple() == eventSampleSet[5].toTuple()
    assert fetchedEvents[2].toTuple() == eventSampleSet[6].toTuple()


def testGetEventsOnLayout(testEventManager, eventSampleSet):

    # ACT
    for event in eventSampleSet:
        testEventManager.insertEvent(event)
    fetchedEvents = testEventManager.getEventsOnLayout("monaco_gp")
    # ASSERT
    assert len(fetchedEvents) == 2
    assert fetchedEvents[0].toTuple() == eventSampleSet[3].toTuple()
    assert fetchedEvents[1].toTuple() == eventSampleSet[7].toTuple()


def testDeleteEvent(testEventManager, eventSampleSet):

    # ACT
    for event in eventSampleSet:
        testEventManager.insertEvent(event)
    testEventManager.deleteEvent(1, 4)
    fetchedEvent = testEventManager.getEvent(1, 4)
    fetchedEvents = testEventManager.getEvents()
    # ASSERT
    assert fetchedEvent is None
    assert len(fetchedEvents) == 7

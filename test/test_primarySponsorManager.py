from pathlib import Path
import pytest
import sys

src_path = Path(__file__).resolve().parent.parent / 'src'
db_path = src_path / 'Database'
class_path = src_path / 'Classes'
sys.path.append(str(src_path))
sys.path.append(str(db_path))
sys.path.append(str(class_path))

from enums import TargetType
from Classes.primarySponsor import PrimarySponsor
from Database.databaseManager import DatabaseManager
from Database.primarySponsorManager import PrimarySponsorManager


@pytest.fixture()
def testPSponsorManager():

    testDB = DatabaseManager("Test_DB.db")
    testManager = PrimarySponsorManager(testDB.databaseConnection)
    yield testManager
    testDB.deleteDatabase()

@pytest.fixture()
def pSponsorSampleSet():

    set = []
    set.append(PrimarySponsor((0, "Sponsor1", 18, 100000, 30000, 5, 0, 100000)))
    set.append(PrimarySponsor((1, "Sponsor2", 18, 100000, 30000, 3, 1, 250000)))
    set.append(PrimarySponsor((2, "Sponsor3", 18, 200000, 50000, 8, 2, 50000)))
    set.append(PrimarySponsor((3, "Sponsor4", 18, 400000, 20000, 6, 3, 200000)))
    set.append(PrimarySponsor((4, "Sponsor5", 18, 300000, 35000, 5, 4, 120000)))
    set.append(PrimarySponsor((5, "Sponsor6", 18, 250000, 25000, 4, 5, 100000)))
    set.append(PrimarySponsor((6, "Sponsor7", 18, 100000, 30000, 2, 0, 200000)))

    return set


def testInsertAndGetPSponsor(testPSponsorManager, pSponsorSampleSet):

    # ACT
    insertedSponsor = pSponsorSampleSet[2]
    testPSponsorManager.insertSponsor(insertedSponsor)
    fetchedSponsor = testPSponsorManager.getSponsor(insertedSponsor.id)
    # ASSERT
    assert insertedSponsor.toTuple() == fetchedSponsor.toTuple()


def testGetPSponsors(testPSponsorManager, pSponsorSampleSet):

    # ACT
    for sponsor in pSponsorSampleSet:
        testPSponsorManager.insertSponsor(sponsor)
    fetchedSponsors = testPSponsorManager.getSponsors()
    # ASSERT
    assert len(fetchedSponsors) == len(pSponsorSampleSet)
    for i in range(len(pSponsorSampleSet)):
        assert pSponsorSampleSet[i].toTuple() == fetchedSponsors[i].toTuple()


def testUpdatePSponsor(testPSponsorManager, pSponsorSampleSet):

    # ACT
    for sponsor in pSponsorSampleSet:
        testPSponsorManager.insertSponsor(sponsor)
    targetSponsor: PrimarySponsor = testPSponsorManager.getSponsor(4)
    targetSponsor.contractLength = 16
    targetSponsor.name = "NewName"
    targetSponsor.racePay = 450
    targetSponsor.signingPay = 99
    testPSponsorManager.updateSponsor(targetSponsor)
    fetchedSponsor = testPSponsorManager.getSponsor(4)
    unchangedSponsor = testPSponsorManager.getSponsor(3)
    # ASSERT
    assert targetSponsor.toTuple() == fetchedSponsor.toTuple()
    assert unchangedSponsor.toTuple() == pSponsorSampleSet[3].toTuple()


def testDeletePSponsor(testPSponsorManager, pSponsorSampleSet):

    # ACT
    for sponsor in pSponsorSampleSet:
        testPSponsorManager.insertSponsor(sponsor)
    testPSponsorManager.deleteSponsor(1)
    fetchedSponsor = testPSponsorManager.getSponsor(1)
    fetchedSponsors = testPSponsorManager.getSponsors()
    # ASSERT
    assert fetchedSponsor is None
    assert len(fetchedSponsors) == len(pSponsorSampleSet) - 1

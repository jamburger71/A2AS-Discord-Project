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
from Classes.sponsor import Sponsor
from Database.databaseManager import DatabaseManager
from Database.secondarySponsorManager import SecondarySponsorManager


@pytest.fixture()
def testSponsorManager():

    testDB = DatabaseManager("Test_DB.db")
    testManager = SecondarySponsorManager(testDB.databaseConnection)
    yield testManager
    testDB.deleteDatabase()


@pytest.fixture()
def sponsorSampleSet():

    set = []
    set.append(Sponsor((0, "Sponsor1", 18, 100000, 30000)))
    set.append(Sponsor((1, "Sponsor2", 18, 100000, 30000)))
    set.append(Sponsor((2, "Sponsor3", 18, 200000, 50000)))
    set.append(Sponsor((3, "Sponsor4", 18, 400000, 20000)))
    set.append(Sponsor((4, "Sponsor5", 18, 300000, 35000)))
    set.append(Sponsor((5, "Sponsor6", 18, 250000, 25000)))
    set.append(Sponsor((6, "Sponsor7", 18, 100000, 30000)))

    return set


def testInsertAndGetSponsor(testSponsorManager, sponsorSampleSet):

    # ACT
    insertedSponsor = sponsorSampleSet[2]
    testSponsorManager.insertSponsor(insertedSponsor)
    fetchedSponsor = testSponsorManager.getSponsor(insertedSponsor.id)
    # ASSERT
    assert insertedSponsor.toTuple() == fetchedSponsor.toTuple()


def testGetSponsors(testSponsorManager, sponsorSampleSet):

    # ACT
    for sponsor in sponsorSampleSet:
        testSponsorManager.insertSponsor(sponsor)
    fetchedSponsors = testSponsorManager.getSponsors()
    # ASSERT
    assert len(fetchedSponsors) == len(sponsorSampleSet)
    for i in range(len(sponsorSampleSet)):
        assert sponsorSampleSet[i].toTuple() == fetchedSponsors[i].toTuple()


def testUpdateSponsor(testSponsorManager, sponsorSampleSet):

    # ACT
    for sponsor in sponsorSampleSet:
        testSponsorManager.insertSponsor(sponsor)
    targetSponsor: Sponsor = testSponsorManager.getSponsor(4)
    targetSponsor.contractLength = 16
    targetSponsor.name = "NewName"
    targetSponsor.racePay = 450
    targetSponsor.signingPay = 99
    testSponsorManager.updateSponsor(targetSponsor)
    fetchedSponsor = testSponsorManager.getSponsor(4)
    unchangedSponsor = testSponsorManager.getSponsor(3)
    # ASSERT
    assert targetSponsor.toTuple() == fetchedSponsor.toTuple()
    assert unchangedSponsor.toTuple() == sponsorSampleSet[3].toTuple()


def testDeleteSponsor(testSponsorManager, sponsorSampleSet):

    # ACT
    for sponsor in sponsorSampleSet:
        testSponsorManager.insertSponsor(sponsor)
    testSponsorManager.deleteSponsor(1)
    fetchedSponsor = testSponsorManager.getSponsor(1)
    fetchedSponsors = testSponsorManager.getSponsors()
    # ASSERT
    assert fetchedSponsor is None
    assert len(fetchedSponsors) == len(sponsorSampleSet) - 1

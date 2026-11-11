from faker import Faker
import random

class Driver:

    def __init__(self, databaseData: tuple):

        self.ID = databaseData[0]
        self.isActive = databaseData[1]
        self.firstName = databaseData[2]
        self.lastName = databaseData[3]
        self.nationality = databaseData[4]
        self.age = databaseData[5]
        self.qualiPace = databaseData[6]
        self.racePace = databaseData[7]
        self.wetPace = databaseData[8]
        self.tyreManagement = databaseData[9]
        self.aggressiveness = databaseData[10]
        self.defending = databaseData[11]
        self.contractCost = databaseData[12]

    @classmethod
    def new(cls, dbinput: tuple | None):
        if dbinput is not None:
            return cls(dbinput)
        return None
    
    def toTuple(self) -> tuple:
        
        return (
            self.ID,
            self.isActive,
            self.firstName,
            self.lastName,
            self.nationality,
            self.age,
            self.qualiPace,
            self.racePace,
            self.wetPace,
            self.tyreManagement,
            self.aggressiveness,
            self.defending,
            self.contractCost,
        )

    @classmethod
    def randomDriver(cls, driverID):

        isMale = random.randint(0, 100) > 5
        faker = Faker(random.choice(localePool))
        if hasattr(faker, 'romanized_name_male'):
            if isMale:
                firstName, lastName = faker.romanized_name_male().split(' ', 1)
            else:
                firstName, lastName = faker.romanized_name_female().split(' ', 1)
        else:
            firstName = faker.first_name_male() if isMale else faker.first_name_female()
            lastName = faker.last_name()
        age = random.randint(18, 45)
        nationality = faker.country()
        baseVal = random.randint(0, 100)
        deviation = random.randint(0, 25)
        qualiPace = max(min(random.randint(baseVal-deviation, baseVal+deviation), 100), 0)
        racePace = max(min(random.randint(baseVal-deviation, baseVal+deviation), 100), 0)
        wetPace = max(min(random.randint(baseVal-deviation, baseVal+deviation), 100), 0)
        tyreManagement = max(min(random.randint(baseVal-deviation, baseVal+deviation), 100), 0)
        aggressiveness = max(min(random.randint(baseVal-deviation, baseVal+deviation), 100), 0)
        defending = max(min(random.randint(baseVal-deviation, baseVal+deviation), 100), 0)
        cost = random.randint(-10, 100)*1000

        return Driver((driverID, True, firstName, lastName, nationality, age, qualiPace, racePace, wetPace, tyreManagement, aggressiveness, defending, cost))

localeWeights = {
    'en_GB': 100,  # United Kingdom (Heartland of motorsport)
    'fr_FR': 75,   # France
    'de_DE': 70,   # Germany
    'it_IT': 65,   # Italy
    'pt_BR': 60,   # Brazil
    'en_US': 55,   # United States
    'fi_FI': 45,   # Finland
    'nl_NL': 45,   # Netherlands
    'es_ES': 40,   # Spain
    'en_AU': 40,   # Australia
    'fr_CA': 14,   # Canada (French)
    'en_CA': 11,   # Canada (English)
    'ja_JP': 25,   # Japan
    'de_AT': 20,   # Austria
    'es_MX': 15,   # Mexico
    'fr_CH': 6,    # Switzerland (French)
    'de_CH': 6,    # Switzerland (German)
    'da_DK': 10,   # Denmark
    'sv_SE': 10,   # Sweden
    'zh_CN': 8,    # China
    'en_NZ': 8,    # New Zealand
    'th_TH': 6,    # Thailand
    'en_IE': 5,    # Ireland
    'pl_PL': 5,    # Poland
    'ru_RU': 5,    # Russia
    'es_AR': 4,    # Argentina
    'nl_BE': 2,    # Belgium (Dutch)
    'fr_BE': 2,    # Belgium (French)
    'pt_PT': 3,    # Portugal
    'zu_ZA': 3,    # South Africa
    'hu_HU': 2,    # Hungary
    'cs_CZ': 2,    # Czech Republic
    'en_IN': 2,    # India
    'id_ID': 2,    # Indonesia
    'en_PH': 1,    # Philippines (English)
    'tl_PH': 1,    # Philippines (Tagalog)
    'ar_AE': 1,    # UAE
    'ar_SA': 1,    # Saudi Arabia
    'ko_KR': 1,    # South Korea
    'tr_TR': 1,    # Turkey
    'el_GR': 1,    # Greece
    'no_NO': 1,    # Norway
    'uk_UA': 1,    # Ukraine
    'ro_RO': 1,    # Romania
    'he_IL': 1,    # Israel
    'bg_BG': 1,    # Bulgaria
    'sk_SK': 1,    # Slovakia
    'hr_HR': 1,    # Croatia
    'sl_SI': 1,    # Slovenia
    'et_EE': 1,    # Estonia
    'lt_LT': 1,    # Lithuania
    'lv_LV': 1,    # Latvia
    'is_IS': 1,    # Iceland
    'mt_MT': 1,    # Malta
}

localePool = []
for locale, weight in localeWeights.items():
    localePool.extend([locale] * weight)
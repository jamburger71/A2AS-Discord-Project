

from pathlib import Path
import sys

src_path = Path(__file__).resolve().parent.parent / 'src'
db_path = src_path / 'Database'
class_path = src_path / 'Classes'
sys.path.append(str(src_path))
sys.path.append(str(db_path))
sys.path.append(str(class_path))

from Classes.driver import Driver

drivers = [
    Driver((0, "Test",     "Driver",      "DRI", "British",    27,  50,  60,  70,  80,  90,  100, 250000), True),
    Driver((1, "Michael",  "Schumacher",  "MSC", "German",     35,  95,  90,  85,  85,  95,  85,  500000), True),
    Driver((2, "Fernando", "Alonso",      "ALO", "Spanish",    32,  85,  80,  75,  75,  85,  75,  400000), True),
    Driver((3, "Kimi",     "Raikkonen",   "RAI", "Finnish",    34,  80,  75,  70,  70,  80,  70,  350000), True),
    Driver((4, "Rubens",   "Barrichello", "BAR", "Brazillian", 40,  75,  70,  65,  65,	75,	 65,  300000), True),
    Driver((5, "Jarno",    "Trulli",      "TRU", "Italian",    33,	70,	 65,  60,  60,	70,	 60,  250000), True),
]
teams = [
    ("Test Team", "British", 1000000),
    ("Ferrari", "Italian", 5000000),
    ("McLaren", "British", 4000000),
    ("Mercedes", "German", 3500000),
    ("Red Bull", "Austrian", 3000000),
    ("Williams", "British", 2500000),
]
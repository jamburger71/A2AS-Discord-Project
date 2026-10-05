import logging
import sqlite3
import yaml
import os
from contextlib import closing

class EventManager:

    def __init__(self, databaseConnection):

        swlf.DatabaseConnection = databaseConnection
import pyodide
pyodide.loadPackage("micropip")

import discord
from discord import app_commands
from discord.ext import commands
import logging
from yaml import load
try:
  from yaml import CLoader as Loader
except ImportError:
  from yaml import Loader

unparsedData = open("appMetadata.yaml").read()
metadata = load(unparsedData, Loader=Loader)

print(metadata)
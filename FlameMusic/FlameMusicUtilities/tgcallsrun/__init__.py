from os import listdir, mkdir
from pyrogram import Client
from FlameMusic import config
from FlameMusic.FlameMusicUtilities.tgcallsrun.queues import (clear, get, is_empty, put, task_done)
from FlameMusic.FlameMusicUtilities.tgcallsrun.downloader import download
from FlameMusic.FlameMusicUtilities.tgcallsrun.convert import convert
from FlameMusic.FlameMusicUtilities.tgcallsrun.music import run
from FlameMusic.FlameMusicUtilities.tgcallsrun.music import smexy as ASS_ACC
smexy = 1

__title__ = 'fluxpoint'
__author__ = 'Dhruva Shaw'
__license__ = 'GNU GENERAL PUBLIC LICENSE'
__copyright__ = 'Copyright 2021-present Dhruvacube'
__version__ = '1.0.0a'
__path__ = __import__('pkgutil').extend_path(__path__, __name__)

from typing import NamedTuple, Literal
import logging

from .http import *
from .enums import *
from .errors import *
from ._type import *
from .client import *

class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info: VersionInfo = VersionInfo(
    major=1, minor=0, micro=0, releaselevel='alpha', serial=0)

logging.getLogger(__name__).addHandler(logging.NullHandler())

del logging, NamedTuple, Literal, VersionInfo

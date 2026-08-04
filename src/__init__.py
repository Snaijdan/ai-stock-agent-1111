"""
AI Stock Agent - Main application package
"""

__version__ = "1.0.0-alpha"
__author__ = "AI Agent Stock Team"
__description__ = "TradingView-like stock analysis platform for Vietnamese stocks"

from . import data
from . import indicators

__all__ = ["data", "indicators"]

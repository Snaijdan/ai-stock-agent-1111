"""
Configuration settings for AI Stock Agent application
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent
SRC_DIR = PROJECT_ROOT / "src"
DATA_DIR = PROJECT_ROOT / "data"
CACHE_DIR = PROJECT_ROOT / ".cache"

# Create directories if they don't exist
CACHE_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

# API Configuration
VNSTOCK_BASE_URL = "https://api.vnstock.vn"
VNSTOCK_CACHE_TTL = 300  # 5 minutes in seconds
VNSTOCK_MAX_RETRIES = 3
VNSTOCK_TIMEOUT = 10

# Data Configuration
DEFAULT_PERIOD = "1y"  # 1 year of historical data
AVAILABLE_PERIODS = ["1m", "3m", "6m", "1y", "2y", "5y", "all"]
DEFAULT_TIMEFRAME = "1d"  # Daily candles
AVAILABLE_TIMEFRAMES = ["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "1M"]

# Stock Configuration
DEFAULT_STOCKS = ["VNI", "VN30", "HNX", "UPCOM"]
MAJOR_STOCKS = [
    "ACB", "AGF", "BVH", "CTG", "FPT", "GAS", "GVR", "HDB", "HPG", "KDH",
    "MBB", "MSN", "MWG", "PDR", "PNJ", "SAB", "SBT", "TCB", "TPB", "VCB",
    "VIC", "VJC", "VNM", "VPB", "VSH"
]

# Technical Analysis Configuration
TECHNICAL_INDICATORS = {
    "SMA": {"periods": [20, 50, 100, 200]},
    "EMA": {"periods": [12, 26, 50]},
    "RSI": {"period": 14, "overbought": 70, "oversold": 30},
    "MACD": {"fast": 12, "slow": 26, "signal": 9},
    "Bollinger": {"period": 20, "std_dev": 2},
    "ATR": {"period": 14},
    "ADX": {"period": 14},
    "STOCH": {"k_period": 14, "d_period": 3},
    "CCI": {"period": 20},
    "ROC": {"period": 12},
}

# Volume Analysis Configuration
VOLUME_CONFIG = {
    "MFI_PERIOD": 14,
    "CMF_PERIOD": 20,
    "OBV_PERIOD": 20,
    "AD_PERIOD": 20,
}

# Cache Configuration
CACHE_SETTINGS = {
    "enabled": True,
    "backend": "file",  # or "redis" for distributed caching
    "ttl_seconds": 300,
    "max_size_mb": 500,
}

# Chart Configuration
CHART_CONFIG = {
    "height": 600,
    "width": 1200,
    "template": "plotly_white",
    "colors": {
        "bullish": "#26a69a",
        "bearish": "#ef5350",
        "neutral": "#888888",
    },
}

# Database Configuration (optional)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///stock_data.db")
USE_DATABASE = False  # Set to True to enable database storage

# Logging Configuration
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Streamlit Configuration
STREAMLIT_PAGE_ICON = "📈"
STREAMLIT_PAGE_TITLE = "AI Stock Agent"
STREAMLIT_LAYOUT = "wide"
STREAMLIT_INITIAL_SIDEBAR_STATE = "expanded"

# Performance Configuration
MAX_WORKERS = 4  # For multi-threaded data fetching
BATCH_SIZE = 100  # Stocks per batch request
REQUEST_DELAY = 0.1  # Seconds between requests

# Alert Configuration
ALERT_ENABLED = True
ALERT_CHECK_INTERVAL = 60  # seconds

# Feature Flags
FEATURES = {
    "technical_analysis": True,
    "volume_analysis": True,
    "pattern_recognition": True,
    "ml_predictions": False,  # Enable with proper ML setup
    "backtesting": False,
    "real_time_alerts": False,
    "portfolio_tracking": False,
}

# Development Settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
DEVELOPMENT_MODE = os.getenv("ENVIRONMENT", "development") == "development"

# API Rate Limiting
RATE_LIMIT_ENABLED = True
RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_PERIOD = 60  # seconds

# Email Notification (optional)
EMAIL_ENABLED = False
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# Proxy Settings (if needed)
PROXY_ENABLED = False
PROXY_URL = os.getenv("PROXY_URL")

def get_config():
    """Return configuration as dictionary"""
    return {
        "vnstock": {
            "base_url": VNSTOCK_BASE_URL,
            "cache_ttl": VNSTOCK_CACHE_TTL,
            "retries": VNSTOCK_MAX_RETRIES,
            "timeout": VNSTOCK_TIMEOUT,
        },
        "data": {
            "default_period": DEFAULT_PERIOD,
            "available_periods": AVAILABLE_PERIODS,
            "default_timeframe": DEFAULT_TIMEFRAME,
            "available_timeframes": AVAILABLE_TIMEFRAMES,
        },
        "technical": TECHNICAL_INDICATORS,
        "volume": VOLUME_CONFIG,
        "cache": CACHE_SETTINGS,
        "chart": CHART_CONFIG,
        "features": FEATURES,
    }

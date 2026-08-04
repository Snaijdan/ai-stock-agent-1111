"""
vnstock Data Fetcher Module
Handles OHLCV data retrieval from Vietnamese stock market
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
import logging

import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
import config

logger = logging.getLogger(__name__)

class VnstockFetcher:
    """Fetch and manage Vietnamese stock data from vnstock API"""

    def __init__(self):
        self.base_url = config.VNSTOCK_BASE_URL
        self.timeout = config.VNSTOCK_TIMEOUT
        self.max_retries = config.VNSTOCK_MAX_RETRIES
        self.cache = {}
        self.cache_ttl = config.VNSTOCK_CACHE_TTL

    def fetch_ohlcv(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        timeframe: str = "1d"
    ) -> Optional[pd.DataFrame]:
        """
        Fetch OHLCV data for a stock symbol.

        Args:
            symbol: Stock symbol (e.g., 'VNI', 'VN30', 'ACB')
            start_date: Start date in format 'YYYY-MM-DD' (optional)
            end_date: End date in format 'YYYY-MM-DD' (optional)
            timeframe: Timeframe ('1m', '5m', '15m', '1h', '1d', '1w', '1M')

        Returns:
            DataFrame with columns: date, open, high, low, close, volume
            Returns None if fetch fails
        """
        try:
            # Check cache first
            cache_key = f"{symbol}_{start_date}_{end_date}_{timeframe}"
            if cache_key in self.cache:
                cached_data, timestamp = self.cache[cache_key]
                if datetime.now().timestamp() - timestamp < self.cache_ttl:
                    logger.info(f"Cache hit for {cache_key}")
                    return cached_data

            # Fetch from API (placeholder - implement actual vnstock API call)
            data = self._fetch_from_api(
                symbol, start_date, end_date, timeframe
            )

            if data is not None and not data.empty:
                # Cache the result
                self.cache[cache_key] = (data, datetime.now().timestamp())
                logger.info(f"Fetched {len(data)} candles for {symbol}")
                return data
            else:
                logger.warning(f"No data fetched for {symbol}")
                return None

        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {str(e)}")
            return None

    def _fetch_from_api(
        self,
        symbol: str,
        start_date: Optional[str],
        end_date: Optional[str],
        timeframe: str
    ) -> Optional[pd.DataFrame]:
        """
        Internal method to fetch from vnstock API.

        TODO: Implement actual vnstock API integration
        Current implementation returns sample data structure
        """
        try:
            # TODO: Replace with actual vnstock API call
            # Example using vnstock library:
            # from vnstock import stock
            # df = stock(symbol).ohlcv(start_date, end_date)

            logger.info(f"Placeholder: Would fetch {symbol} from {start_date} to {end_date}")

            # Return None for now - agent will implement this
            return None

        except Exception as e:
            logger.error(f"API fetch error: {str(e)}")
            return None

    def fetch_multiple_stocks(
        self,
        symbols: List[str],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        timeframe: str = "1d"
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch data for multiple stocks.

        Args:
            symbols: List of stock symbols
            start_date: Start date
            end_date: End date
            timeframe: Timeframe

        Returns:
            Dictionary with symbol as key and DataFrame as value
        """
        results = {}
        for symbol in symbols:
            data = self.fetch_ohlcv(symbol, start_date, end_date, timeframe)
            if data is not None:
                results[symbol] = data
        return results

    def get_intraday_data(
        self,
        symbol: str,
        days: int = 1
    ) -> Optional[pd.DataFrame]:
        """
        Get intraday data for the last N days.

        Args:
            symbol: Stock symbol
            days: Number of days to fetch

        Returns:
            DataFrame with intraday OHLCV data
        """
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        return self.fetch_ohlcv(symbol, start_date, end_date, timeframe="15m")

    def get_daily_data(
        self,
        symbol: str,
        days: int = 252
    ) -> Optional[pd.DataFrame]:
        """
        Get daily data for the last N trading days.

        Args:
            symbol: Stock symbol
            days: Number of trading days (default: 1 year = ~252 days)

        Returns:
            DataFrame with daily OHLCV data
        """
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        return self.fetch_ohlcv(symbol, start_date, end_date, timeframe="1d")

    def get_market_indices(self) -> Optional[Dict[str, float]]:
        """
        Get current market indices (VNI, VN30, HNX, UPCOM).

        Returns:
            Dictionary with index symbol as key and value as current price
        """
        try:
            # TODO: Fetch market indices from vnstock
            indices = {}
            for symbol in config.DEFAULT_STOCKS:
                # Placeholder: actual implementation needed
                indices[symbol] = None
            return indices
        except Exception as e:
            logger.error(f"Error fetching market indices: {str(e)}")
            return None

    def validate_data(self, df: pd.DataFrame) -> bool:
        """
        Validate OHLCV data integrity.

        Args:
            df: DataFrame with OHLCV data

        Returns:
            True if data is valid, False otherwise
        """
        required_cols = ['open', 'high', 'low', 'close', 'volume']

        # Check required columns
        if not all(col in df.columns for col in required_cols):
            logger.warning("Missing required columns")
            return False

        # Check for null values
        if df[required_cols].isnull().any().any():
            logger.warning("Found null values in OHLCV data")
            return False

        # Check price relationships (H >= O, L <= O, etc.)
        if (df['high'] < df['open']).any() or (df['high'] < df['close']).any():
            logger.warning("High < Open or High < Close detected")
            return False

        if (df['low'] > df['open']).any() or (df['low'] > df['close']).any():
            logger.warning("Low > Open or Low > Close detected")
            return False

        if (df['low'] > df['high']).any():
            logger.warning("Low > High detected")
            return False

        if (df['volume'] < 0).any():
            logger.warning("Negative volume detected")
            return False

        logger.info(f"Data validation passed for {len(df)} rows")
        return True

    def clear_cache(self, symbol: Optional[str] = None):
        """
        Clear cache entries.

        Args:
            symbol: If provided, only clear cache for this symbol. Otherwise clear all.
        """
        if symbol:
            keys_to_remove = [k for k in self.cache.keys() if k.startswith(symbol)]
            for key in keys_to_remove:
                del self.cache[key]
            logger.info(f"Cleared cache for {symbol}")
        else:
            self.cache.clear()
            logger.info("Cleared entire cache")

    def get_cache_size(self) -> int:
        """Get number of cached entries"""
        return len(self.cache)


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)

    fetcher = VnstockFetcher()

    # Example: Fetch VNI data for the last year
    data = fetcher.get_daily_data("VNI", days=365)
    if data is not None:
        print(f"Fetched {len(data)} days of data")
        print(data.head())
    else:
        print("Failed to fetch data - vnstock API integration needed")

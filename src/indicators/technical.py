"""
Technical Analysis Indicators Module
Implements various technical indicators for stock analysis
"""
import sys
from pathlib import Path
from typing import Optional, Tuple
import logging

import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
import config

logger = logging.getLogger(__name__)

class TechnicalAnalyzer:
    """Calculate technical indicators for stock analysis"""

    def __init__(self, data: pd.DataFrame):
        """
        Initialize analyzer with OHLCV data.

        Args:
            data: DataFrame with columns: open, high, low, close, volume
        """
        self.data = data.copy()
        self.validate_data()

    def validate_data(self) -> bool:
        """Validate data has required columns"""
        required = ['open', 'high', 'low', 'close', 'volume']
        if not all(col in self.data.columns for col in required):
            raise ValueError(f"Data missing required columns: {required}")
        return True

    # ===== Moving Average Indicators =====

    def calculate_sma(self, period: int = 20) -> pd.Series:
        """
        Simple Moving Average.

        Args:
            period: Number of periods for SMA

        Returns:
            Series with SMA values
        """
        return self.data['close'].rolling(window=period).mean()

    def calculate_ema(self, period: int = 12) -> pd.Series:
        """
        Exponential Moving Average.

        Args:
            period: Number of periods for EMA

        Returns:
            Series with EMA values
        """
        return self.data['close'].ewm(span=period, adjust=False).mean()

    # ===== Momentum Indicators =====

    def calculate_rsi(self, period: int = 14) -> pd.Series:
        """
        Relative Strength Index (RSI).

        RSI = 100 - (100 / (1 + RS))
        RS = Average Gain / Average Loss

        Args:
            period: Number of periods for RSI

        Returns:
            Series with RSI values (0-100)
        """
        delta = self.data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def calculate_macd(
        self,
        fast: int = 12,
        slow: int = 26,
        signal: int = 9
    ) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        MACD (Moving Average Convergence Divergence).

        Args:
            fast: Fast EMA period
            slow: Slow EMA period
            signal: Signal line EMA period

        Returns:
            Tuple of (MACD line, Signal line, Histogram)
        """
        ema_fast = self.data['close'].ewm(span=fast, adjust=False).mean()
        ema_slow = self.data['close'].ewm(span=slow, adjust=False).mean()

        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        histogram = macd_line - signal_line

        return macd_line, signal_line, histogram

    def calculate_stochastic(
        self,
        k_period: int = 14,
        d_period: int = 3
    ) -> Tuple[pd.Series, pd.Series]:
        """
        Stochastic Oscillator.

        %K = (Close - Lowest Low) / (Highest High - Lowest Low) * 100
        %D = 3-period SMA of %K

        Args:
            k_period: Period for K line
            d_period: Period for D line (SMA)

        Returns:
            Tuple of (%K, %D)
        """
        low_min = self.data['low'].rolling(window=k_period).min()
        high_max = self.data['high'].rolling(window=k_period).max()

        k_percent = ((self.data['close'] - low_min) / (high_max - low_min) * 100)
        d_percent = k_percent.rolling(window=d_period).mean()

        return k_percent, d_percent

    # ===== Volatility Indicators =====

    def calculate_bollinger_bands(
        self,
        period: int = 20,
        std_dev: float = 2.0
    ) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Bollinger Bands.

        Args:
            period: SMA period
            std_dev: Standard deviations for bands

        Returns:
            Tuple of (Middle band (SMA), Upper band, Lower band)
        """
        middle = self.data['close'].rolling(window=period).mean()
        std = self.data['close'].rolling(window=period).std()

        upper = middle + (std_dev * std)
        lower = middle - (std_dev * std)

        return middle, upper, lower

    def calculate_atr(self, period: int = 14) -> pd.Series:
        """
        Average True Range (ATR).

        Measures volatility.

        Args:
            period: ATR period

        Returns:
            Series with ATR values
        """
        # Calculate True Range
        high_low = self.data['high'] - self.data['low']
        high_close = np.abs(self.data['high'] - self.data['close'].shift())
        low_close = np.abs(self.data['low'] - self.data['close'].shift())

        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)

        # Calculate ATR
        atr = true_range.rolling(window=period).mean()
        return atr

    def calculate_adx(self, period: int = 14) -> pd.Series:
        """
        Average Directional Index (ADX).

        Measures trend strength (0-100).

        Args:
            period: ADX period

        Returns:
            Series with ADX values
        """
        # Calculate directional movements
        up_move = self.data['high'].diff()
        down_move = -self.data['low'].diff()

        pos_dm = up_move.where((up_move > down_move) & (up_move > 0), 0)
        neg_dm = down_move.where((down_move > up_move) & (down_move > 0), 0)

        # Calculate ATR
        high_low = self.data['high'] - self.data['low']
        high_close = np.abs(self.data['high'] - self.data['close'].shift())
        low_close = np.abs(self.data['low'] - self.data['close'].shift())
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = true_range.rolling(window=period).mean()

        # Calculate DI+ and DI-
        di_pos = 100 * (pos_dm.rolling(window=period).mean() / atr)
        di_neg = 100 * (neg_dm.rolling(window=period).mean() / atr)

        # Calculate ADX
        di_diff = np.abs(di_pos - di_neg)
        di_sum = di_pos + di_neg
        dx = 100 * (di_diff / di_sum)
        adx = dx.rolling(window=period).mean()

        return adx

    # ===== Support/Resistance =====

    def calculate_support_resistance(self, window: int = 20) -> Tuple[pd.Series, pd.Series]:
        """
        Calculate support and resistance levels.

        Support = Lowest low in window
        Resistance = Highest high in window

        Args:
            window: Lookback window

        Returns:
            Tuple of (Support levels, Resistance levels)
        """
        support = self.data['low'].rolling(window=window).min()
        resistance = self.data['high'].rolling(window=window).max()
        return support, resistance

    # ===== Trend Analysis =====

    def calculate_trend_direction(self, fast_ma: int = 12, slow_ma: int = 26) -> pd.Series:
        """
        Simple trend direction based on moving averages.

        Returns:
            Series with values: 1 (Uptrend), -1 (Downtrend), 0 (Neutral)
        """
        fast = self.calculate_ema(period=fast_ma)
        slow = self.calculate_ema(period=slow_ma)

        trend = pd.Series(0, index=self.data.index)
        trend[fast > slow] = 1
        trend[fast < slow] = -1

        return trend

    # ===== Price Action =====

    def calculate_roc(self, period: int = 12) -> pd.Series:
        """
        Rate of Change (ROC).

        Measures momentum as percentage change.

        Args:
            period: ROC period

        Returns:
            Series with ROC values
        """
        roc = ((self.data['close'] - self.data['close'].shift(period)) /
               self.data['close'].shift(period) * 100)
        return roc

    def calculate_cci(self, period: int = 20) -> pd.Series:
        """
        Commodity Channel Index (CCI).

        Identifies cyclical trends.

        Args:
            period: CCI period

        Returns:
            Series with CCI values
        """
        typical_price = (self.data['high'] + self.data['low'] + self.data['close']) / 3
        sma = typical_price.rolling(window=period).mean()
        mad = typical_price.rolling(window=period).apply(
            lambda x: np.mean(np.abs(x - np.mean(x)))
        )

        cci = (typical_price - sma) / (0.015 * mad)
        return cci

    # ===== Analysis Summary =====

    def calculate_all_indicators(self) -> dict:
        """
        Calculate all key technical indicators.

        Returns:
            Dictionary with all indicator values
        """
        indicators = {
            'sma_20': self.calculate_sma(20),
            'sma_50': self.calculate_sma(50),
            'sma_200': self.calculate_sma(200),
            'ema_12': self.calculate_ema(12),
            'ema_26': self.calculate_ema(26),
            'rsi_14': self.calculate_rsi(14),
            'macd': self.calculate_macd(),
            'bollinger': self.calculate_bollinger_bands(),
            'atr_14': self.calculate_atr(14),
            'support_resistance': self.calculate_support_resistance(),
            'trend': self.calculate_trend_direction(),
            'roc_12': self.calculate_roc(12),
            'cci_20': self.calculate_cci(20),
        }
        return indicators

    def get_latest_values(self) -> dict:
        """Get latest values for key indicators"""
        if len(self.data) < 200:
            logger.warning("Not enough data for all indicators")
            return {}

        values = {
            'price': self.data['close'].iloc[-1],
            'sma_20': self.calculate_sma(20).iloc[-1],
            'sma_50': self.calculate_sma(50).iloc[-1],
            'sma_200': self.calculate_sma(200).iloc[-1],
            'rsi_14': self.calculate_rsi(14).iloc[-1],
            'atr_14': self.calculate_atr(14).iloc[-1],
            'volume': self.data['volume'].iloc[-1],
        }
        return values


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)

    # Create sample data
    dates = pd.date_range(start='2023-01-01', periods=100)
    sample_data = pd.DataFrame({
        'open': np.random.randn(100).cumsum() + 100,
        'high': np.random.randn(100).cumsum() + 102,
        'low': np.random.randn(100).cumsum() + 98,
        'close': np.random.randn(100).cumsum() + 100,
        'volume': np.random.randint(1000, 10000, 100),
    }, index=dates)

    analyzer = TechnicalAnalyzer(sample_data)
    rsi = analyzer.calculate_rsi()
    sma = analyzer.calculate_sma(20)

    print(f"Latest RSI: {rsi.iloc[-1]:.2f}")
    print(f"Latest SMA(20): {sma.iloc[-1]:.2f}")

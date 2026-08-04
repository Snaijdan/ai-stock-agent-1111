"""
VN Market Liquidity Analyzer
Analyzes bid-ask spread, order book depth, and liquidity quality
"""
import sys
from pathlib import Path
from typing import Optional, Dict, Tuple
import logging

import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
import config

logger = logging.getLogger(__name__)

class VNLiquidityAnalyzer:
    """Analyze Vietnamese market liquidity characteristics"""

    def __init__(self, data: pd.DataFrame):
        """
        Initialize with OHLCV data.

        Args:
            data: DataFrame with open, high, low, close, volume
        """
        self.data = data.copy()
        self.validate_data()

    def validate_data(self) -> bool:
        """Validate data has required columns"""
        required = ['open', 'high', 'low', 'close', 'volume']
        if not all(col in self.data.columns for col in required):
            raise ValueError(f"Data missing required columns: {required}")
        return True

    def estimate_spread(self, window: int = 20) -> pd.Series:
        """
        Estimate bid-ask spread based on high-low range.

        For stocks with no direct bid-ask data, estimate from candle body.
        Actual spread usually smaller than half of daily range.

        Args:
            window: Lookback period for average calculation

        Returns:
            Series with estimated spread (in VND)
        """
        # High-Low range as proxy for spread
        range_series = self.data['high'] - self.data['low']

        # Average spread estimation (typically 10-30% of range)
        avg_range = range_series.rolling(window=window).mean()
        estimated_spread = avg_range * 0.15  # Estimate 15% of range as spread

        return estimated_spread

    def get_spread_quality(self, current_spread: float, historical_avg: float) -> str:
        """
        Assess spread quality.

        Args:
            current_spread: Current spread value
            historical_avg: Historical average spread

        Returns:
            Quality assessment: 'excellent', 'good', 'fair', 'poor'
        """
        ratio = current_spread / historical_avg if historical_avg > 0 else 1

        if ratio < 0.8:
            return 'excellent'  # 20% tighter than average
        elif ratio < 1.0:
            return 'good'  # At or better than average
        elif ratio < 1.2:
            return 'fair'  # 20% wider than average
        else:
            return 'poor'  # >20% wider (avoid entry)

    def calculate_volume_by_price(self, bins: int = 20) -> Dict:
        """
        Calculate volume distribution across price levels.

        Args:
            bins: Number of price bins

        Returns:
            Dictionary with price levels and associated volume
        """
        min_price = self.data['low'].min()
        max_price = self.data['high'].max()

        price_bins = np.linspace(min_price, max_price, bins)
        volume_by_price = {}

        for i in range(len(price_bins) - 1):
            bin_start = price_bins[i]
            bin_end = price_bins[i + 1]
            bin_mid = (bin_start + bin_end) / 2

            # Count how many candles have price in this range
            in_range = ((self.data['low'] <= bin_end) & (self.data['high'] >= bin_start))
            bin_volume = self.data.loc[in_range, 'volume'].sum()

            if bin_volume > 0:
                volume_by_price[bin_mid] = bin_volume

        return volume_by_price

    def find_poc(self) -> Tuple[float, float]:
        """
        Find Point of Control (price level with most volume).

        Returns:
            Tuple of (price_level, volume_at_level)
        """
        volume_by_price = self.calculate_volume_by_price(bins=50)

        if not volume_by_price:
            return None, None

        poc_price = max(volume_by_price, key=volume_by_price.get)
        poc_volume = volume_by_price[poc_price]

        return poc_price, poc_volume

    def find_liquidity_zones(self, threshold_percentile: int = 75) -> Dict:
        """
        Identify thick and thin liquidity zones.

        Args:
            threshold_percentile: Percentile for thick liquidity

        Returns:
            Dictionary with 'thick' and 'thin' zones
        """
        volume_by_price = self.calculate_volume_by_price(bins=30)

        if not volume_by_price:
            return {'thick': [], 'thin': []}

        volumes = list(volume_by_price.values())
        threshold = np.percentile(volumes, threshold_percentile)

        thick_zones = [price for price, vol in volume_by_price.items() if vol >= threshold]
        thin_zones = [price for price, vol in volume_by_price.items() if vol < np.percentile(volumes, 25)]

        return {
            'thick_zones': sorted(thick_zones),
            'thin_zones': sorted(thin_zones),
            'threshold_volume': float(threshold),
        }

    def calculate_liquidity_score(self, period: int = 20) -> pd.Series:
        """
        Calculate overall liquidity score (0-100).

        Higher = more liquid (easier to trade)
        Lower = less liquid (harder to trade, higher slippage)

        Args:
            period: Lookback period

        Returns:
            Series with liquidity scores
        """
        # Factors in liquidity score:
        # 1. Volume (higher = more liquid)
        # 2. Spread (lower = more liquid)
        # 3. Volatility (lower = more liquid)

        # Normalize volume (higher is better)
        avg_volume = self.data['volume'].rolling(window=period).mean()
        volume_score = (self.data['volume'] / (avg_volume + 1)) * 50  # 0-50 points

        # Normalize spread (lower is better)
        spread = self.estimate_spread(period)
        avg_spread = spread.rolling(window=period).mean()
        spread_ratio = spread / (avg_spread + 0.001)
        spread_score = (1 / spread_ratio.clip(lower=0.1)) * 25  # 0-25 points

        # Normalize volatility (lower is better)
        volatility = self.data['close'].pct_change().rolling(window=period).std()
        avg_volatility = volatility.rolling(window=period).mean()
        vol_ratio = volatility / (avg_volatility + 0.0001)
        volatility_score = (1 / vol_ratio.clip(lower=0.1)) * 25  # 0-25 points

        # Combined score
        liquidity_score = (
            volume_score.fillna(0) +
            spread_score.fillna(0) +
            volatility_score.fillna(0)
        ).clip(0, 100)

        return liquidity_score

    def detect_large_orders(self, volume_threshold: int = 50000) -> pd.DataFrame:
        """
        Detect potential large orders based on volume spikes.

        Args:
            volume_threshold: Volume size to consider as 'large'

        Returns:
            DataFrame with large order candles
        """
        large_orders = self.data[self.data['volume'] > volume_threshold].copy()

        if not large_orders.empty:
            large_orders['volume_rank'] = large_orders['volume'].rank(ascending=False)

        return large_orders

    def calculate_order_imbalance(self, period: int = 20) -> pd.Series:
        """
        Calculate buying vs selling pressure.

        Positive = more buying pressure
        Negative = more selling pressure

        Args:
            period: Lookback period

        Returns:
            Series with imbalance values (-1 to 1)
        """
        # Proxy: use close vs open
        close_up = (self.data['close'] > self.data['open']).astype(int)
        close_down = (self.data['close'] < self.data['open']).astype(int)

        buying_candles = close_up.rolling(window=period).sum()
        selling_candles = close_down.rolling(window=period).sum()

        imbalance = (buying_candles - selling_candles) / period

        return imbalance.clip(-1, 1)

    def estimate_slippage(self, order_size: int, price: float) -> Dict:
        """
        Estimate slippage cost for given order size.

        Args:
            order_size: Number of shares to buy/sell
            price: Current price

        Returns:
            Dictionary with slippage metrics
        """
        # Estimate based on volume liquidity
        avg_volume = self.data['volume'].mean()
        volume_ratio = order_size / avg_volume

        # Slippage increases with order size
        if volume_ratio < 0.1:
            slippage_pct = 0.02  # 0.02% for small orders
        elif volume_ratio < 0.5:
            slippage_pct = 0.05  # 0.05% for medium orders
        elif volume_ratio < 1.0:
            slippage_pct = 0.10  # 0.10% for large orders
        else:
            slippage_pct = 0.20  # 0.20%+ for very large orders

        slippage_amount = price * slippage_pct / 100

        return {
            'order_size': order_size,
            'price': price,
            'volume_ratio': volume_ratio,
            'estimated_slippage_pct': slippage_pct,
            'estimated_slippage_vnd': slippage_amount,
            'total_cost': price * order_size + (slippage_amount * order_size),
        }

    def get_best_entry_level(self, order_size: int) -> Dict:
        """
        Recommend best entry level considering liquidity.

        Args:
            order_size: Desired order size

        Returns:
            Recommendation with best entry point
        """
        liquidity_score = self.calculate_liquidity_score()
        latest_score = liquidity_score.iloc[-1]

        if latest_score < 30:
            recommendation = 'WAIT'
            reason = 'Poor liquidity - avoid entry now'
        elif latest_score < 50:
            recommendation = 'SPLIT_ORDERS'
            reason = 'Fair liquidity - split order into smaller parts'
        else:
            recommendation = 'ENTRY_OK'
            reason = 'Good liquidity - safe to enter'

        current_price = self.data['close'].iloc[-1]
        slippage = self.estimate_slippage(order_size, current_price)

        return {
            'recommendation': recommendation,
            'reason': reason,
            'liquidity_score': latest_score,
            'current_price': current_price,
            'slippage_estimate': slippage,
            'order_size': order_size,
        }

    def get_liquidity_summary(self) -> Dict:
        """Get comprehensive liquidity analysis"""
        latest_price = self.data['close'].iloc[-1]
        latest_volume = self.data['volume'].iloc[-1]
        avg_volume = self.data['volume'].mean()
        spread = self.estimate_spread().iloc[-1]
        liquidity_score = self.calculate_liquidity_score().iloc[-1]
        poc, poc_volume = self.find_poc()
        imbalance = self.calculate_order_imbalance().iloc[-1]

        return {
            'latest_price': latest_price,
            'latest_volume': latest_volume,
            'average_volume': avg_volume,
            'volume_trend': 'increasing' if latest_volume > avg_volume else 'decreasing',
            'estimated_spread': spread,
            'liquidity_score': liquidity_score,
            'liquidity_status': 'good' if liquidity_score > 60 else ('fair' if liquidity_score > 40 else 'poor'),
            'point_of_control': poc,
            'poc_volume': poc_volume,
            'order_imbalance': imbalance,
            'buying_pressure': 'strong' if imbalance > 0.2 else ('weak' if imbalance < -0.2 else 'balanced'),
        }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("VN Liquidity Analyzer - Ready for implementation")

"""
VN Market Alert System
Generates actionable trading alerts for Vietnamese stock market
"""
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import logging

import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
import config

logger = logging.getLogger(__name__)

class Alert:
    """Represents a trading alert"""

    PRIORITY_LEVELS = ['INFO', 'ATTENTION', 'WARNING', 'CRITICAL']

    def __init__(
        self,
        symbol: str,
        alert_type: str,
        message: str,
        priority: str = 'ATTENTION',
        timestamp: Optional[datetime] = None,
        price: Optional[float] = None,
        action: Optional[str] = None
    ):
        self.symbol = symbol
        self.alert_type = alert_type
        self.message = message
        self.priority = priority
        self.timestamp = timestamp or datetime.now()
        self.price = price
        self.action = action  # BUY, SELL, WAIT, ATTENTION

    def __repr__(self) -> str:
        return (f"[{self.priority}] {self.symbol} - {self.alert_type} @ {self.price} "
                f"| {self.message} | Action: {self.action}")

    def to_dict(self) -> Dict:
        return {
            'symbol': self.symbol,
            'alert_type': self.alert_type,
            'message': self.message,
            'priority': self.priority,
            'timestamp': self.timestamp,
            'price': self.price,
            'action': self.action,
        }


class VNAlertGenerator:
    """Generate alerts for VN stock trading"""

    def __init__(self, symbol: str, data: pd.DataFrame):
        """
        Initialize alert generator.

        Args:
            symbol: Stock symbol
            data: OHLCV DataFrame
        """
        self.symbol = symbol
        self.data = data.copy()
        self.alerts: List[Alert] = []
        self.validate_data()

    def validate_data(self) -> bool:
        """Validate data"""
        required = ['open', 'high', 'low', 'close', 'volume']
        if not all(col in self.data.columns for col in required):
            raise ValueError(f"Data missing required columns")
        return True

    # ===== Breakout Alerts =====

    def check_resistance_breakout(self, resistance_level: float, volume_multiplier: float = 1.2) -> Optional[Alert]:
        """
        Alert on resistance breakout with volume confirmation.

        Args:
            resistance_level: Resistance price level
            volume_multiplier: Volume must exceed average by this factor

        Returns:
            Alert if breakout detected, None otherwise
        """
        current_price = self.data['close'].iloc[-1]
        current_volume = self.data['volume'].iloc[-1]
        avg_volume = self.data['volume'].tail(20).mean()

        if current_price > resistance_level and current_volume > avg_volume * volume_multiplier:
            alert = Alert(
                symbol=self.symbol,
                alert_type='RESISTANCE_BREAKOUT',
                message=f'Breakout above resistance {resistance_level} with volume confirmation',
                priority='WARNING',
                price=current_price,
                action='BUY'
            )
            return alert

        return None

    def check_support_breakdown(self, support_level: float, volume_multiplier: float = 1.2) -> Optional[Alert]:
        """
        Alert on support breakdown with volume confirmation.

        Args:
            support_level: Support price level
            volume_multiplier: Volume must exceed average by this factor

        Returns:
            Alert if breakdown detected, None otherwise
        """
        current_price = self.data['close'].iloc[-1]
        current_volume = self.data['volume'].iloc[-1]
        avg_volume = self.data['volume'].tail(20).mean()

        if current_price < support_level and current_volume > avg_volume * volume_multiplier:
            alert = Alert(
                symbol=self.symbol,
                alert_type='SUPPORT_BREAKDOWN',
                message=f'Breakdown below support {support_level} with volume confirmation',
                priority='WARNING',
                price=current_price,
                action='SELL'
            )
            return alert

        return None

    # ===== Volume Alerts =====

    def check_volume_spike(self, multiplier: float = 2.0) -> Optional[Alert]:
        """
        Alert on unusually high volume.

        Args:
            multiplier: Volume spike threshold (X times average)

        Returns:
            Alert if volume spike detected
        """
        current_volume = self.data['volume'].iloc[-1]
        avg_volume = self.data['volume'].tail(20).mean()

        if current_volume > avg_volume * multiplier:
            spike_ratio = current_volume / avg_volume
            alert = Alert(
                symbol=self.symbol,
                alert_type='VOLUME_SPIKE',
                message=f'Unusual volume: {spike_ratio:.1f}x average ({current_volume:.0f} vs {avg_volume:.0f})',
                priority='ATTENTION',
                price=self.data['close'].iloc[-1],
                action='ATTENTION'
            )
            return alert

        return None

    # ===== Session Alerts =====

    def check_close_volume_alert(self, threshold: float = 1.5) -> Optional[Alert]:
        """
        Alert when close volume is significantly higher than average.

        Indicates strong close direction.

        Args:
            threshold: Volume multiplier threshold

        Returns:
            Alert if close volume is elevated
        """
        # Assuming last candle is close (final 15 minutes)
        close_volume = self.data['volume'].iloc[-1]
        prev_avg_volume = self.data['volume'].iloc[-20:-1].mean()

        if close_volume > prev_avg_volume * threshold:
            direction = 'UP' if self.data['close'].iloc[-1] > self.data['open'].iloc[-1] else 'DOWN'
            alert = Alert(
                symbol=self.symbol,
                alert_type='STRONG_CLOSE',
                message=f'Strong close {direction} with {close_volume/prev_avg_volume:.1f}x volume',
                priority='WARNING',
                price=self.data['close'].iloc[-1],
                action='BUY' if direction == 'UP' else 'SELL'
            )
            return alert

        return None

    # ===== Momentum Alerts =====

    def check_price_momentum(self, period: int = 5) -> Optional[Alert]:
        """
        Alert on strong price momentum.

        Args:
            period: Period for momentum calculation

        Returns:
            Alert if strong momentum detected
        """
        if len(self.data) < period:
            return None

        momentum = (self.data['close'].iloc[-1] - self.data['close'].iloc[-period]) / self.data['close'].iloc[-period]

        if abs(momentum) > 0.02:  # 2% move
            direction = 'UP' if momentum > 0 else 'DOWN'
            alert = Alert(
                symbol=self.symbol,
                alert_type='STRONG_MOMENTUM',
                message=f'Strong {direction} momentum: {abs(momentum)*100:.2f}% in {period} candles',
                priority='ATTENTION',
                price=self.data['close'].iloc[-1],
                action='BUY' if direction == 'UP' else 'SELL'
            )
            return alert

        return None

    # ===== Spread/Liquidity Alerts =====

    def check_wide_spread_alert(self, spread_threshold: float = None) -> Optional[Alert]:
        """
        Alert when spread is unusually wide.

        Avoid entries with wide spread.

        Args:
            spread_threshold: Maximum acceptable spread percentage

        Returns:
            Alert if spread is too wide
        """
        current_range = self.data['high'].iloc[-1] - self.data['low'].iloc[-1]
        avg_range = self.data['high'].tail(20).sub(self.data['low'].tail(20)).mean()

        if current_range > avg_range * 1.5:
            alert = Alert(
                symbol=self.symbol,
                alert_type='WIDE_SPREAD',
                message=f'Wide spread detected: {current_range:.0f} vs avg {avg_range:.0f}',
                priority='ATTENTION',
                price=self.data['close'].iloc[-1],
                action='WAIT'
            )
            return alert

        return None

    # ===== Trend Alerts =====

    def check_trend_reversal(self, ma_period_fast: int = 12, ma_period_slow: int = 26) -> Optional[Alert]:
        """
        Alert on potential trend reversal (MA crossover).

        Args:
            ma_period_fast: Fast MA period
            ma_period_slow: Slow MA period

        Returns:
            Alert if MA crossover detected
        """
        if len(self.data) < ma_period_slow:
            return None

        fast_ma = self.data['close'].ewm(span=ma_period_fast, adjust=False).mean()
        slow_ma = self.data['close'].ewm(span=ma_period_slow, adjust=False).mean()

        current_fast = fast_ma.iloc[-1]
        current_slow = slow_ma.iloc[-1]
        prev_fast = fast_ma.iloc[-2]
        prev_slow = slow_ma.iloc[-2]

        # Check for crossover
        if prev_fast <= prev_slow and current_fast > current_slow:
            alert = Alert(
                symbol=self.symbol,
                alert_type='BULLISH_CROSSOVER',
                message=f'Bullish MA crossover: Fast MA crossed above Slow MA',
                priority='WARNING',
                price=self.data['close'].iloc[-1],
                action='BUY'
            )
            return alert

        elif prev_fast >= prev_slow and current_fast < current_slow:
            alert = Alert(
                symbol=self.symbol,
                alert_type='BEARISH_CROSSOVER',
                message=f'Bearish MA crossover: Fast MA crossed below Slow MA',
                priority='WARNING',
                price=self.data['close'].iloc[-1],
                action='SELL'
            )
            return alert

        return None

    # ===== Level Alerts =====

    def check_level_test(self, level: float, tolerance: float = 0.01) -> Optional[Alert]:
        """
        Alert when price approaches or tests a level.

        Args:
            level: Price level to monitor
            tolerance: Price tolerance (in %)

        Returns:
            Alert if level is being tested
        """
        current_price = self.data['close'].iloc[-1]
        tolerance_amount = level * tolerance

        if abs(current_price - level) < tolerance_amount:
            if current_price > level:
                alert = Alert(
                    symbol=self.symbol,
                    alert_type='RESISTANCE_TEST',
                    message=f'Price testing resistance at {level}',
                    priority='ATTENTION',
                    price=current_price,
                    action='ATTENTION'
                )
            else:
                alert = Alert(
                    symbol=self.symbol,
                    alert_type='SUPPORT_TEST',
                    message=f'Price testing support at {level}',
                    priority='ATTENTION',
                    price=current_price,
                    action='ATTENTION'
                )
            return alert

        return None

    # ===== Generate All Alerts =====

    def generate_all_alerts(self, resistance: Optional[float] = None, support: Optional[float] = None) -> List[Alert]:
        """
        Generate all applicable alerts.

        Args:
            resistance: Resistance level to monitor
            support: Support level to monitor

        Returns:
            List of active alerts
        """
        self.alerts = []

        # Check all alert types
        alerts_to_check = [
            self.check_volume_spike(),
            self.check_close_volume_alert(),
            self.check_price_momentum(),
            self.check_wide_spread_alert(),
            self.check_trend_reversal(),
        ]

        if resistance:
            alerts_to_check.append(self.check_resistance_breakout(resistance))

        if support:
            alerts_to_check.append(self.check_support_breakdown(support))

        # Filter out None values
        self.alerts = [alert for alert in alerts_to_check if alert is not None]

        return self.alerts

    def get_priority_alerts(self) -> List[Alert]:
        """Get only high-priority alerts"""
        priority_alerts = [a for a in self.alerts if a.priority in ['WARNING', 'CRITICAL']]
        return sorted(priority_alerts, key=lambda x: ['CRITICAL', 'WARNING'].index(x.priority))

    def get_alert_summary(self) -> Dict:
        """Get alert summary"""
        if not self.alerts:
            return {
                'total_alerts': 0,
                'critical': 0,
                'warning': 0,
                'attention': 0,
                'alerts': []
            }

        summary = {
            'total_alerts': len(self.alerts),
            'critical': len([a for a in self.alerts if a.priority == 'CRITICAL']),
            'warning': len([a for a in self.alerts if a.priority == 'WARNING']),
            'attention': len([a for a in self.alerts if a.priority == 'ATTENTION']),
            'alerts': [a.to_dict() for a in self.alerts],
        }

        return summary


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("VN Alert System - Ready for implementation")

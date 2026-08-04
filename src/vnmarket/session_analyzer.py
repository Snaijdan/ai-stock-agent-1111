"""
VN Market Session Analyzer
Analyzes volume and price patterns within VN trading sessions
"""
import sys
from pathlib import Path
from datetime import datetime, time
from typing import Optional, Tuple, Dict
import logging

import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
import config

logger = logging.getLogger(__name__)

class VNSessionAnalyzer:
    """Analyze Vietnamese market trading sessions"""

    # VN Market session times (in HH:MM format)
    MORNING_START = time(9, 15)
    MORNING_END = time(11, 30)
    AFTERNOON_START = time(13, 0)
    AFTERNOON_END = time(15, 0)
    ATO_START = time(9, 15)
    ATO_END = time(9, 30)
    CLOSE_START = time(14, 45)
    CLOSE_END = time(15, 0)

    def __init__(self, data: pd.DataFrame):
        """
        Initialize with intraday data (1-minute or 5-minute candles).

        Args:
            data: DataFrame with datetime index and OHLCV columns
        """
        self.data = data.copy()
        self.data.index = pd.to_datetime(self.data.index)
        self.validate_data()

    def validate_data(self) -> bool:
        """Validate data has required columns"""
        required = ['open', 'high', 'low', 'close', 'volume']
        if not all(col in self.data.columns for col in required):
            raise ValueError(f"Data missing required columns: {required}")
        return True

    def get_session_data(self, session: str = 'morning') -> pd.DataFrame:
        """
        Get data for specific session.

        Args:
            session: 'morning', 'afternoon', 'ato', or 'close'

        Returns:
            DataFrame with session data
        """
        session = session.lower()

        if session == 'morning':
            start_time, end_time = self.MORNING_START, self.MORNING_END
        elif session == 'afternoon':
            start_time, end_time = self.AFTERNOON_START, self.AFTERNOON_END
        elif session == 'ato':
            start_time, end_time = self.ATO_START, self.ATO_END
        elif session == 'close':
            start_time, end_time = self.CLOSE_START, self.CLOSE_END
        else:
            raise ValueError(f"Invalid session: {session}")

        session_data = self.data[
            (self.data.index.time >= start_time) &
            (self.data.index.time < end_time)
        ]

        return session_data

    def analyze_session(self, session: str = 'morning') -> Dict:
        """
        Analyze specific session metrics.

        Args:
            session: 'morning', 'afternoon', 'ato', or 'close'

        Returns:
            Dictionary with session metrics
        """
        session_data = self.get_session_data(session)

        if session_data.empty:
            return {}

        metrics = {
            'session': session,
            'open': session_data['open'].iloc[0],
            'high': session_data['high'].max(),
            'low': session_data['low'].min(),
            'close': session_data['close'].iloc[-1],
            'volume': session_data['volume'].sum(),
            'candles': len(session_data),
            'range': session_data['high'].max() - session_data['low'].min(),
            'direction': 'bullish' if session_data['close'].iloc[-1] > session_data['open'].iloc[0] else 'bearish',
        }

        return metrics

    def get_all_sessions(self) -> Dict[str, Dict]:
        """Get metrics for all sessions"""
        sessions = {}
        for session in ['ato', 'morning', 'afternoon', 'close']:
            sessions[session] = self.analyze_session(session)
        return sessions

    def compare_sessions(self) -> Dict:
        """
        Compare morning vs afternoon.

        Returns:
            Comparison metrics
        """
        morning = self.analyze_session('morning')
        afternoon = self.analyze_session('afternoon')

        if not morning or not afternoon:
            return {}

        comparison = {
            'morning_volume': morning.get('volume', 0),
            'afternoon_volume': afternoon.get('volume', 0),
            'morning_direction': morning.get('direction', 'unknown'),
            'afternoon_direction': afternoon.get('direction', 'unknown'),
            'volume_ratio': (afternoon.get('volume', 0) / max(morning.get('volume', 1), 1)) if morning.get('volume') else 0,
            'morning_range': morning.get('range', 0),
            'afternoon_range': afternoon.get('range', 0),
            'correlation': self._calculate_direction_correlation(morning, afternoon),
        }

        return comparison

    def _calculate_direction_correlation(self, morning: Dict, afternoon: Dict) -> str:
        """
        Determine if afternoon continues or reverses morning trend.

        Returns:
            'continuation', 'reversal', or 'mixed'
        """
        if not morning or not afternoon:
            return 'unknown'

        morning_dir = morning.get('direction')
        afternoon_dir = afternoon.get('direction')

        if morning_dir == afternoon_dir:
            return 'continuation'
        else:
            return 'reversal'

    def get_ato_analysis(self) -> Dict:
        """
        Analyze ATO (opening auction) metrics.

        Returns:
            ATO metrics and signals
        """
        ato_data = self.get_session_data('ato')

        if ato_data.empty:
            return {}

        # Get previous close for comparison
        prev_close = self.data['close'].iloc[0] if len(self.data) > 0 else None

        ato_metrics = {
            'ato_open': ato_data['open'].iloc[0],
            'ato_high': ato_data['high'].max(),
            'ato_low': ato_data['low'].min(),
            'ato_close': ato_data['close'].iloc[-1],
            'ato_volume': ato_data['volume'].sum(),
            'ato_direction': 'bullish' if ato_data['close'].iloc[-1] > ato_data['open'].iloc[0] else 'bearish',
            'ato_range': ato_data['high'].max() - ato_data['low'].min(),
        }

        if prev_close:
            ato_metrics['gap'] = ato_data['open'].iloc[0] - prev_close
            ato_metrics['gap_direction'] = 'up' if ato_metrics['gap'] > 0 else 'down'

        return ato_metrics

    def get_close_analysis(self) -> Dict:
        """
        Analyze closing period (last 15 minutes) metrics.

        Returns:
            Close period metrics and signals
        """
        close_data = self.get_session_data('close')

        if close_data.empty:
            return {}

        afternoon_data = self.get_session_data('afternoon')
        afternoon_high = afternoon_data['high'].max() if not afternoon_data.empty else 0
        afternoon_low = afternoon_data['low'].min() if not afternoon_data.empty else 0

        close_metrics = {
            'close_price': close_data['close'].iloc[-1],
            'close_high': close_data['high'].max(),
            'close_low': close_data['low'].min(),
            'close_volume': close_data['volume'].sum(),
            'close_direction': 'bullish' if close_data['close'].iloc[-1] > close_data['open'].iloc[0] else 'bearish',
            'close_range': close_data['high'].max() - close_data['low'].min(),
            'volume_spike': close_data['volume'].mean() > afternoon_data['volume'].mean() * 1.5 if not afternoon_data.empty else False,
        }

        # Close position analysis
        close_price = close_data['close'].iloc[-1]
        if close_price > afternoon_high:
            close_metrics['close_position'] = 'above_high'
        elif close_price < afternoon_low:
            close_metrics['close_position'] = 'below_low'
        else:
            close_metrics['close_position'] = 'within_range'

        return close_metrics

    def get_session_momentum(self, session: str = 'morning') -> float:
        """
        Calculate session momentum (-1 to 1).

        Args:
            session: Session name

        Returns:
            Momentum value: 1 = strong bullish, -1 = strong bearish, 0 = neutral
        """
        session_data = self.get_session_data(session)

        if session_data.empty or len(session_data) < 2:
            return 0

        # Price momentum
        price_change = (session_data['close'].iloc[-1] - session_data['open'].iloc[0]) / session_data['open'].iloc[0]
        price_momentum = np.clip(price_change * 100, -1, 1)  # Convert to -1 to 1 range

        # Volume momentum (compare to average)
        avg_volume = session_data['volume'].mean()
        current_volume = session_data['volume'].iloc[-1]
        volume_ratio = (current_volume / avg_volume) if avg_volume > 0 else 1
        volume_momentum = np.clip((volume_ratio - 1) / 5, -1, 1)  # Normalize

        # Combined momentum
        momentum = (price_momentum * 0.7) + (volume_momentum * 0.3)

        return float(np.clip(momentum, -1, 1))

    def predict_next_session(self, current_session: str = 'morning') -> Dict:
        """
        Predict next session direction based on current session.

        Args:
            current_session: Current session name

        Returns:
            Prediction metrics
        """
        current_data = self.get_session_data(current_session)

        if current_data.empty:
            return {}

        momentum = self.get_session_momentum(current_session)

        prediction = {
            'current_session': current_session,
            'current_momentum': momentum,
            'predicted_direction': 'bullish' if momentum > 0.1 else ('bearish' if momentum < -0.1 else 'neutral'),
            'confidence': abs(momentum),
            'confidence_pct': f"{abs(momentum) * 100:.1f}%",
        }

        return prediction

    def get_daily_summary(self) -> Dict:
        """
        Get comprehensive daily trading summary.

        Returns:
            Dictionary with daily metrics and insights
        """
        all_sessions = self.get_all_sessions()
        comparison = self.compare_sessions()
        ato = self.get_ato_analysis()
        close = self.get_close_analysis()

        summary = {
            'sessions': all_sessions,
            'comparison': comparison,
            'ato': ato,
            'close': close,
            'daily_volume': self.data['volume'].sum(),
            'daily_high': self.data['high'].max(),
            'daily_low': self.data['low'].min(),
            'daily_open': self.data['open'].iloc[0] if len(self.data) > 0 else None,
            'daily_close': self.data['close'].iloc[-1] if len(self.data) > 0 else None,
        }

        return summary


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Example usage with sample data
    print("VN Session Analyzer - Ready for implementation")
    print("Awaiting real vnstock data integration...")

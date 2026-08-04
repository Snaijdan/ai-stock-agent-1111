"""
AI Stock Agent - TradingView-like Stock Analysis Platform
Main Streamlit application entry point
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import config

# Page configuration
st.set_page_config(
    page_title=config.STREAMLIT_PAGE_TITLE,
    page_icon=config.STREAMLIT_PAGE_ICON,
    layout=config.STREAMLIT_LAYOUT,
    initial_sidebar_state=config.STREAMLIT_INITIAL_SIDEBAR_STATE,
)

# Custom CSS
st.markdown("""
<style>
    [data-testid="stMetric"] {
        border: 1px solid #ddd;
        padding: 10px;
        border-radius: 5px;
    }
    .stPlotlyChart {
        border: 1px solid #eee;
        border-radius: 5px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables"""
    if "symbol" not in st.session_state:
        st.session_state.symbol = "VNI"
    if "period" not in st.session_state:
        st.session_state.period = "1y"
    if "timeframe" not in st.session_state:
        st.session_state.timeframe = "1d"
    if "watchlist" not in st.session_state:
        st.session_state.watchlist = config.DEFAULT_STOCKS
    if "show_indicators" not in st.session_state:
        st.session_state.show_indicators = {
            "SMA": True,
            "EMA": True,
            "RSI": True,
            "MACD": False,
            "Bollinger": False,
        }

def render_sidebar():
    """Render sidebar with controls"""
    with st.sidebar:
        st.header("⚙️ Configuration")

        # Stock selection
        st.subheader("Stock Selection")
        symbol = st.selectbox(
            "Select Stock Symbol",
            options=config.MAJOR_STOCKS + config.DEFAULT_STOCKS,
            index=0 if st.session_state.symbol not in config.MAJOR_STOCKS else config.MAJOR_STOCKS.index(st.session_state.symbol),
            key="symbol_select"
        )
        st.session_state.symbol = symbol

        # Time period selection
        st.subheader("Time Period")
        period = st.selectbox(
            "Select Period",
            options=config.AVAILABLE_PERIODS,
            index=config.AVAILABLE_PERIODS.index(st.session_state.period) if st.session_state.period in config.AVAILABLE_PERIODS else 3,
            key="period_select"
        )
        st.session_state.period = period

        # Timeframe selection
        st.subheader("Timeframe")
        timeframe = st.selectbox(
            "Select Timeframe",
            options=config.AVAILABLE_TIMEFRAMES,
            index=config.AVAILABLE_TIMEFRAMES.index(st.session_state.timeframe) if st.session_state.timeframe in config.AVAILABLE_TIMEFRAMES else 6,
            key="timeframe_select"
        )
        st.session_state.timeframe = timeframe

        # Technical Indicators
        st.subheader("Technical Indicators")
        for indicator in st.session_state.show_indicators.keys():
            st.session_state.show_indicators[indicator] = st.checkbox(
                indicator,
                value=st.session_state.show_indicators[indicator]
            )

        # Watchlist
        st.subheader("Watchlist")
        if st.button("➕ Add to Watchlist"):
            if symbol not in st.session_state.watchlist:
                st.session_state.watchlist.append(symbol)
                st.success(f"Added {symbol} to watchlist!")

        st.write("Current Watchlist:")
        for i, stock in enumerate(st.session_state.watchlist):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"• {stock}")
            with col2:
                if st.button("✕", key=f"remove_{i}"):
                    st.session_state.watchlist.remove(stock)
                    st.rerun()

def render_main_content():
    """Render main content area"""
    # Header
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.title(f"📊 {st.session_state.symbol} Analysis")

    # Status information
    st.info(
        f"📈 **Period**: {st.session_state.period} | "
        f"⏱️ **Timeframe**: {st.session_state.timeframe} | "
        f"🔄 **Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    # Placeholder for real data
    st.subheader("📊 Price Chart")
    st.warning(
        "⚠️ **Feature in Development**\n\n"
        "Real-time chart and technical analysis will be displayed here once data integration is complete.\n\n"
        "The application will:\n"
        "- Fetch OHLCV data from vnstock API\n"
        "- Calculate technical indicators (SMA, EMA, RSI, MACD, etc.)\n"
        "- Display interactive Plotly charts\n"
        "- Perform volume and cash flow analysis\n"
        "- Show pattern recognition results"
    )

    # Key Metrics
    st.subheader("📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Price", "N/A", "N/A", help="Current price")
    with col2:
        st.metric("Change %", "N/A", "N/A", help="Price change percentage")
    with col3:
        st.metric("Volume", "N/A", "N/A", help="Trading volume")
    with col4:
        st.metric("RSI(14)", "N/A", "N/A", help="Relative Strength Index")

    # Technical Analysis Section
    if any(st.session_state.show_indicators.values()):
        st.subheader("📊 Technical Analysis")
        with st.expander("Technical Indicators"):
            st.info("Technical indicator data will be calculated and displayed here")

            # Create placeholder columns for indicators
            cols = st.columns(2)
            for i, (indicator, enabled) in enumerate(st.session_state.show_indicators.items()):
                if enabled:
                    with cols[i % 2]:
                        st.text(f"{indicator} (Pending)")

    # Volume Analysis Section
    st.subheader("📊 Volume & Cash Flow Analysis")
    with st.expander("Volume Metrics"):
        st.info("Volume analysis, money flow indicators, and liquidity metrics will be shown here")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("MFI(14)", "N/A", help="Money Flow Index")
        with col2:
            st.metric("OBV", "N/A", help="On-Balance Volume")
        with col3:
            st.metric("CMF(20)", "N/A", help="Chaikin Money Flow")

    # Pattern Recognition Section
    st.subheader("🔍 Pattern Recognition")
    with st.expander("Detected Patterns"):
        st.info("Support/resistance levels, trend lines, and candlestick patterns will be identified here")

    # Analysis Summary
    st.subheader("📋 Analysis Summary")
    with st.expander("Full Analysis Report"):
        st.markdown("""
        ### Stock Analysis Report

        **Coming Soon:**
        - Comprehensive technical analysis
        - Trend assessment
        - Support/Resistance levels
        - Volume analysis interpretation
        - Trading signals
        - Risk assessment
        """)

def render_footer():
    """Render footer information"""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888; font-size: 0.8em;">
        <p>AI Stock Agent v1.0 | Powered by vnstock API | Last Updated: 2026-08-04</p>
        <p>Disclaimer: This tool is for analysis only. Always do your own research before trading.</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main application entry point"""
    # Initialize session state
    init_session_state()

    # Render sidebar
    render_sidebar()

    # Render main content
    render_main_content()

    # Render footer
    render_footer()

if __name__ == "__main__":
    main()

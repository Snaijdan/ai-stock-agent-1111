# AI Stock Agent - Build Guide for Cloud Agent

This guide outlines the development priorities and tasks for building out the AI Stock Agent application.

## 🎯 Development Priorities (VN Market Focused)

### Phase 1: VN-Specific Session & Volume Analysis (CRITICAL)
**Goal**: Implement VN market session analysis and money flow detection

#### Tasks:
1. **Implement VN Session Analyzer** (`src/vnmarket/session_analyzer.py`) ✅ READY
   - Morning (09:15-11:30) vs Afternoon (13:00-15:00) volume breakdown
   - ATO (9:15-9:30) analysis - volume, direction, predictive power
   - Close (14:45-15:00) analysis - volume spike, direction confirmation
   - Session momentum calculation
   - Session pattern recognition (morning trend → afternoon continuation/reversal)
   - Daily summary with all metrics

2. **Implement Liquidity Analyzer** (`src/vnmarket/liquidity_analyzer.py`) ✅ READY
   - Bid-ask spread estimation and tracking
   - Volume by price level (POC - Point of Control)
   - Liquidity score calculation (0-100)
   - Liquidity zones (thick vs thin)
   - Large order detection (whale orders >50k shares)
   - Order book imbalance detection
   - Slippage estimation for different order sizes
   - Best entry level recommendation

3. **Implement VN Alert System** (`src/vnmarket/vn_alerts.py`) ✅ READY
   - Breakout alerts (with volume confirmation)
   - Volume spike alerts (>200% average)
   - Strong close alerts (high volume + direction)
   - Momentum alerts (2%+ moves)
   - Spread widening alerts (liquidity warning)
   - Trend reversal alerts (MA crossovers)
   - Level test alerts (S/R approach)
   - Multi-level alert priority system

4. **Core Data Integration**
   - Fetch OHLCV data from vnstock API
   - Support 1-minute and 5-minute candles (for intraday analysis)
   - Daily candles (for swing trading)
   - Data caching mechanism
   - Error handling and retries

### Phase 2: VN-Specific Levels & Institutional Flow (High Priority)
**Goal**: Identify VN-specific price levels and detect institutional trading

#### Tasks:
1. **Implement VN Level Detection** (`src/vnmarket/vn_levels.py`)
   - Psychological levels (round numbers: 100, 200, 500, 1000 VND)
   - Decade levels (10,000, 20,000, 50,000 VND) - VN traders focus on these
   - 52-week highs/lows
   - Previous day OHLC levels
   - Trend lines (higher lows, lower highs)
   - Level clustering (confluence zones)
   - Level strength scoring (X touches = stronger level)

2. **Implement Institutional Flow Detection**
   - Large block order detection (>50k, >100k shares)
   - Foreign investor flow direction (if data available)
   - Accumulation vs Distribution patterns
   - Domestic fund buying/selling patterns
   - Retail panic indicators

3. **Implement Technical Indicators** (`src/indicators/technical.py` - Already templated)
   - Core indicators: SMA, EMA, RSI, MACD, Bollinger Bands
   - Volatility: ATR, ADX
   - Momentum: Stochastic, ROC, CCI
   - Focus on using these with VN liquidity patterns

### Phase 3: UI/Dashboard Enhancement (Medium Priority)
**Goal**: Create interactive, professional-grade dashboard

#### Tasks:
1. **Implement chart rendering**
   - OHLCV candlestick charts
   - Technical indicators overlays
   - Volume bars
   - Interactive Plotly charts
   - Multiple timeframe support

2. **Enhance Streamlit UI**
   - Real data integration in main.py
   - Dynamic metric updates
   - Interactive controls
   - Stock comparison
   - Watchlist functionality

3. **Add advanced features**
   - Alert system
   - Portfolio tracking
   - Analysis export (CSV, PDF)
   - Dark mode support

### Phase 4: Performance & Optimization (Medium Priority)
**Goal**: Ensure smooth, responsive application

#### Tasks:
1. **Optimize data loading**
   - Implement intelligent caching
   - Multi-threaded data fetching
   - Lazy loading for large datasets

2. **Performance monitoring**
   - Add logging system
   - Performance metrics
   - Error handling

3. **Database integration (optional)**
   - Setup SQLite for historical data
   - Implement data persistence
   - Query optimization

### Phase 5: Testing & Documentation (Low-Medium Priority)
**Goal**: Ensure code quality and maintainability

#### Tasks:
1. **Unit tests**
   - Test data fetching
   - Test indicator calculations
   - Test data validation

2. **Integration tests**
   - API integration tests
   - UI component tests
   - End-to-end workflow tests

3. **Documentation**
   - API documentation
   - Indicator formulas
   - Usage examples
   - Contributing guidelines

## 📋 Code Structure to Implement

```
src/
├── data/
│   ├── __init__.py
│   ├── vnstock_fetcher.py          # Main data fetching module
│   ├── data_models.py              # Data classes and structures
│   ├── data_validator.py           # Validation logic
│   └── cache_manager.py            # Caching implementation
├── indicators/
│   ├── __init__.py
│   ├── technical.py                # Technical indicators
│   ├── volume.py                   # Volume indicators
│   ├── patterns.py                 # Pattern recognition
│   └── calculator.py               # Shared calculation utilities
├── models/
│   ├── __init__.py
│   ├── ml_models.py                # ML-based predictions (optional)
│   └── backtester.py               # Backtesting engine (optional)
├── ui/
│   ├── __init__.py
│   ├── charts.py                   # Chart rendering with Plotly
│   ├── components.py               # Reusable UI components
│   └── styles.py                   # UI styling utilities
├── utils/
│   ├── __init__.py
│   ├── logger.py                   # Logging setup
│   ├── decorators.py               # Useful decorators (caching, timing)
│   ├── helpers.py                  # Utility functions
│   └── exceptions.py               # Custom exceptions
├── main.py                         # Streamlit app entry point
└── analyze.py                      # CLI analysis tool

tests/
├── __init__.py
├── test_data_fetching.py
├── test_indicators.py
├── test_ui_components.py
└── test_integration.py
```

## 🔧 Implementation Guidelines

### Code Quality
- Follow PEP 8 style guide
- Use type hints for all functions
- Write docstrings for all modules and functions
- Keep functions focused and maintainable
- Maximum function length: ~50 lines

### Performance
- Cache frequently accessed data
- Use vectorized operations (NumPy/Pandas)
- Avoid N+1 queries
- Profile code before optimizing
- Target: <1s response time for most operations

### Error Handling
- Graceful API failure handling
- User-friendly error messages
- Comprehensive logging
- Retry logic with exponential backoff

### Testing
- Aim for >80% code coverage
- Test edge cases and error conditions
- Mock external API calls in tests
- Use fixtures for test data

## 📦 Dependencies Already Installed

From requirements.txt:
- **vnstock** - Vietnamese stock API
- **pandas** - Data manipulation
- **numpy** - Numerical computation
- **streamlit** - UI framework
- **plotly** - Interactive charts
- **ta** - Technical analysis library (can use as reference)
- **scipy** - Scientific computation
- **scikit-learn** - ML algorithms

## ⚡ Quick Start Development

1. Start with `src/data/vnstock_fetcher.py`
   - Create `fetch_ohlcv()` function
   - Test with a single stock (e.g., 'VNI')

2. Move to `src/indicators/technical.py`
   - Implement SMA, EMA, RSI first
   - Test with sample data

3. Integrate into `src/main.py`
   - Replace placeholder metrics with real data
   - Add chart rendering

4. Add volume indicators
   - Implement MFI, CMF, OBV
   - Add volume chart

5. Enhance UI/UX
   - Improve layout and styling
   - Add interactive features
   - Performance optimization

## 🎨 UI/UX Considerations

- Keep interface clean and professional
- Follow TradingView-like design patterns
- Responsive design for different screen sizes
- Dark mode support
- Real-time updates where possible
- Clear visual hierarchy

## 🚀 Performance Targets

- Page load: <2 seconds
- Chart rendering: <1 second
- Indicator calculation: <500ms
- API call: <5 seconds
- Cache hit rate: >80%

## 📊 Feature Checklist

- [ ] OHLCV data fetching
- [ ] Data caching
- [ ] SMA indicator
- [ ] EMA indicator
- [ ] RSI indicator
- [ ] MACD indicator
- [ ] Bollinger Bands
- [ ] Volume indicators (MFI, CMF, OBV)
- [ ] Candlestick charts
- [ ] Multiple timeframe support
- [ ] Technical indicator overlays
- [ ] Pattern recognition (basic)
- [ ] Watchlist functionality
- [ ] Real-time metrics display
- [ ] Error handling and logging
- [ ] Performance optimization
- [ ] Unit tests
- [ ] Documentation

## 🔗 Reference Resources

- TradingView: https://www.tradingview.com
- vnstock Documentation: Check GitHub repo
- Technical Analysis: https://school.stockcharts.com
- Streamlit: https://docs.streamlit.io
- Plotly: https://plotly.com/python/

## 💡 Tips for Success

1. **Start small**: Get basic data fetching working first
2. **Test frequently**: Run tests after each feature
3. **Use version control**: Commit frequently with clear messages
4. **Document as you go**: Write docstrings and comments
5. **Performance matters**: Profile and optimize regularly
6. **User experience**: Test UI changes with actual data
7. **Handle edge cases**: Test with multiple stocks and timeframes

---

**Last Updated**: 2026-08-04
**Status**: Ready for development
**Priority**: Complete Phase 1 & 2 first, then Phase 3-5

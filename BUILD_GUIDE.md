# AI Stock Agent - Build Guide for Cloud Agent

This guide outlines the development priorities and tasks for building out the AI Stock Agent application.

## 🎯 Development Priorities

### Phase 1: Core Data & API Integration (High Priority)
**Goal**: Establish reliable data pipeline from vnstock API

#### Tasks:
1. **Implement vnstock_fetcher.py**
   - Fetch OHLCV data for Vietnamese stocks
   - Support multiple timeframes (1m, 5m, 15m, 30m, 1h, 1d, 1w, 1M)
   - Implement data caching mechanism
   - Handle API errors and retries
   - Rate limiting compliance

2. **Create data models/dataclasses**
   - Define OHLCV data structure
   - Stock metadata
   - Candlestick data
   - Volume data

3. **Implement data validation**
   - Verify data integrity
   - Check for gaps in time series
   - Validate OHLCV relationships (H >= O, L <= O, etc.)

### Phase 2: Technical Analysis Indicators (High Priority)
**Goal**: Calculate all required technical indicators

#### Tasks:
1. **Implement core indicators (src/indicators/technical.py)**
   - Simple Moving Average (SMA)
   - Exponential Moving Average (EMA)
   - Relative Strength Index (RSI)
   - MACD (Moving Average Convergence Divergence)
   - Bollinger Bands
   - Average True Range (ATR)
   - Average Directional Index (ADX)
   - Stochastic Oscillator

2. **Implement volume indicators (src/indicators/volume.py)**
   - Money Flow Index (MFI)
   - Chaikin Money Flow (CMF)
   - On-Balance Volume (OBV)
   - Accumulation/Distribution Line (A/D)
   - Volume Rate of Change (VROC)

3. **Implement pattern recognition**
   - Support/Resistance detection
   - Trend identification
   - Candlestick patterns
   - Moving average crossovers

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

# AI Stock Agent - TradingView-like Analysis Platform

A comprehensive AI-powered stock analysis application for Vietnamese stocks, combining technical analysis, cash flow analysis, and machine learning insights using real-time data from vnstock API.

## Features

### Technical Analysis
- Technical indicators (SMA, EMA, RSI, MACD, Bollinger Bands, ATR, etc.)
- Pattern recognition (support/resistance levels, trend lines, candlestick patterns)
- Multiple timeframe analysis (1m, 5m, 15m, 1h, 1d, 1w, 1m)
- Trend detection and momentum analysis

### Cash Flow & Volume Analysis
- Volume profile and analysis
- Money flow indicators (MFI, CMF, OBV)
- Institutional buying/selling patterns
- Liquidity depth analysis
- Volume trend analysis

### Data & Performance
- Real-time data from vnstock API
- Efficient data caching and storage
- Support for VNI, VN30, HNX, and individual stocks
- Optimized data pipeline for fast retrieval
- Multi-threaded data fetching

### User Interface
- Interactive Streamlit dashboard
- Real-time charts with Plotly
- Stock watchlist management
- Alert configuration
- Portfolio tracking
- Analysis export (CSV, PDF)

## Tech Stack

- **Backend**: Python 3.8+
- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy, SciPy
- **Technical Analysis**: TA-Lib, Custom indicators
- **Charting**: Plotly
- **Data Source**: vnstock API
- **Storage**: SQLite/PostgreSQL (optional)
- **ML**: scikit-learn, XGBoost (optional)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Snaijdan/ai-stock-agent-1111.git
cd ai-stock-agent-1111
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment (optional):
```bash
cp .env.example .env
# Edit .env with your settings
```

## Usage

### Run the Application

```bash
streamlit run src/main.py
```

The application will be available at `http://localhost:8501`

### Command Line Analysis

```bash
python src/analyze.py --symbol VNI --period 30d
```

### Configuration

Edit `config.py` for:
- API endpoints
- Default time periods
- Chart configurations
- Technical indicator parameters
- Cache settings

## Project Structure

```
ai-stock-agent-1111/
├── src/
│   ├── main.py                 # Streamlit application entry point
│   ├── analyze.py              # CLI analysis tool
│   ├── indicators/             # Technical indicator implementations
│   ├── data/                   # Data fetching and processing
│   ├── models/                 # ML models (optional)
│   └── utils/                  # Utility functions
├── tests/                      # Unit tests
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
├── .env.example                # Environment variables template
└── README.md                   # This file
```

## Development

### Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

### Test your changes:
```bash
python -m pytest tests/
```

### Commit and push:
```bash
git add .
git commit -m "feat: add your feature description"
git push origin feature/your-feature-name
```

## API Usage

### Fetch Stock Data
```python
from src.data.vnstock_fetcher import VnstockFetcher

fetcher = VnstockFetcher()
data = fetcher.get_ohlcv('VNI', start_date='2024-01-01', end_date='2024-08-04')
```

### Calculate Indicators
```python
from src.indicators.technical import TechnicalAnalyzer

analyzer = TechnicalAnalyzer(data)
sma = analyzer.calculate_sma(period=20)
rsi = analyzer.calculate_rsi(period=14)
```

## Performance Tips

- Use caching for frequently accessed stocks
- Batch requests when fetching multiple stocks
- Adjust technical indicator periods based on timeframe
- Monitor API rate limits

## Contributing

1. Fork the repository
2. Create feature branch
3. Make your changes
4. Add tests for new features
5. Submit pull request

## License

MIT License - see LICENSE file for details

## Support

For issues, feature requests, or questions:
- Open an issue on GitHub
- Check existing documentation
- Review technical analysis guidelines

## Roadmap

### v1.0 (Current)
- Core technical analysis
- Basic UI with Streamlit
- vnstock integration

### v1.1 (Planned)
- ML-based pattern recognition
- Portfolio backtesting
- Advanced alert system
- Mobile app support

### v2.0 (Future)
- Real-time trading signals
- Machine learning predictions
- Multi-market support
- API for external integration

## Changelog

See CHANGELOG.md for detailed version history

---

**Last Updated**: 2026-08-04
**Version**: 1.0.0-alpha
**Status**: In Active Development

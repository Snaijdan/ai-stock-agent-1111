#!/bin/bash
# Setup script for cloud agent - RUN THIS FIRST

echo "Step 1: Installing dependencies..."
pip install -r requirements.txt -q

echo "Step 2: Checking Python syntax..."
python -m py_compile src/main.py
python -m py_compile src/data/vnstock_fetcher.py
python -m py_compile src/indicators/technical.py
python -m py_compile src/vnmarket/session_analyzer.py
python -m py_compile src/vnmarket/liquidity_analyzer.py
python -m py_compile src/vnmarket/vn_alerts.py

echo "Step 3: Testing imports..."
python -c "import sys; sys.path.insert(0, '.'); import streamlit; print('✓ streamlit')"
python -c "import sys; sys.path.insert(0, '.'); from src.data.vnstock_fetcher import VnstockFetcher; print('✓ vnstock_fetcher')"
python -c "import sys; sys.path.insert(0, '.'); from src.indicators.technical import TechnicalAnalyzer; print('✓ technical')"
python -c "import sys; sys.path.insert(0, '.'); from src.vnmarket.session_analyzer import VNSessionAnalyzer; print('✓ session_analyzer')"
python -c "import sys; sys.path.insert(0, '.'); from src.vnmarket.liquidity_analyzer import VNLiquidityAnalyzer; print('✓ liquidity_analyzer')"
python -c "import sys; sys.path.insert(0, '.'); from src.vnmarket.vn_alerts import VNAlertGenerator; print('✓ vn_alerts')"

echo "✅ All setup checks passed! Ready to build."

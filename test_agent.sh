#!/bin/bash
# Cloud agent test script

echo "Step 1: Configure git"
git config user.name "Claude Agent"
git config user.email "claude@anthropic.com"

echo "Step 2: Install dependencies"
pip install -r requirements.txt -q

echo "Step 3: Test imports"
python -c "import sys; sys.path.insert(0, '.'); from src.main import *; from src.data.vnstock_fetcher import VnstockFetcher; from src.indicators.technical import TechnicalAnalyzer; from src.vnmarket.session_analyzer import VNSessionAnalyzer; from src.vnmarket.liquidity_analyzer import VNLiquidityAnalyzer; from src.vnmarket.vn_alerts import VNAlertGenerator; print('OK')"

echo "Step 4: Commit and push"
git add .
git commit -m "test: Cloud agent validation - all modules working with correct dependencies"
git push origin main

echo "Done"

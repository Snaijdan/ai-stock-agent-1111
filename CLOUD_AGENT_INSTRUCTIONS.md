# Cloud Agent - Step-by-Step Instructions

**IMPORTANT**: Follow these steps EXACTLY in order. Do NOT skip Setup.

---

## ⚠️ SETUP (DO THIS FIRST - NO EXCEPTIONS)

```bash
# Step 1: Install all dependencies
pip install -r requirements.txt

# Step 2: Verify all files compile
python -m py_compile src/main.py src/data/vnstock_fetcher.py src/indicators/technical.py src/vnmarket/session_analyzer.py src/vnmarket/liquidity_analyzer.py src/vnmarket/vn_alerts.py

# Step 3: Test imports work
python -c "import sys; sys.path.insert(0, '.'); from src.main import *; print('✅ All imports OK')"
```

**If ANY of these fail, STOP immediately and report the error. Do NOT continue.**

---

## 📋 Phase 1: Validation & Testing

### 1.1 Test vnstock API
Write and run this test script:
```python
# test_vnstock.py
import sys
sys.path.insert(0, '.')
from src.data.vnstock_fetcher import VnstockFetcher

print("Testing vnstock integration...")
fetcher = VnstockFetcher()

# Try to fetch real data
data = fetcher.fetch_ohlcv('VNI', start_date='2024-01-01', end_date='2024-01-10')

if data is None or data.empty:
    print("⚠️ vnstock API not returning data - placeholder mode detected")
    print("This is expected if vnstock is not fully integrated yet")
else:
    print(f"✅ vnstock working! Fetched {len(data)} candles")
    print(data.head())
```

**Action**: Run this and check output. Document result before proceeding.

### 1.2 Test Technical Indicators
```python
# test_indicators.py
import sys, pandas as pd, numpy as np
sys.path.insert(0, '.')
from src.indicators.technical import TechnicalAnalyzer

# Create sample data
dates = pd.date_range('2024-01-01', periods=100)
data = pd.DataFrame({
    'open': np.random.randn(100).cumsum() + 100,
    'high': np.random.randn(100).cumsum() + 102,
    'low': np.random.randn(100).cumsum() + 98,
    'close': np.random.randn(100).cumsum() + 100,
    'volume': np.random.randint(1000, 10000, 100),
}, index=dates)

# Test indicator calculations
analyzer = TechnicalAnalyzer(data)
sma = analyzer.calculate_sma(20)
rsi = analyzer.calculate_rsi(14)
macd, signal, hist = analyzer.calculate_macd()

print(f"✅ SMA calculated: {sma.iloc[-1]:.2f}")
print(f"✅ RSI calculated: {rsi.iloc[-1]:.2f}")
print(f"✅ MACD calculated: {macd.iloc[-1]:.2f}")

# Check for NaN errors
if sma.isna().all():
    print("❌ ERROR: SMA all NaN")
elif rsi.isna().all():
    print("❌ ERROR: RSI all NaN")
else:
    print("✅ All indicators working")
```

**Action**: Run and fix any NaN/calculation errors found.

### 1.3 Test VN Session Analyzer
```python
# test_session.py
import sys, pandas as pd, numpy as np
sys.path.insert(0, '.')
from src.vnmarket.session_analyzer import VNSessionAnalyzer

# Create sample intraday data (with time index)
times = pd.date_range('2024-01-01 09:15', periods=100, freq='1min')
data = pd.DataFrame({
    'open': np.random.randn(100).cumsum() + 100,
    'high': np.random.randn(100).cumsum() + 102,
    'low': np.random.randn(100).cumsum() + 98,
    'close': np.random.randn(100).cumsum() + 100,
    'volume': np.random.randint(100, 1000, 100),
}, index=times)

analyzer = VNSessionAnalyzer(data)
summary = analyzer.get_daily_summary()

print(f"✅ Session analysis working")
print(f"Daily volume: {summary.get('daily_volume', 'N/A')}")
```

**Action**: Run and fix any errors.

### 1.4 Test Liquidity Analyzer
```python
# test_liquidity.py
import sys, pandas as pd, numpy as np
sys.path.insert(0, '.')
from src.vnmarket.liquidity_analyzer import VNLiquidityAnalyzer

# Sample data
dates = pd.date_range('2024-01-01', periods=100)
data = pd.DataFrame({
    'open': np.random.randn(100).cumsum() + 100,
    'high': np.random.randn(100).cumsum() + 102,
    'low': np.random.randn(100).cumsum() + 98,
    'close': np.random.randn(100).cumsum() + 100,
    'volume': np.random.randint(1000, 10000, 100),
}, index=dates)

analyzer = VNLiquidityAnalyzer(data)
summary = analyzer.get_liquidity_summary()

print(f"✅ Liquidity analysis working")
print(f"Liquidity score: {summary.get('liquidity_score', 'N/A')}")
```

**Action**: Run and verify working.

### 1.5 Test Alert System
```python
# test_alerts.py
import sys, pandas as pd, numpy as np
sys.path.insert(0, '.')
from src.vnmarket.vn_alerts import VNAlertGenerator

# Sample data
dates = pd.date_range('2024-01-01', periods=100)
data = pd.DataFrame({
    'open': np.random.randn(100).cumsum() + 100,
    'high': np.random.randn(100).cumsum() + 102,
    'low': np.random.randn(100).cumsum() + 98,
    'close': np.random.randn(100).cumsum() + 100,
    'volume': np.random.randint(1000, 10000, 100),
}, index=dates)

generator = VNAlertGenerator('VNI', data)
alerts = generator.generate_all_alerts(resistance=105, support=95)

print(f"✅ Alert system working")
print(f"Generated {len(alerts)} alerts")
for alert in alerts:
    print(f"  - {alert.alert_type}: {alert.message}")
```

**Action**: Run and verify working.

---

## 🔧 Phase 2: Fix Any Bugs Found

If any tests above failed:
1. Identify the error
2. Fix the code in the relevant module
3. Re-test
4. Commit: `fix: Handle {issue} in {module}`

Common issues to check:
- NaN values in calculations
- Division by zero (especially RSI, MFI, CCI)
- Empty DataFrames
- Incorrect indexing

---

## 📝 Phase 3: Documentation & Commit

After all tests pass:
```bash
git add .
git commit -m "test: Validate all modules work with real data

- Tested vnstock_fetcher integration
- Tested technical indicators (SMA, EMA, RSI, MACD, etc.)
- Tested VN session analyzer (morning/afternoon/ATO/close)
- Tested liquidity analyzer (spread, POC, score)
- Tested alert generation system
- Fixed any NaN/calculation errors
- All modules now tested and working"

git push origin main
```

---

## ⚡ Quality Checklist Before Committing

- [ ] All imports work without errors
- [ ] vnstock API tested (or documented as not implemented)
- [ ] All indicator calculations produce non-NaN results
- [ ] No division by zero errors
- [ ] Session analyzer works with time-based data
- [ ] Liquidity calculations work
- [ ] Alert system generates alerts correctly
- [ ] Code compiles without syntax errors
- [ ] No circular imports
- [ ] Commit message is accurate

---

## ✅ Success = Tests Pass + Code Committed

When this is done, you've completed Phase 1 validation. The foundation is solid for Phase 2 (UI integration).

**Remember**: Correctness > Features. A few working, tested modules are better than many broken ones.

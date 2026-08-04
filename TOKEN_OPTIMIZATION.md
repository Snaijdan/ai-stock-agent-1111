# Token Optimization Guide for Cloud Agent

**Goal**: Maximize useful output while minimizing token waste. Every token spent must produce real value.

## 🎯 Core Principle
**Quality > Quantity | Efficiency > Verbosity | Real Features > Placeholder Code**

---

## ❌ AVOID (Token Waste)

### 1. Redundant Code
```python
# BAD - redundant parameter checking
def get_data(symbol):
    if not symbol:
        raise ValueError("symbol required")
    if symbol == "":
        raise ValueError("symbol cannot be empty")
    # ... rest of code
```

### 2. Over-Commenting
```python
# BAD - verbose comments waste tokens
# Get the close price from the data
close_price = data['close']
# Convert to float
close_price = float(close_price)
# Return the value
return close_price
```

### 3. Placeholder/Mock Code That Won't Be Used
```python
# BAD - fake implementation
def fetch_data(symbol):
    # TODO: implement vnstock API
    return pd.DataFrame([{'close': 100}])  # Fake data!
```

### 4. Testing Everything
- Don't test basic Python functionality (list.append, dict.keys)
- Don't test pandas/numpy operations that are standard library
- Focus testing on YOUR custom logic only

### 5. Multiple Implementations of Same Thing
```python
# BAD - why have both?
def calculate_sma(data, period=20):
    return data.rolling(period).mean()

def calc_sma(data, p=20):  # Same thing, different name
    return data.rolling(p).mean()
```

### 6. Verbose Logging
```python
# BAD - logs everywhere
logger.info(f"Starting function")
logger.info(f"Got parameter: {x}")
logger.info(f"About to calculate")
logger.info(f"Calculation done")
logger.info(f"Returning result")
```

---

## ✅ DO (Token Efficiency)

### 1. Clean, Functional Code
```python
# GOOD - straight to the point
def get_sma(data: pd.Series, period: int = 20) -> pd.Series:
    """Simple Moving Average"""
    return data.rolling(window=period).mean()
```

### 2. Test Only What You Changed
```python
# GOOD - test the actual custom logic
def calculate_rsi(data, period=14):
    # Test this specific implementation
    delta = data.diff()
    # ... rest of code

# Run once with sample data:
# test_data = pd.Series([100, 102, 101, 103, 105])
# result = calculate_rsi(test_data)
# assert not result.isna().all()
```

### 3. Reuse Existing Code
```python
# GOOD - use existing indicator instead of reimplementing
from src.indicators.technical import TechnicalAnalyzer

analyzer = TechnicalAnalyzer(data)
rsi = analyzer.calculate_rsi()  # Don't rewrite RSI logic
```

### 4. Strategic Logging
```python
# GOOD - log only critical points
logger.info(f"Fetched {len(data)} candles for {symbol}")
logger.warning(f"API rate limit approaching: {calls_remaining}")
```

### 5. Focus Implementation
```python
# GOOD - implement ONE thing well, not multiple half-baked things
# Phase: Implement real vnstock data fetching
# (Don't also implement ML predictions, backtesting, etc.)
```

---

## 📋 Implementation Checklist (Use This, Not Extra Testing)

### Before Writing Code
- [ ] Read existing code that does similar thing
- [ ] Check if code already exists (don't duplicate)
- [ ] Plan the implementation (write down steps before coding)

### While Writing
- [ ] Remove unnecessary imports
- [ ] Remove unused variables
- [ ] Keep functions <30 lines if possible
- [ ] One responsibility per function

### Before Committing
- [ ] Run syntax check: `python -m py_compile file.py`
- [ ] Test imports: `python -c "from module import X"`
- [ ] Run basic functionality once with real data
- [ ] Check for debugging print statements or commented code
- [ ] Verify commit message is accurate

---

## 🚀 Token Budget Allocation Strategy

**Total Budget: ~150k-200k tokens per session**

### Recommended Allocation:
| Phase | Budget | Focus |
|-------|--------|-------|
| Phase 1: Data Layer | 30-40k | Real vnstock API, test with 1-2 stocks |
| Phase 2: Indicators | 20-30k | Wire up existing modules, test calculations |
| Phase 3: UI/Charts | 40-50k | Streamlit integration, Plotly charts |
| Phase 4: Alerts | 20-30k | Implement alert system |
| Phase 5: Refinement | 20-30k | Bug fixes, optimizations, docs |

**Do NOT spend tokens on**:
- Verbose documentation (README is already detailed)
- Multiple implementations of same feature
- Testing standard library functionality
- Decorative comments
- "Nice to have" features (focus on core)

---

## 🎯 Priority Decision Matrix

**Spend tokens on** ✅ | **Skip or defer** ❌
---|---
Real vnstock API working | Fancy UI animations
Edge case handling | Multiple implementations
Performance optimization | Extensive logging
Type hints on public APIs | Every single comment
Error handling for API failures | "Might be useful" features
Integration between modules | Optional parameters

---

## ⚡ Quick Wins (High Value, Low Token Cost)

1. **Test actual import chain** (5 min, 100 tokens)
   - `python -c "import sys; sys.path.insert(0,'.'); from src.indicators.technical import TechnicalAnalyzer"`
   - Catches 90% of bugs

2. **Fetch one real data point** (10 min, 200 tokens)
   - `fetcher.fetch_ohlcv('VNM', start='2024-01-01', end='2024-08-04')`
   - Confirms vnstock API works

3. **Test one indicator calculation** (5 min, 200 tokens)
   - Calculate RSI on real data, print output
   - Verify formula is correct

4. **Verify Streamlit app imports** (5 min, 100 tokens)
   - `streamlit run src/main.py --logger.level=error 2>&1 | head -20`
   - Catch import/runtime errors early

---

## ⛔ Common Token Wastage Patterns

### Pattern 1: Scope Creep
❌ "While I'm here, let me also add ML predictions..."
✅ "Focus on Phase 1: data layer only"

### Pattern 2: Over-Engineering
❌ "Build a generic framework that could handle any indicator..."
✅ "Implement these 5 specific indicators correctly"

### Pattern 3: Fixing Non-Issues
❌ "Refactor all code to use factory patterns..."
✅ "Make sure the data and UI work correctly first"

### Pattern 4: Duplicate Testing
❌ "Test SMA, test EMA, test RSI, test all 20 combinations..."
✅ "Test 3 key indicators + edge cases (NaN, empty, zero)"

---

## 📊 Success Metrics

**Good session**:
- ✅ Core feature implemented and tested to work
- ✅ Code committed in non-broken state
- ✅ Real data flows through system
- ✅ Minimal redundancy

**Bad session**:
- ❌ Lots of code but nothing actually works
- ❌ Multiple broken commits
- ❌ Placeholder code left in place
- ❌ Redundant implementations

---

## Token Tips

1. **Use tools efficiently**
   - Bash: Run quick tests, not verbose output
   - Read: Get what you need, don't read entire files needlessly
   - Write: Commit working code, don't iterate dozens of times
   - Grep: Search before writing new code

2. **Batch operations**
   - Don't: Write file → Commit → Write another file → Commit
   - Do: Write file → Write another file → Commit once

3. **Strategic reviewing**
   - Don't: Read every line of every existing file
   - Do: Search for relevant code, read just that part

4. **Short feedback loops**
   - Test early, fail fast
   - If something doesn't work after 5 min, investigate immediately
   - Don't code for 30 min then test

---

**Remember**: 1 working feature beats 10 half-implemented features.
**Token efficiency = Ruthless prioritization + Laser focus + Fast verification.**

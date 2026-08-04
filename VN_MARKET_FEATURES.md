# Vietnamese Stock Market - Specialized Features Guide

## 🇻🇳 VN Market Characteristics

### Market Structure
- **Trading Sessions**: Morning (09:15-11:30) + Afternoon (13:00-15:00)
- **Trading Days**: Monday-Friday (T2-T6)
- **Main Indices**: VNI, VN30, HNX, UPCOM
- **Trading Units**: Shares (minimum varies)
- **Price Decimals**: 0, 50, or 100 VND depending on price range

### Market Participants
- **Retail Traders**: Majority volume, reactive trading
- **Domestic Funds**: Consistent buying/selling patterns
- **Foreign Investors**: Large blocks, morning/end-of-day focus
- **Market Makers**: Limited (mainly for VN30)

### Volume Characteristics
- **Morning Session**: Typically 40-60% of daily volume
- **ATO (09:15-09:30)**: Critical volume build-up
- **Lunch Break**: Complete halt (11:30-13:00)
- **Afternoon Session**: 40-60% volume, momentum continuation
- **Close (14:45-15:00)**: Very active (5-10% of daily volume)

---

## 🔴 PRIORITY 1: Intraday Volume & Money Flow Analysis

### Module: `src/vnmarket/session_analyzer.py`

**Purpose**: Analyze volume patterns within VN trading sessions

**Key Metrics**:
```python
- Morning volume (09:15-11:30) %
- Afternoon volume (13:00-15:00) %
- ATO volume & direction
- Close volume & direction
- Session high/low/close
- Session momentum (bullish/bearish)
- Volume distribution by time
```

**Features to Implement**:
1. **Session Breakdown**
   - Morning vs Afternoon volume comparison
   - Session open price vs previous close
   - Session high/low/close levels
   - Session range analysis

2. **ATO Analysis** (09:15-09:30)
   - ATO volume vs average
   - ATO direction (bullish/bearish)
   - ATO volatility
   - Predictive power for day's trend

3. **Close Analysis** (14:45-15:00)
   - Close volume surge detection
   - Close direction (up/down close)
   - Close above/below S/R levels
   - Close momentum intensity

4. **Session Correlation**
   - Does morning trend continue to afternoon?
   - Session reversal detection
   - Predictive patterns

**Practical Use Cases**:
- Morning bullish ATO → expect bullish afternoon
- Large afternoon volume → confirm intraday trend
- Close on high volume → strong signal for next day
- Session momentum change → potential reversal

---

## 🔴 PRIORITY 2: Liquidity & Spread Analysis

### Module: `src/vnmarket/liquidity_analyzer.py`

**Purpose**: Analyze bid-ask spread and order book depth

**Key Metrics**:
```python
- Bid-ask spread (in VND and %)
- Spread width vs average
- Bid-ask imbalance
- Order book depth (volume at each price level)
- Liquidity zones
- Best entry/exit levels
- Slippage estimation
```

**Features to Implement**:
1. **Spread Analysis**
   - Current spread vs historical average
   - Spread by price range (low price = wider spread)
   - Spread widening alerts (illiquidity warning)
   - Spread trending (increasing/decreasing)

2. **Volume by Price**
   - Volume concentrated at which levels
   - Resistance from thick volume
   - Support from thick volume
   - Volume profile POC (Point of Control)

3. **Liquidity Quality**
   - Liquidity score (0-100)
   - Safe entry/exit zones
   - Risky entry points (wide spread)
   - Slippage cost estimation

4. **Order Book Analysis**
   - Bid-ask imbalance ratio
   - Large order detection (whale orders)
   - Order book thickness at key levels
   - Order absorption capacity

**Practical Use Cases**:
- Wide spread → avoid entry (wait for better liquidity)
- Thick volume at level → strong S/R
- Imbalanced order book → directional bias
- Thin liquidity → risk management needed

---

## 🟠 PRIORITY 3: VN-Specific Level Analysis

### Module: `src/vnmarket/vn_levels.py`

**Purpose**: Identify psychological and technical levels specific to VN market

**Key Metrics**:
```python
- Round numbers (100, 200, 500, 1000 VND)
- Psychological levels (10,000, 20,000, 50,000 VND)
- 52-week highs/lows
- Previous day high/low
- Support/Resistance from historical levels
- Volume profile nodes
- Trend lines (higher lows/lower highs)
```

**Features to Implement**:
1. **Psychological Levels**
   - x.00 levels (major round numbers)
   - x.50 levels (half numbers)
   - Decade levels (10,000, 20,000, etc.)
   - Level strength (touched X times)

2. **Historical S/R**
   - 52-week high/low
   - Monthly/weekly highs/lows
   - Daily pivot points
   - Previous session OHLC levels

3. **Trend Lines**
   - Higher lows (uptrend)
   - Lower highs (downtrend)
   - Trend line breaks (reversal signal)
   - Distance to trend line

4. **Level Clustering**
   - Multiple levels converging
   - Zone support/resistance (not single line)
   - Confluence zones (strongest levels)

**Practical Use Cases**:
- VN traders buy at round numbers (9,500 instead of 9,475)
- Decade levels act as resistance (10,000, 20,000)
- Previous day high = common entry target
- Trend line break = trend reversal signal

---

## 🟠 PRIORITY 4: Trading Session Pattern Analysis

### Module: `src/vnmarket/session_patterns.py`

**Purpose**: Detect and analyze VN-specific session trading patterns

**Key Metrics**:
```python
- Morning strength vs afternoon continuation
- Session reversal patterns
- Close vs session high/low
- Session volatility
- Average move by session
- Session momentum acceleration
- Opening gap patterns
```

**Features to Implement**:
1. **Session Pattern Recognition**
   - Morning uptrend + afternoon uptrend = CONTINUE
   - Morning uptrend + afternoon downtrend = REVERSAL
   - Morning sideways + afternoon trend = BREAKOUT
   - Historical pattern frequency

2. **Opening Patterns**
   - Gap up from previous close (bullish)
   - Gap down from previous close (bearish)
   - ATO direction vs previous close
   - Morning first hour direction

3. **Close Patterns**
   - Close on high volume = strong
   - Close above resistance = breakout confirmation
   - Close below support = breakdown confirmation
   - Last hour momentum = next day predictor

4. **Session Statistics**
   - Average morning move
   - Average afternoon move
   - Morning + afternoon correlation
   - Win rate of patterns

**Practical Use Cases**:
- Morning trend strong → expect afternoon continuation
- Close on high volume + above resistance → strong buy signal
- Morning weak but afternoon strong → potential trend change
- Historical pattern repeat → high probability setup

---

## 🟡 PRIORITY 5: Smart Alert System for VN Traders

### Module: `src/vnmarket/vn_alerts.py`

**Purpose**: Generate actionable alerts for VN stock traders

**Alert Types**:

### A. Breakout Alerts
```
Condition: Price breaks above resistance + Volume > 120% average
Action: BUY SIGNAL
Example: VNI breaks 1300 with high volume → potential continuation
```

### B. Volume Spike Alerts
```
Condition: Volume > 200% of 20-day average
Action: ATTENTION - Something happening
Example: ACB suddenly 5x average volume → institutional activity
```

### C. Session Alerts
```
Morning Momentum: Strong morning ATO + uptrend → expect afternoon continuation
Afternoon Reversal: Morning downtrend reversed to uptrend in afternoon → trend change signal
Close Alert: Close on high volume + breakout → strong confirmation
```

### D. Liquidity Alerts
```
Spread Widening: Bid-ask spread > 200% average → AVOID entry (wait)
Thin Liquidity: Not enough buying/selling at price level → slippage risk
Large Order: >50k shares order detected → whale activity
```

### E. Money Flow Alerts
```
Buying Pressure: More large buys than sells → accumulation phase
Selling Pressure: More large sells than buys → distribution phase
Flow Reversal: Switch from buying to selling → potential top
```

### F. Level Alerts
```
Support Test: Price approaching key support level → potential reversal
Resistance Test: Price approaching key resistance level → potential pullback
Level Break: Price breaks above/below key level + volume → trend change
```

**Alert Delivery**:
- Real-time Streamlit notifications
- Email alerts (priority alerts)
- Telegram/Discord (optional)
- Alert history/log for review

---

## 📊 Implementation Priority Timeline

### Phase 1: Critical (Days 1-3)
✅ Session analysis (morning/afternoon breakdown)
✅ Volume and money flow detection
✅ Basic level identification (previous high/low, round numbers)

### Phase 2: High Priority (Days 3-5)
✅ Liquidity analysis (spread, bid-ask)
✅ VN-specific level system (psychological levels)
✅ Alert system (basic alerts)

### Phase 3: Enhanced (Days 5-7)
✅ Session pattern recognition
✅ Institutional flow detection
✅ Advanced alert system (conditional alerts)

---

## 🎯 Expected Outcomes

### For Day Traders
- Better entry/exit points (liquidity analysis)
- Session momentum confirmation
- Breakout + volume confirmation alerts
- Risk management (spread analysis)

### For Swing Traders
- Key level identification (S/R zones)
- Trend change detection (session patterns)
- Money flow direction (accumulation/distribution)
- Confluence zones (multiple confirmations)

### For Fundamental Investors
- Market structure analysis (volume by session)
- Institutional activity tracking
- Market sentiment gauge (money flow)
- Liquidity for position building

---

## 🔧 Technical Implementation Notes

### Data Requirements
- Real-time OHLCV data (at least 1-minute candles)
- Bid-ask data (if available from vnstock)
- Historical data (52-week minimum)
- Session time boundaries (09:15-11:30, 13:00-15:00)

### Performance Considerations
- Cache historical levels (recalculate daily at 21:00)
- Real-time alerts need sub-second latency
- Volume calculation by session (aggregate trades)
- Bid-ask spread calculation (bid-ask data availability)

### Data Validation
- Verify session boundaries
- Check for data gaps (missing candles)
- Validate volume consistency
- Confirm bid-ask data accuracy

---

## 📚 Reference: VN Market Behavior Patterns

### Morning Session (09:15-11:30)
- 40-60% of daily volume
- High volatility (traders building positions)
- Direction set by ATO
- Trend continuation likely

### Lunch Break (11:30-13:00)
- Complete halt (no trading)
- Traders review morning action
- Prepare for afternoon

### Afternoon Session (13:00-15:00)
- 40-60% of daily volume
- Momentum continuation from morning
- Possible reversal if morning weak
- Close very active (last 15 minutes)

### Key Time Windows
- 09:15-09:30 (ATO): Volume spike, direction set
- 10:30-11:30 (Morning end): Momentum confirmation
- 14:45-15:00 (Close): Final position building

---

## 💡 Practical Tips for Implementation

1. **Always combine Volume + Price**
   - Price break without volume = unreliable
   - Volume spike without price move = accumulation/distribution

2. **Session correlation matters**
   - Morning strength usually continues to afternoon
   - But reversals happen → need volume confirmation

3. **Liquidity first, entry second**
   - Never entry with wide spread
   - Wait for good liquidity even if miss a few points

4. **Levels are zones, not lines**
   - S/R not single point but cluster
   - Multiple touches = stronger level

5. **VN traders follow patterns**
   - Round numbers, psychological levels
   - Previous highs/lows are magnets
   - Use this knowledge for prediction

---

**Last Updated**: 2026-08-04
**VN Market Focused**: Yes
**Practical for Traders**: Yes
**Ready for Implementation**: Yes

# 🔬 BioTrial Quality Analyzer

### Automated Due Diligence for Biotech Catalyst Trading

## The Problem
Retail traders lose money on "positive" biotech data because they ignore structural trial flaws (surrogate endpoints, skipped Phase 2) or fail to account for imminent dilution risk.

## The Solution
This tool automates scientific due diligence by combining live market data with clinical trial quality analysis.

### Red Flags Detected:
1. **Phase 2 Skips** - Historical Phase 3 success drops to 31% vs. 57% with proper Phase 2
2. **Single-Arm Trials** - No control group = high placebo/bias risk
3. **Surrogate Endpoints** - PFS vs OS = higher regulatory rejection risk
4. **Underpowered Studies** - N<20 in Phase 1 = statistically unreliable
5. **Dilution Risk** - <4 months cash runway = offering imminent

## Tech Stack
- **Python** - Data processing and analysis logic
- **Streamlit** - Interactive web dashboard
- **yfinance** - Real-time market data
- **Pandas** - Data manipulation

## Features
- Automated date filtering (past events hidden)
- Live price fetching from Yahoo Finance
- Research-backed red flag detection
- Risk scoring (0-5 flags per catalyst)
- Trade verdict generator

## Data Sources
- Clinical trial design: Manual research (ClinicalTrials.gov)
- Success rates: Industry research (Intuition Labs, FDA guidance)
- Market data: yfinance API

---

**Built by:** [Your Name]  
**Education:** Finance MSc @ Nova SBE | Biology BSc @ UWE Bristol  
**Experience:** 6 years biotech catalyst trading

⚠️ **Disclaimer:** Financial metrics and catalyst dates are illustrative for demonstration purposes.


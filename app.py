import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import date

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="BioTrial Pro", layout="wide")
st.title("🔬 Automated Clinical Trial Quality Analyzer")
st.markdown("### ⚡ Live Feed + Structural Flaw Detection")

# 2. LOAD DATA FROM CSV
try:
    df = pd.read_csv("catalyst_database.csv", encoding='utf-8')
    df['Catalyst_Date'] = pd.to_datetime(df['Catalyst_Date']).dt.date
    df['Cash_Runway_Mo'] = pd.to_numeric(df['Cash_Runway_Mo'], errors='coerce')
    df['Enrollment_N'] = pd.to_numeric(df['Enrollment_N'], errors='coerce')
except FileNotFoundError:
    st.error("⚠️ Error: 'catalyst_database.csv' not found.")
    st.stop()
except Exception as e:
    st.error(f"⚠️ Error loading CSV: {e}")
    st.stop()

# 3. FILTER PAST EVENTS
today = date.today()
df = df[df['Catalyst_Date'] >= today].sort_values(by='Catalyst_Date')

if df.empty:
    st.warning("No upcoming catalysts found in database.")
    st.stop()

# 4. FETCH LIVE PRICES
@st.cache_data(ttl=3600)
def get_live_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        price = stock.info.get('currentPrice')
        if price is None or price == 0:
            hist = stock.history(period="1d")
            if not hist.empty:
                price = hist['Close'].iloc[-1]
        return price if price else None
    except Exception:
        return None

df_top = df.head(10).copy()
with st.spinner(f"📡 Fetching live prices for {len(df_top)} catalysts..."):
    df_top['Live_Price'] = df_top['Ticker'].apply(get_live_price)

# 5. QUALITY ANALYSIS
def analyze_trial_quality(row):
    flags = []
    
    if row['Stage'] == 'Phase 3' and 'Skipped' in str(row['Prior_Phase_Data']):
        flags.append("🚩 **CRITICAL: Skipped Phase 2.** Historical Phase 3 success rate drops to 31% vs. 57% with proper Phase 2.")
    
    if 'Single Arm' in str(row['Control_Arm']):
        flags.append("⚠️ **Single Arm Trial.** No control group = high risk of placebo effect masquerading as efficacy.")
    
    if 'Surrogate' in str(row['Endpoint_Type']):
        flags.append("⚠️ **Surrogate Endpoint.** FDA prefers clinical outcomes (OS) over surrogates (PFS) for full approval.")
    
    if row['Stage'] == 'Phase 1' and pd.notna(row['Enrollment_N']) and row['Enrollment_N'] < 20:
        flags.append(f"🚩 **Underpowered (N={int(row['Enrollment_N'])}).** Sample size too small for statistical reliability.")
    
    if pd.notna(row['Cash_Runway_Mo']) and row['Cash_Runway_Mo'] < 4:
        flags.append(f"💸 **Dilution Zone.** Only {row['Cash_Runway_Mo']:.1f} months cash. Offering likely within 8 weeks.")
    
    return flags

df_top['Red_Flags'] = df_top.apply(analyze_trial_quality, axis=1)
df_top['Flag_Count'] = df_top['Red_Flags'].apply(len)

# 6. DASHBOARD
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📅 Next 10 Catalysts")
    
    display = df_top.copy()
    display['Price'] = display['Live_Price'].apply(lambda x: f"${x:.2f}" if pd.notna(x) else "N/A")
    
    st.dataframe(
        display[['Ticker', 'Catalyst_Date', 'Event', 'Stage', 'Price', 'Flag_Count']],
        hide_index=True,
        use_container_width=True,
        column_config={
            "Flag_Count": st.column_config.NumberColumn("🚩 Flags", help="Number of structural red flags detected"),
            "Catalyst_Date": st.column_config.DateColumn("Date", format="YYYY-MM-DD")
        }
    )

with col2:
    st.subheader("🧐 Deep Dive")
    selected = st.selectbox("Select Ticker:", df_top['Ticker'])
    
    row = df_top[df_top['Ticker'] == selected].iloc[0]
    
    st.markdown(f"### {row['Ticker']}: {row['Event']}")
    
    c1, c2 = st.columns(2)
    price_str = f"${row['Live_Price']:.2f}" if pd.notna(row['Live_Price']) else "N/A"
    c1.metric("Live Price", price_str)
    
    if pd.notna(row['Cash_Runway_Mo']):
        c2.metric("Cash Runway", f"{row['Cash_Runway_Mo']:.1f} Mo")
    
    st.divider()
    
    if row['Flag_Count'] > 0:
        st.error(f"**{row['Flag_Count']} Structural Flaw(s) Detected:**")
        for flag in row['Red_Flags']:
            st.markdown(flag)
        st.markdown("---")
        st.markdown("**Verdict: ⛔ AVOID / SHORT SETUP**")
    else:
        st.success("✅ **Clean Trial Design**")
        st.markdown("**Verdict: 🟢 LONG OK** (pending catalyst outcome)")

st.markdown("---")
st.caption("Data: yfinance (prices), manual research (trial design)")


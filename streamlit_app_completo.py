import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Screener Sala Trading", layout="wide")

st.markdown("## Sala Trading Screener - Top 10 Azioni S&P 500")

# === Sidebar ===
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/3/3f/Trading_view_logo.png", width=150)
st.sidebar.markdown("### Filtri fondamentali")

sectors = ['All', 'Technology', 'Healthcare', 'Financial Services', 'Consumer Defensive', 'Energy', 'Industrials']
selected_sector = st.sidebar.selectbox("Settore", sectors)

market_caps = ['All', 'Large Cap (>10B)', 'Mid Cap (2B-10B)', 'Small Cap (<2B)']
selected_cap = st.sidebar.selectbox("Capitalizzazione", market_caps)

pe_min, pe_max = st.sidebar.slider("PE Ratio", 0, 100, (0, 25))
margin_min, margin_max = st.sidebar.slider("Margine Operativo (%)", 0, 100, (10, 100))
growth_min, growth_max = st.sidebar.slider("Crescita utile (%)", -50, 100, (5, 100))

# === Dati simulati (in demo) ===
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'JNJ', 'XOM', 'PG', 'NVDA', 'UNH']
names = ['Apple', 'Microsoft', 'Alphabet', 'Amazon', 'Meta', 'Johnson & Johnson', 'ExxonMobil', 'Procter & Gamble', 'Nvidia', 'UnitedHealth']

# Genero dataframe fittizio (può essere sostituito con scraping o API reali)
data = []
for i, ticker in enumerate(tickers):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")
    pe = round(15 + i*2, 2)
    margin = 10 + i * 3
    growth = 10 + i * 4
    cap = 'Large Cap (>10B)'
    sector = sectors[i % len(sectors)]
    price = hist['Close'].iloc[-1] if not hist.empty else 0
    data.append([ticker, names[i], sector, cap, pe, margin, growth, price])

df = pd.DataFrame(data, columns=['Ticker', 'Nome', 'Settore', 'Cap', 'PE', 'Margine', 'Crescita', 'Prezzo'])

# === Applica i filtri ===
if selected_sector != 'All':
    df = df[df['Settore'] == selected_sector]

if selected_cap != 'All':
    df = df[df['Cap'] == selected_cap]

df = df[df['PE'].between(pe_min, pe_max)]
df = df[df['Margine'].between(margin_min, margin_max)]
df = df[df['Crescita'].between(growth_min, growth_max)]

# Ordina per crescita utile
df = df.sort_values(by="Crescita", ascending=False).head(10)

# === Visualizza risultati ===
st.markdown("### Risultati filtrati")
st.dataframe(df, use_container_width=True)

# === Grafici ===
st.markdown("### Grafici di prezzo (ultimi 12 mesi)")
for ticker in df['Ticker']:
    st.markdown(f"**{ticker}**")
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")
    st.line_chart(hist['Close'])

# === Footer ===
st.markdown("---")
st.markdown("App creata da `ziosalatrading` - [GitHub](https://github.com/ziosalatrading/screener-sala)")
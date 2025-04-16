import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ===== GOOGLE SHEETS SETUP =====
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Sala_Portafoglio_Storico").sheet1  # Cambia con il nome del tuo file se diverso

# ===== APP UI =====
st.title("📊 Screener Azioni S&P500")
st.write("Filtra le migliori azioni con criteri tecnici e fondamentali")

selettore_settore = st.selectbox("Seleziona settore", ["Tutti", "Technology", "Healthcare", "Financial", "Energy"])
pe_max = st.slider("P/E massimo", 0, 50, 20)
margine_min = st.slider("Margine minimo (%)", 0, 50, 10)
crescita_min = st.slider("Crescita utile (%) minimo", 0, 50, 10)

# ===== DATI AZIONI (mock per esempio) =====
data = {
    "Ticker": ["AAPL", "MSFT", "GOOG", "AMZN"],
    "Settore": ["Technology", "Technology", "Technology", "Consumer"],
    "P/E": [15, 25, 18, 60],
    "Margine": [22, 30, 25, 5],
    "Crescita utile": [15, 12, 18, -3],
    "Prezzo": [175.3, 310.5, 138.9, 102.1]
}
df = pd.DataFrame(data)

# ===== FILTRI =====
if selettore_settore != "Tutti":
    df = df[df["Settore"] == selettore_settore]

filtro = (df["P/E"] < pe_max) & (df["Margine"] > margine_min) & (df["Crescita utile"] > crescita_min)
df_filtrato = df[filtro]

# ===== MOSTRA =====
st.dataframe(df_filtrato)

# ===== CRONOLOGIA SU SHEETS =====
if st.button("📤 Salva portafoglio su Google Sheets"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    for _, row in df_filtrato.iterrows():
        sheet.append_row([now, row["Ticker"], row["Prezzo"], row["P/E"], row["Margine"], row["Crescita utile"]])
    st.success("✅ Portafoglio salvato su Google Sheets!")
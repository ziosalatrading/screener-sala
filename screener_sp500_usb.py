
import yfinance as yf
import pandas as pd
import datetime
import os

tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'JPM', 'UNH', 'XOM', 'PG']

end_date = datetime.datetime.today()
start_date = end_date - datetime.timedelta(days=180)
results = []

for ticker in tickers:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)
        if hist.shape[0] < 50:
            continue

        hist['EMA50'] = hist['Close'].ewm(span=50).mean()
        hist['RSI'] = 100 - (100 / (1 + hist['Close'].pct_change().rolling(14).mean() / hist['Close'].pct_change().rolling(14).std()))
        macd_line = hist['Close'].ewm(span=12).mean() - hist['Close'].ewm(span=26).mean()
        signal_line = macd_line.ewm(span=9).mean()

        last_close = hist['Close'][-1]
        last_ema50 = hist['EMA50'][-1]
        last_rsi = hist['RSI'][-1]
        last_macd = macd_line[-1]
        last_signal = signal_line[-1]

        tech_ok = (
            last_close > last_ema50 and
            50 < last_rsi < 70 and
            last_macd > last_signal
        )

        pe_ratio = stock.info.get('trailingPE', None)
        profit_margin = stock.info.get('profitMargins', None)
        net_income = stock.info.get('netIncomeToCommon', None)

        fund_ok = (
            pe_ratio is not None and pe_ratio < 20 and
            profit_margin is not None and profit_margin > 0 and
            net_income is not None and net_income > 0
        )

        if tech_ok and fund_ok:
            results.append({
                'Ticker': ticker,
                'Price': round(last_close, 2),
                'PE Ratio': round(pe_ratio, 2),
                'Profit Margin': round(profit_margin, 3),
                'RSI': round(last_rsi, 2),
                'MACD > Signal': last_macd > last_signal,
            })
    except Exception as e:
        print(f"Errore con {ticker}: {e}")

df_results = pd.DataFrame(results)
df_results = df_results.sort_values(by='PE Ratio').head(10)

output_file = os.path.join(os.getcwd(), "Top10_Azioni_SP500.xlsx")
df_results.to_excel(output_file, index=False)
print(f"File creato: {output_file}")
input("Premi INVIO per chiudere.")

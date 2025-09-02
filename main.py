from valuation.graham import graham_valuation
from valuation.dcf import dcf_valuation
from valuation.ddm import ddm_valuation
from valuation.multiples import multiples_valuation
from data_fetcher import fetch_financial_data, fetch_historical_data
import matplotlib.pyplot as plt
import mplfinance as mpf
import os

def average_valuation(ticker):
    try:
        data = fetch_financial_data(ticker)
        market_price = data["price"]

        graham = graham_valuation(data)
        dcf = dcf_valuation(data)
        ddm = ddm_valuation(data)
        multiples = multiples_valuation(data)

        valuations = {
            "Graham": graham,
            "DCF": dcf,
            "DDM": ddm,
            "Multiples": multiples
        }

        valid_vals = [v for v in valuations.values() if v is not None]
        avg = sum(valid_vals) / len(valid_vals) if valid_vals else None

        html_content = f"""
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <title>Raport wyceny - {ticker}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f9f9f9;
            color: #333;
        }}
        h1 {{
            color: #0073e6;
        }}
        ul {{
            list-style-type: none;
            padding: 0;
        }}
        li {{
            padding: 4px 0;
        }}
        img {{
            max-width: 100%;
            height: auto;
            margin-top: 20px;
            border: 1px solid #ccc;
            box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
        }}
    </style>
</head>
<body>
    <h1>Wyceny dla spółki {ticker}</h1>
    <ul>
"""

        for method, value in valuations.items():
            if value is not None:
                html_content += f"<li><b>{method}</b>: {value:.2f} USD</li>"
            else:
                html_content += f"<li><b>{method}</b>: Brak danych</li>"
        html_content += f"<li><b>Cena rynkowa</b>: {market_price:.2f} USD</li>"
        if avg:
            html_content += f"<li><b>Średnia wycena</b>: {avg:.2f} USD</li>"
        else:
            html_content += "<li><b>Średnia wycena</b>: Brak danych</li>"
        html_content += "</ul>"

        labels = list(valuations.keys()) + ["Cena rynkowa"]
        values = [valuations[k] if valuations[k] is not None else 0 for k in valuations] + [market_price]

        chart_file = f"{ticker}_valuation_chart.png"
        plt.figure(figsize=(10, 6))
        plt.bar(labels, values)
        plt.axhline(y=market_price, color='r', linestyle='--', label=f"Cena rynkowa: {market_price:.2f} USD")
        plt.title(f"Wyceny vs. cena rynkowa dla {ticker}")
        plt.ylabel("Wartość (USD)")
        plt.legend()
        plt.grid(True, axis='y')
        plt.tight_layout()
        plt.savefig(chart_file)
        plt.close()

        html_content += f'<img src="{chart_file}" alt="Wyceny i cena rynkowa"><br>'

        hist_data = fetch_historical_data(ticker)
        if hist_data is not None:
            candle_chart_file = f"{ticker}_candlestick.png"
            mpf.plot(hist_data, type='candle', style='yahoo', title=f"Świece japońskie: {ticker}",
                     ylabel="Cena (USD)", savefig=candle_chart_file)

            html_content += f'<img src="{candle_chart_file}" alt="Świece japońskie"><br>'
        else:
            print("Brak danych historycznych.")

        html_content += "</body></html>"

        html_path = os.path.abspath(f"{ticker}_valuation_report.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"✅ Raport HTML zapisany w: {html_path}")

    except Exception as e:
        print("❌ Błąd podczas generowania raportu:", e)

if __name__ == "__main__":
    ticker = input("Podaj ticker spółki: ").upper()
    average_valuation(ticker)

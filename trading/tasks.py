from celery import shared_task
import yfinance as yf

@shared_task
def get_chart(symbol):

    stock = yf.Ticker(symbol)

    df = stock.history(
        period="1d",
        interval="5m"
    )

    candles = []

    for index,row in df.iterrows():

        candles.append({

            "time":
            int(index.timestamp()),

            "open":
            round(row["Open"],2),

            "high":
            round(row["High"],2),

            "low":
            round(row["Low"],2),

            "close":
            round(row["Close"],2)

        })

    return candles
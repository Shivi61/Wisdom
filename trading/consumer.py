from channels.generic.websocket import AsyncWebsocketConsumer

import json
import asyncio
import yfinance as yf
import random


class TradeConsumer(
    AsyncWebsocketConsumer
):

    async def connect(self):

        await self.accept()

        self.running=False

    async def disconnect(
        self,
        close_code
    ):

        self.running=False

    async def receive(
        self,
        text_data
    ):

        data=json.loads(
            text_data
        )

        stock=data.get(
            "stock",
            "AAPL"
        )

        self.running=True

        while self.running:

            ticker=yf.Ticker(
                stock
            )

            history=ticker.history(

                period="1d",

                interval="5m"

            )

            candles=[]

            rows=history.tail(
                50
            )

            for idx,row in rows.iterrows():

                close=float(
                    row["Close"]
                )

                close+=random.uniform(
                    -0.3,
                    0.3
                )

                candles.append({

                    "time":
                    int(
                        idx.timestamp()
                    ),

                    "open":
                    float(
                        row["Open"]
                    ),

                    "high":
                    float(
                        row["High"]
                    ),

                    "low":
                    float(
                        row["Low"]
                    ),

                    "close":
                    round(
                        close,
                        2
                    )

                })

            await self.send(

                text_data=json.dumps({

                    "candles":
                    candles

                })

            )

            await asyncio.sleep(
                5
            )
import pandas as pd
from backtesting import Backtest, Strategy
from datetime import timedelta, date
import yfinance as yf
from datetime import date
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def WilliamsAlligator(high, low, jaw_len, teeth_len, lips_len, jaw_offset, teeth_offset, lips_offset):    
    df = pd.DataFrame({'high': high, 'low': low})
    df['median'] = (df['high'] + df['low']) / 2    
    jaw = df['median'].rolling(window=jaw_len).mean().shift(jaw_offset)
    teeth = df['median'].rolling(window=teeth_len).mean().shift(teeth_offset)
    lips = df['median'].rolling(window=lips_len).mean().shift(lips_offset)
    return jaw, teeth, lips

today = date.today()
start_day = today - timedelta(days=58)
market = "BTC-USD"
dataframe = "15m"
# Download the backtest data
data = yf.download(market, start=start_day, end=today, interval=dataframe)


class alligator(Strategy):
    def init(self):
        self.high = self.data.High
        self.low = self.data.Low
        jaw_len = 13
        teeth_len = 8
        lips_len = 5
        jaw_offset = 8
        teeth_offset = 5
        lips_offset = 3
        self.jaw, self.teeth, self.lips = self.I(WilliamsAlligator, self.high, self.low, jaw_len, teeth_len, lips_len, jaw_offset, teeth_offset, lips_offset)
   
    def next(self):
        self.price = self.data.Close
        self.r = False # This indicates the position
        if self.price[-1] > self.jaw[-1] and self.price[-1] > self.teeth[-1] and self.price[-1] > self.lips[-1] and not self.r:
            # Buy
            self.buy()
            self.r = True # Position = True
        elif self.price[-1] < self.jaw[-1] or self.price[-1] < self.teeth[-1] or self.price[-1] < self.lips[-1] and self.r:
            # Sell
            self.r = False # Position = False

bt = Backtest(data, alligator, commission=0.01, exclusive_orders=True, cash=1000000)
output = bt.run()
print(output)
bt.plot()

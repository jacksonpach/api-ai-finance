import pandas as pd
from yahoo_fin import stock_info as si
from finvizfinance.quote import finvizfinance
from datetime import datetime, timedelta
import yfinance as yf
from app import config as config
from app.entities.analytic_entity import StocksAnalytics


def fields_validate(current_price, market_cap, relative_volume, volatility_week):
    return current_price and market_cap and relative_volume and volatility_week


class AnalyticsServices:

    def __init__(self):
        self.df = None
        self.stock_finviz_fundament = None
        self.stock = None
        self.analytic = []

    def set_stock_analytic(self, stock):
        self.analytic.append(stock)

    def get_stock_analytic(self):
        return self.analytic

    def get_symbols_us(self):
        tickers = si.tickers_sp500()
        self.df = pd.DataFrame(tickers)
        return set(symbol for symbol in self.df[0].values.tolist())

    def get_max_month(self, stock):
        start_day = datetime.now() + timedelta(days=-31)
        end_day = datetime.now() + timedelta()
        df_month = yf.download(stock, start=start_day, end=end_day)
        max_price = max(df_month['High'][:-1])
        last_price = df_month['High'][-1:][0]

        return max_price > last_price

    async def get_stock_analytic_data(self, asset):
        self.df = await self.get_finviz(asset)

        current_price, market_cap, relative_volume, volatility_week = self.validate_data_analytic()

        validate = fields_validate(current_price, market_cap, relative_volume, volatility_week)
        if validate:
            if market_cap > config.market_cap:
                if relative_volume > 1:
                    if volatility_week > 3:
                        if self.get_max_month(asset):
                            return StocksAnalytics(asset, current_price, market_cap, relative_volume, volatility_week)
        return ''

    def validate_data_analytic(self):
        current_price = float(self.df['Price'][0])
        market_cap = float((self.df['Market Cap'][0][:-1]))
        relative_volume = float(self.df['Rel Volume'][0])
        volatility_week = float(self.df['Volatility W'][0][:-1])
        return current_price, market_cap, relative_volume, volatility_week

    async def get_finviz(self, stock):
        self.stock = finvizfinance(stock)
        self.stock_finviz_fundament = self.stock.ticker_fundament()
        return pd.DataFrame([self.stock_finviz_fundament])

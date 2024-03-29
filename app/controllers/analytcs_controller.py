from app.services.analytics_service import AnalyticsServices


class AnalyticsController:
    def __init__(self):
        self.analytics = AnalyticsServices()

    def get_analytics(self):
        symbol_list = self.analytics.get_symbols_us()
        for symbol in symbol_list:
            self.analytics.get_stock_analytic_data(symbol)

        return self.analytics.get_stock_analytic()

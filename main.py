from fastapi import FastAPI
import uvicorn
from services.analytics_service import AnalyticsServices
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"Root": "Route: /"}


@app.get("/analytics")
async def analytics():
    a_service = AnalyticsServices()
    symbols = a_service.get_symbols_us()
    list_stocks_analytics = []

    for symbol in symbols:
        stocks_analytics = await a_service.get_stock_analytic_data(symbol)
        if (stocks_analytics != "None") and (stocks_analytics != ""):
            list_stocks_analytics.append(stocks_analytics)
            print(list_stocks_analytics)

    # print(list_stocks_analytics)
    # type(response_json)
    return {"list_stocks_analytics": list_stocks_analytics}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7000)

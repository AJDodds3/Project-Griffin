import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def get_stock_data(ticker, period="1y", interval="1d"):
    """
    Get stock data for a given ticker and time period
    period options: '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'
    interval options: '1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'
    """
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period, interval=interval)
    return hist

def plot_stock_data(df, ticker, period, interval):
    """Plot stock data with a title showing the ticker and time period"""
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Close'], label='Close Price')
    
    interval_text = "Hourly" if interval == "1h" else "Daily"
    plt.title(f'{ticker} Stock Price - {period} Period ({interval_text} Data)')
    
    plt.xlabel('Date/Time')
    plt.ylabel('Price (USD)')
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    ticker = "GME"
    periods = {
        '1': ('1d', '1h'),    # 1 day with hourly data
        '2': ('5d', '1h'),    # 5 days with hourly data
        '3': ('1mo', '1d'),   # 1 month with daily data
        '4': ('3mo', '1d'),   # 3 months with daily data
        '5': ('6mo', '1d'),   # 6 months with daily data
        '6': ('1y', '1d'),    # 1 year with daily data
        '7': ('2y', '1d'),    # 2 years with daily data
        '8': ('5y', '1d'),    # 5 years with daily data
        '9': ('10y', '1d'),   # 10 years with daily data
        '10': ('ytd', '1d'),  # Year to date with daily data
        '11': ('max', '1d')   # All time with daily data
    }
    
    while True:
        print("\nSelect time period for GameStop stock data:")
        print("1. 1 Day (Hourly)")
        print("2. 5 Days (Hourly)")
        print("3. 1 Month")
        print("4. 3 Months")
        print("5. 6 Months")
        print("6. 1 Year")
        print("7. 2 Years")
        print("8. 5 Years")
        print("9. 10 Years")
        print("10. Year to Date")
        print("11. All Time")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-11): ")
        
        if choice == '0':
            print("Exiting...")
            break
            
        if choice in periods:
            period, interval = periods[choice]
            print(f"\nFetching {ticker} data for {period} period...")
            df = get_stock_data(ticker, period, interval)
            plot_stock_data(df, ticker, period, interval)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
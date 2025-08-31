import yfinance as yf
import pandas as pd
import os
from datetime import datetime

def get_data_for_backtesting(ticker, start_date, end_date, data_dir="../data", interval='1d'):
    """
    Downloads historical stock data using yfinance and saves it to a CSV file.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL').
        start_date (str): The start date for the data in 'YYYY-MM-DD' format.
        end_date (str): The end date for the data in 'YYYY-MM-DD' format.
        data_dir (str): The directory to save the data in.

    Returns:
        str: The file path of the saved CSV file.
    """
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Create a unique filename
    filename = f"{ticker}_{start_date}_{end_date}.csv"
    filepath = os.path.join(data_dir, filename)

    # Download data
    try:
        data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
        if data.empty:
            print(f"No data found for ticker {ticker} from {start_date} to {end_date}.")
            return None
        
        # Select required columns and rename them
        data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
        data.columns = ['open', 'high', 'low', 'close', 'volume']
        
        # Calculate amount
        data['amount'] = data['close'] * data['volume']
        
        # Rename the index column
        data.index.name = 'timestamps'
        
        # Save to CSV
        data.to_csv(filepath)
        print(f"Data for {ticker} saved to {filepath}")
        return filepath
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == '__main__':
    # Example usage for minute-level data
    ticker = "BTC-USD"  # Using a stock ticker for more reliable minute data
    start_date = "2022-08-29"
    end_date = "2025-08-30"
    
    # The data will be saved in webui/data/
    # Note: yfinance may have limitations on historical minute data availability
    data_path = get_data_for_backtesting(ticker, start_date, end_date, interval='1d')
    
    if data_path:
        print(f"Data downloaded and available at: {data_path}")
        # You can now use this data_path in your backtesting.py
        # For example, by reading the CSV with pandas:
        df = pd.read_csv(data_path, index_col='timestamps', parse_dates=True)
        print("Generated data sample:")
        print(df.head())

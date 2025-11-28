import pandas as pd
import os # We'll use os.path.join for safer path construction

def load_stock_data(tickers, file_extension):
    """
    Loads historical stock data from CSV files for a list of tickers.

    Args:
        tickers (list): List of stock ticker symbols (e.g., ['NVDA', 'AAPL']).
        file_extension (str): File extension (e.g., ".csv" or ".xlsx").

    Returns:
        dict: A dictionary where keys are tickers and values are pandas DataFrames.
    """
    stock_data = {}
    
    # Define the base directory path (assuming files are in '../data/')
    base_dir = "../data/"

    for ticker in tickers:
        # Construct the full file path safely
        filename = os.path.join(base_dir, ticker + file_extension)
        
        try:
            # Check if the file is an Excel file
            if file_extension.lower() == ".xlsx":
                 df = pd.read_excel(
                    filename, 
                    index_col='Date', 
                    parse_dates=True
                )
            
            # Check if the file is a CSV file (your current default)
            elif file_extension.lower() == ".csv":
                df = pd.read_csv(
                    filename, 
                    index_col='Date', 
                    parse_dates=True
                )
            else:
                 print(f" ERROR: Unsupported file extension: {file_extension}")
                 continue
                 
            # Store the DataFrame in the dictionary
            stock_data[ticker] = df
            
            print(f" Loaded {ticker}. Shape: {df.shape}")
            
        except FileNotFoundError:
            print(f" ERROR: File '{filename}' not found. Check your file path.")
        except Exception as e:
            print(f" ERROR processing {ticker}: {e}")

    return stock_data
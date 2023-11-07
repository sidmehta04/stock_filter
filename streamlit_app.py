import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import streamlit as st

from bsedata.bse import BSE
import yfinance as yf
import openai

# Set up OpenAI API credentials
openai.api_key = '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'
# Function to fetch fundamental data and give advice
stock_name_to_code = {
    "Reliance": "500325",
    "Tata Motors": "500570",
    "Infosys": "500209",
    "Wipro": "507685",
    "HDFC Bank": "500180",
    "ICICI Bank": "532174",
    "SBI": "500112",
    "Axis Bank": "532215",
    "Bharti Airtel": "532454",
    "TCS": "532540",
    "HCL Tech": "532281",
    "L&T": "500510",
    "ITC": "500875",
    "Bajaj Finance": "500034",
    "Hind Unilever": "500696",
    # Add more mappings as needed
}

def get_stock_description(stock_name):
    # Constructing the prompt for the AI to generate the stock description
    prompt = f"Write a concise and informative description of the stock named {stock_name}."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message.content
# Placeholder function to simulate fundamental analysis retrieval
def get_fundamental_analysis(stock_code):
    # Here you would fetch and return the fundamental analysis data for the stock code
    # This is just a placeholder with simulated data
    return {
        "PE Ratio": np.random.uniform(10, 30),
        "Market Cap": np.random.uniform(100e7, 500e7)
    }

# Placeholder function to simulate technical analysis (moving average calculation)
def get_technical_analysis(stock_code):
    # Here you would fetch historical stock data and calculate technical indicators
    # This is just a placeholder with simulated data
    closing_prices = np.random.uniform(100, 200, 50)  # Simulating 50 days of closing prices
    moving_average = np.mean(closing_prices)
    return {
        "50-Day Moving Average": moving_average
    }

# Function to provide analysis based on stock name
def stock_analysis(stock_name):
    stock_code = stock_name_to_code.get(stock_name)
    if not stock_code:
        return "Stock name not found. Please check the name and try again."
    
    fundamental_analysis = get_fundamental_analysis(stock_code)
    technical_analysis = get_technical_analysis(stock_code)
    
    return fundamental_analysis, technical_analysis


# Function to display About section
def about_section():
    st.title("About")
    st.write(
        """At Money Mate Analyzer, we are on a mission to empower students and beginners in the world of stock investments. We understand that the stock market can be complex and intimidating, especially for those new to investing. That's why we've created a user-friendly platform that simplifies the stock market for you.

Our team of experts and educators have distilled years of knowledge into easy-to-understand resources, tools, and guides. Whether you're looking to learn the basics of stock trading, analyze market trends, or make informed investment decisions, we've got you covered.

With our innovative tools and educational content, you can gain confidence in your investment choices and build a strong foundation for financial success. We believe that everyone deserves the opportunity to grow their wealth through smart investing, and we're here to support you on that journey.

Join the Money Mate Analyzer community today and take the first step towards simplifying stock investments. Let's make the world of finance accessible to all students and beginners who aspire to achieve their financial goals."""
    )

# Function to display detailed descriptions of trading strategies
def strategies_section():
    st.title("Trading Strategies")

    st.header("Golden Cross Strategy")
    st.write(
        "The Golden Cross strategy is a long-term moving average strategy. It involves two moving averages: a short-term moving average (e.g., 50-day) and a long-term moving average (e.g., 200-day). When the short-term moving average crosses above the long-term moving average, it generates a buy signal."
    )
    st.write("Risk-to-Reward Ratio: 2:1")

    st.header("MACD Strategy")
    st.write(
        "The MACD (Moving Average Convergence Divergence) strategy is a momentum-based strategy. It uses the MACD line and signal line to generate buy and sell signals based on their crossovers."
    )
    st.write("Risk-to-Reward Ratio: 5:3")

    st.header("RSI Strategy")
    st.write(
        "The RSI (Relative Strength Index) strategy is a momentum oscillator strategy. It measures the speed and change of price movements and generates overbought and oversold signals."
    )
    st.write("Risk-to-Reward Ratio: 6:2")

    st.header("SMA Strategy")
    st.write(
        "The SMA (Simple Moving Average) strategy is a trend-following strategy. It uses a short-term and long-term SMA to generate buy and sell signals based on their crossovers."
    )
    st.write("Risk-to-Reward Ratio: 1:1")

# Function to fetch and display stock news
def stock_news_section():
    st.title("Stock News")
    selected_ticker = st.sidebar.selectbox(
        "Select a stock ticker",
        [
            "RELIANCE.NS",
            "INFY.NS",
            "TATAMOTORS.NS",
            "WIPRO.NS",
            "HDFCBANK.NS",
            "ICICIBANK.NS",
            "SBI.NS",
            "AXISBANK.NS",
            "BHARTIARTL.NS",
        ],
    )
    # Define the URL for stock news. You should replace 'AAPL' with the selected ticker symbol.
    url = f'https://www.google.com/search?q={selected_ticker}+stock+news&oq={selected_ticker}+stock+news&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIGCAEQRRg80gEINDU3M2owajSoAgCwAgA&sourceid=chrome&ie=UTF-8'

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        st.error(f"HTTP Error: {errh}")
        return
    except requests.exceptions.ConnectionError as errc:
        st.error(f"Connection Error: {errc}")
        return
    except requests.exceptions.Timeout as errt:
        st.error(f"Timeout Error: {errt}")
        return
    except requests.exceptions.RequestException as err:
        st.error(f"Request Exception: {err}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.find_all('h3')
    unwanted = ['BBC World News TV', 'BBC World Service Radio',
                'News daily newsletter', 'Mobile app', 'Get in touch']

    for x in list(dict.fromkeys(headlines)):
        if x.text.strip() not in unwanted:
            # Create a clickable button for each news headline
            if st.button(x.text.strip()):
                st.markdown(f"[{x.text.strip()}]({url})")

def retrieve_fundamental_data(selected_ticker):
    # Fetch live financial data from Yahoo Finance
    stock = yf.Ticker(selected_ticker)
    balance_sheet = stock.balance_sheet

    # Get the most recent year's data
    most_recent_year_data = balance_sheet.iloc[0]

    # Get the previous year's data
    previous_year_data = balance_sheet.iloc[1]

    # Calculate revenue growth (Year over Year)
    current_year_revenue = most_recent_year_data.get("Total Revenue", 0)
    previous_year_revenue = previous_year_data.get("Total Revenue", 0)

    if previous_year_revenue == 0:
        revenue_growth = None
    else:
        revenue_growth = (current_year_revenue - previous_year_revenue) / previous_year_revenue

    # Calculate profit margin
    current_year_profit = most_recent_year_data.get("Net Income", 0)
    if current_year_revenue == 0:
        profit_margin = None
    else:
        profit_margin = (current_year_profit / current_year_revenue)

    return revenue_growth, profit_margin

# Main Streamlit code
st.set_page_config(
    page_title="Stock Trading Strategy Analyzer", page_icon=":chart_with_upwards_trend:"
)

# Create navigation
nav_option = st.sidebar.selectbox("Navigation", ("Home", "About", "Strategies", "Stock News", "OpenAI Analysis"))

# Home page
if nav_option == "Home":
    st.title("Money Mate Analyzer")
    st.sidebar.title("Options")

    # Sidebar options
    selected_ticker = st.sidebar.selectbox(
        "Select a stock ticker",
        [
            "RELIANCE.NS",
            "INFY.NS",
            "TATAMOTORS.NS",
            "WIPRO.NS",
            "HDFCBANK.NS",
            "ICICIBANK.NS",
            "SBI.NS",
            "AXISBANK.NS",
            "BHARTIARTL.NS",
            "AAPL",
            "AMZN"
        ],
    )

    selected_strategy = st.sidebar.selectbox(
        "Select a strategy", ["Golden Cross", "MACD", "RSI", "SMA"]
    )

    selected_statement = st.sidebar.selectbox(
        "Select a financial statement",
        ["Balance Sheet", "P&L Statement", "Cash Flow Statement"],
    )

    st.write(
        f"You selected {selected_ticker}, {selected_strategy}, and {selected_statement}"
    )

    # Fetch financial statements
    stock = yf.Ticker(selected_ticker)
    if selected_statement == "Balance Sheet":
        st.subheader("Balance Sheet")
        st.write(stock.balance_sheet)
    elif selected_statement == "P&L Statement":
        st.subheader("P&L Statement")
        st.write(stock.financials)
    elif selected_statement == "Cash Flow Statement":
        st.subheader("Cash Flow Statement")
        st.write(stock.cashflow)

    # Define Trading Strategies and Risk-to-Reward Ratios
    risk_to_reward = {"Golden Cross": 2, "MACD": 5 / 3, "RSI": 6 / 2, "SMA": 1}

    # Golden Cross Strategy
    def golden_cross(data, selected_ticker):
        # Check if fundamental criteria are met
        if not retrieve_fundamental_data(selected_ticker):
            return 0, 0

        data["50_MA"] = data["Close"].rolling(window=50).mean()
        data["200_MA"] = data["Close"].rolling(window=200).mean()
        buy_signal = np.where(data["50_MA"] > data["200_MA"], 1, 0)
        return buy_signal[-1], data["Close"].iloc[-1]
    # MACD Strategy
    def macd(data):
        exp12 = data["Close"].ewm(span=12, adjust=False).mean()
        exp26 = data["Close"].ewm(span=26, adjust=False).mean()
        macd = exp12 - exp26
        signal = macd.ewm(span=9, adjust=False).mean()
        buy_signal = np.where(macd > signal, 1, 0)
        return buy_signal[-1], data["Close"].iloc[-1]

    # RSI Strategy
    def rsi(data, window=14):
        delta = data["Close"].diff(1)
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        buy_signal = np.where(rsi < 30, 1, np.where(rsi > 70, -1, 0))
        return buy_signal[-1], data["Close"].iloc[-1]

    # SMA Strategy
    def sma(data, window=20):
        data["SMA"] = data["Close"].rolling(window=window).mean()
        buy_signal = np.where(data["Close"] > data["SMA"], 1, -1)
        return buy_signal[-1], data["Close"].iloc[-1]

    # Strategy Mapping
    strategy_function_mapping = {
        "Golden Cross": golden_cross,
        "MACD": macd,
        "RSI": rsi,
        "SMA": sma,
    }

if st.button("Analyze Strategy"):
    st.header("Analysis Result")
    st.write("Analyzing...")

    # Fetch real-time data
    stock_data = yf.download(selected_ticker, period="5d", interval="1m")

    # Apply selected strategy (assuming you've collected enough data)
    if len(stock_data) >= 200:
        if selected_strategy == "Golden Cross":
            buy_signal, buy_price = golden_cross(stock_data.copy(), selected_ticker)
        else:
            buy_signal, buy_price = strategy_function_mapping[selected_strategy](
                stock_data.copy()
            )

        if buy_signal > 0:
            target_price = buy_price * (1 + risk_to_reward[selected_strategy] / 100)
            stop_loss = buy_price * (1 - risk_to_reward[selected_strategy] / 100)
            st.write(
                f"The stock {selected_ticker} is suitable for the {selected_strategy} strategy."
            )
            st.write(f"Buy Price: {buy_price:.2f}")
            st.write(f"Target Price: {target_price:.2f}")
            st.write(f"Stop Loss: {stop_loss:.2f}")
        else:
            st.write(
                f"The stock {selected_ticker} is not suitable for the {selected_strategy} strategy."
            )

# About page
elif nav_option == "About":
    about_section()

# Strategies page
elif nav_option == "Strategies":
    strategies_section()
elif nav_option == "Stock News":
    
    stock_news_section()

if nav_option == "OpenAI Analysis":
    # OpenAI Stock Advisor section now accepts stock names
    st.title("OpenAI Stock Advisor")

    # Get user input for stock name
    stock_name = st.text_input("Enter the stock name for advice:")
    
    if st.button("Get Analysis"):
        # Get the financial and technical analysis based on stock name
        result = stock_analysis(stock_name)
        
        if isinstance(result, tuple):
            fundamental_data, technical_data = result
            st.subheader("Fundamental Analysis")
            st.json(fundamental_data)
            st.subheader("Technical Analysis")
            st.json(technical_data)
            description = get_stock_description(stock_name)
            st.subheader("Stock Description")
            st.write(description)

        else:
            st.error(result)

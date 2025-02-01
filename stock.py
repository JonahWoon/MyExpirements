import sys
import subprocess

# Ensure yfinance is installed
try:
    import yfinance as yf
except ImportError:
    print("yfinance not found, installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance"])
    import yfinance as yf

class Stock:
    def __init__(self, symbol):
        self.symbol = symbol
        self.data = None
    
    def update_price(self):
        stock_data = yf.Ticker(self.symbol)
        self.data = stock_data.history(period='1d')
        return self.get_price()
    
    def get_price(self):
        if self.data is not None and not self.data.empty:
            return self.data['Close'].iloc[-1]
        return None

class Portfolio:
    def __init__(self, balance=1000):
        self.holdings = {}  # {symbol: (shares, avg_price)}
        self.balance = balance
    
    def buy_stock(self, symbol, shares):
        stock = Stock(symbol)
        price = stock.update_price()
        if price is None:
            print("Error fetching stock price. Try again.")
            return
        cost = price * shares
        
        if self.balance >= cost:
            self.balance -= cost
            if symbol in self.holdings:
                total_shares, avg_price = self.holdings[symbol]
                new_avg_price = ((total_shares * avg_price) + cost) / (total_shares + shares)
                self.holdings[symbol] = (total_shares + shares, new_avg_price)
            else:
                self.holdings[symbol] = (shares, price)
            print(f"Bought {shares} of {symbol} at ${price:.2f}")
        else:
            print("Insufficient funds")
    
    def sell_stock(self, symbol, shares):
        if symbol in self.holdings and self.holdings[symbol][0] >= shares:
            stock = Stock(symbol)
            price = stock.update_price()
            if price is None:
                print("Error fetching stock price. Try again.")
                return
            self.balance += price * shares
            total_shares, avg_price = self.holdings[symbol]
            if total_shares == shares:
                del self.holdings[symbol]
            else:
                self.holdings[symbol] = (total_shares - shares, avg_price)
            print(f"Sold {shares} of {symbol} at ${price:.2f}")
        else:
            print("Not enough shares to sell")
    
    def view_portfolio(self):
        print("\nPortfolio:")
        for symbol, (shares, avg_price) in self.holdings.items():
            print(f"{symbol}: {shares} shares, Avg Price: ${avg_price:.2f}")
        print(f"Balance: ${self.balance:.2f}")

if __name__ == "__main__":
    portfolio = Portfolio()
    while True:
        print("\nOptions: buy, sell, view, exit")
        action = input("Enter action: ").strip().lower()
        if action == "buy":
            symbol = input("Enter stock symbol: ").strip().upper()
            try:
                shares = int(input("Enter number of shares: ").strip())
                portfolio.buy_stock(symbol, shares)
            except ValueError:
                print("Invalid number of shares")
        elif action == "sell":
            symbol = input("Enter stock symbol: ").strip().upper()
            try:
                shares = int(input("Enter number of shares: ").strip())
                portfolio.sell_stock(symbol, shares)
            except ValueError:
                print("Invalid number of shares")
        elif action == "view":
            portfolio.view_portfolio()
        elif action == "exit":
            print("Exiting...")
            break
        else:
            print("Invalid action")

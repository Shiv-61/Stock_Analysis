import tkinter as tk
from tkinter import messagebox
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def fetch_stock_data():
    stock_name = entry_stock.get().strip().upper()
    if not stock_name:
        messagebox.showwarning("Input Error", "Please enter a valid stock ticker symbol like AAPL for Apple or AMZN for Amazon.")
        return
    
    try:
        # Fetch stock data
        stock = yf.Ticker(stock_name)
        info = stock.info
        history = stock.history(period="6mo")  # Fetch 6 months of historical data

        if history.empty:
            messagebox.showwarning("Data Error", f"No historical data available for {stock_name}.")
            return

        # Extract current, 52-week low, and 52-week high prices
        current_price = info.get("currentPrice", "N/A")
        year_low = info.get("fiftyTwoWeekLow", "N/A")
        year_high = info.get("fiftyTwoWeekHigh", "N/A")

        # Display stock details
        lbl_result.config(
            text=f"Stock: {stock_name}\n"
                 f"Current Price (in $): {current_price}\n"
                 f"52-Week Low (in $): {year_low}\n"
                 f"52-Week High (in $): {year_high}"
        )

        # Suggest long or short-term investment
        if current_price != "N/A" and year_low != "N/A" and year_high != "N/A":
            price_range = year_high - year_low
            relative_position = (current_price - year_low) / price_range if price_range else 0.5
            if relative_position < 0.3:
                lbl_suggestion.config(text="Good for long-term investment (near 52-week low).", fg="green")
            elif relative_position > 0.7:
                lbl_suggestion.config(text="Risky for short-term gains (near 52-week high).", fg="red")
            else:
                lbl_suggestion.config(text="Moderately positioned, evaluate carefully.", fg="orange")
        else:
            lbl_suggestion.config(text="Insufficient data to suggest investment strategy.", fg="grey")

        # Plot the graph
        plot_stock_graph(history, stock_name)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data for {stock_name}. Error: {e}")

def plot_stock_graph(history, stock_name):
    # Clear the previous graph if any
    for widget in graph_frame.winfo_children():
        widget.destroy()

    # Create a new figure
    fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
    ax.plot(history.index, history['Close'], label=f"{stock_name} Closing Price", color="blue")
    ax.set_title(f"{stock_name} Stock Price (Last 6 Months)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Closing Price ($)")
    ax.legend()
    ax.grid()

    # Embed the figure in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Create the main application window
root = tk.Tk()
root.title("Stock Analyzer with Graph")
root.geometry("800x600")

# Create widgets
lbl_prompt = tk.Label(root, text="Enter Stock Ticker Symbol:", font=("Arial", 12))
lbl_prompt.pack(pady=10)

entry_stock = tk.Entry(root, width=20, font=("Arial", 14))
entry_stock.pack(pady=5)

btn_fetch = tk.Button(root, text="Fetch Data", command=fetch_stock_data, font=("Arial", 12))
btn_fetch.pack(pady=10)

lbl_result = tk.Label(root, text="", font=("Arial", 12), justify="left")
lbl_result.pack(pady=10)

lbl_suggestion = tk.Label(root, text="", font=("Arial", 12), wraplength=350, justify="left")
lbl_suggestion.pack(pady=10)

# Create a frame for the graph
graph_frame = tk.Frame(root)
graph_frame.pack(fill=tk.BOTH, expand=True, pady=20)

# Run the application
root.mainloop()

# 💰 Asset Allocation Bot

### *Single-File Python Portfolio Optimizer*

This project contains a Python script designed to perform automated
**asset allocation** and **portfolio optimization** using principles
from Modern Portfolio Theory (MPT).\
The tool computes optimal portfolio weights based on user-defined
criteria such as:

-   Maximizing the **Sharpe Ratio**
-   Minimizing **volatility**
-   Achieving a **target return**

All functionality is contained in a **single Python file**.

------------------------------------------------------------------------

## ✨ Features

### **Data Fetching**

Retrieves historical price data for a configurable list of tickers using
`yfinance`.

### **Portfolio Optimization**

Uses Modern Portfolio Theory:

Expected Returns:

$$
\mu = \mathbb{E}[r]
$$

Covariance Matrix:

$$
\Sigma = \text{Cov}(r)
$$

Portfolio Return:

$$
R_p = w^\top \mu
$$

Portfolio Volatility:

$$
\sigma_p = \sqrt{w^\top \Sigma w}
$$



### **Sharpe Ratio Maximization**

Finds:

$$
\max_w \frac{R_p - R_f}{\sigma_p}
$$

### **Minimum Variance Portfolio**

Solves:

$$
\min_w \sigma_p
$$

### **Visualization**

Matplotlib plots for the efficient frontier.

### **Single-File Simplicity**

All logic lives inside one file: `asset_allocator.py`.

------------------------------------------------------------------------

## 🛠️ Prerequisites

Python **3.8+** required.

Install dependencies:

``` bash
pip install pandas numpy scipy yfinance matplotlib
```

  Library      Purpose
  ------------ ---------------------------------
  pandas       Time series handling
  numpy        Numerical operations
  scipy        Optimization routines
  yfinance     Fetching market data
  matplotlib   Plotting the Efficient Frontier

------------------------------------------------------------------------

## 🚀 Installation & Setup

### **1. Clone the Repository**

``` bash
git clone https://your-repo-link.git
cd asset-allocation-bot
```

### **2. Install Dependencies**

``` bash
pip install pandas numpy scipy yfinance matplotlib
```

------------------------------------------------------------------------

## 📖 Usage

### **1. Configure the Script**

Open `asset_allocator.py` and adjust:

  ----------------------------------------------------------------------------------------
  Variable           Description                             Default Example
  ------------------ --------------------------------------- -----------------------------
  `TICKERS`          Asset symbols                           `['SPY','QQQ','GLD','BND']`

  `START_DATE`       Historical data start                   `'2018-01-01'`

  `END_DATE`         End date                                `datetime.now()`

  `RISK_FREE_RATE`   Risk-free rate (R_f)                    `0.02`
  ----------------------------------------------------------------------------------------

------------------------------------------------------------------------

### **2. Run the Bot**

``` bash
python asset_allocator.py
```

------------------------------------------------------------------------

## 📊 Reviewing Output

The script prints:

### **Maximum Sharpe Ratio Portfolio**

- Expected Return

$$
R_p = w^\top \mu
$$

- Volatility

$$
\sigma_p = \sqrt{w^\top \Sigma w}
$$

- Sharpe Ratio
  
$$
S = \frac{R_p - R_f}{\sigma_p}
$$

- Optimal weights

$$
w^\*
$$



### **Minimum Volatility Portfolio**

-   Expected Return
-   Volatility
-   Sharpe Ratio
-   Optimal weights

If plotting is enabled, the **Efficient Frontier** will be displayed.

------------------------------------------------------------------------

## 📁 File Structure

    asset-allocation-bot/
    ├── asset_allocator.py
    └── README.md

------------------------------------------------------------------------

## 💡 Customization

### **Change Tickers**

Modify `TICKERS` to analyze any set of assets.

### **Adjust Time Horizon**

Update `START_DATE` for shorter or longer historical windows.

### **Add Constraints**

Modify the `scipy.optimize.minimize` call to include constraints such
as:

$$
w_i \le 0.30
$$

or non-negativity constraints:

$$
w_i \ge 0
$$

---

## 🤝 Contributions

Contributions are welcome! Whether you want to fix a bug, improve performance, add new optimization methods, or enhance documentation, your help is appreciated. To contribute:

1. Fork the repository  
2. Create a new branch for your feature or fix  
3. Commit your changes with clear messages  
4. Submit a pull request describing what you changed and why  

Please ensure your modifications follow best practices and maintain the simplicity of the single-file architecture.

---

## 🚀 Future Improvements

Several enhancements can make this project more powerful and flexible:

### **1. More Optimization Models**
- Add Conditional Value at Risk (CVaR) optimization  
- Add Black–Litterman allocation  
- Add risk-parity portfolio construction  
- Add reinforcement learning–based portfolio allocation models  

### **2. Enhanced Constraints**
- Sector/country allocation limits  
- Maximum/minimum asset exposure  
- Leverage and short-selling options  

### **3. Improved Visualization**
- Interactive charts using Plotly  
- Rolling return/volatility charts  
- Risk contribution bar plots  

### **4. Performance Enhancements**
- Caching of downloaded data  
- Parallelized Monte Carlo simulations  
- Faster optimization using NumPy or JAX  

### **5. Better User Interface**
- Command-line flags for custom inputs  
- Config file (YAML/JSON) for portfolio settings  
- Optional minimal GUI using Streamlit  

### **6. More Robust Error Handling**
- Graceful handling of missing ticker data  
- Logging system for debugging  
- Automatic retries for API rate limits  

---

## ⚠️ Disclaimer

This project is intended **for educational and research purposes only**.  
It has **not been tested in real-world trading environments**, and the results should **not** be considered financial advice.  
Market conditions, model assumptions, and data sources can significantly impact performance.

Always perform your own due diligence and consult a licensed financial professional before making investment decisions.

---


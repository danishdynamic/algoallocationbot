
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.2-green)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2.0-blue)](https://reactjs.org/)
[![Docker](https://img.shields.io/badge/Docker-20.10.17-blue)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# 💰 Algo Asset Allocation Bot

**End-to-End Asset Allocation Platform with FastAPI + React (TypeScript)**

This project is a **full-stack quantitative asset allocation system** that combines:

* 📈 **Python-based portfolio & momentum backtesting**
* ⚙️ **FastAPI backend API**
* 🖥️ **React + TypeScript frontend**
* 🚦 **Rate-limited endpoints**
* 📤 **CSV export for results**
* 📊 Extensible architecture for future models

The system allows users to run asset allocation strategies via a REST API and visualize results through a modern web UI.

---

## 🧠 Core Concepts

* Momentum-based asset allocation
* Moving-average crossover strategies
* Portfolio performance metrics (Sharpe, volatility)
* Separation of **quant logic** from **API** and **UI**

---

## ✨ Features

### 🔧 Backend (FastAPI)

* REST API for running allocation/backtests
* Modular Python architecture
* Rate-limited endpoints (API abuse protection)
* CSV export of transactions & portfolio results
* Clean request/response schemas (Pydantic)
* Ready for database integration (PostgreSQL)

### 🖥️ Frontend (React + TypeScript)

* Modern Vite-based React app
* Component-based UI (Header, Footer, Pages)
* API service abstraction
* Extensible for charts & dashboards
* Clean separation of concerns

### 📊 Quant Engine

* Historical price data via `yfinance`
* Momentum strategy with:

  * Short/long moving averages
  * Market regime filter (ACWI)
* Backtest engine with:

  * Transaction tracking
  * Sharpe ratio
  * Volatility
* CSV export for offline analysis

---

## 🏗️ Project Structure

```
algoallocationbot/
│
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI entry point
│   │   ├── assetbot.py        # Core backtest & allocation logic
│   │   ├── schemas.py         # Request/response models
│   │   ├── rate_limit.py      # API rate limiting
│   │   └── __init__.py
│   └── requirements.txt
│
├── frontend/
│   └── asset-ui/
│       ├── src/
│       │   ├── components/    # Header, Footer, UI components
│       │   ├── pages/         # Home, future views
│       │   ├── services/      # API calls
│       │   ├── App.tsx
│       │   └── main.tsx
│       └── package.json
│
├── README.md
└── .gitignore
```

---

## 🛠️ Tech Stack

### Backend

* Python 3.9+
* FastAPI
* Pydantic
* yfinance
* pandas / numpy
* Uvicorn

### Frontend

* React
* TypeScript
* Vite
* Axios / Fetch API

### Data

* Yahoo Finance (market data)
* CSV exports
* PostgreSQL (planned)

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/algoallocationbot.git
cd algoallocationbot
```

---

## ⚙️ Backend Setup (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn app.main:app --reload
```

API docs available at:

```
http://localhost:8000/docs
```

---

## 🖥️ Frontend Setup (React + TypeScript)

```bash
cd frontend/asset-ui
npm install
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

## 🔌 API Overview

### POST `/allocate`

Runs an asset allocation/backtest.

**Request**

```json
{
  "symbol": "AAPL",
  "initial_money": 100000
}
```

**Response**

```json
{
  "symbol": "AAPL",
  "sharpe": 1.42,
  "volatility": 0.18,
  "final_account_value": 132450,
  "transactions": {...}
}
```

---

## 📤 CSV Export

* Portfolio transactions can be exported as CSV
* Useful for:

  * Excel analysis
  * Research notebooks
  * Auditing strategies

---

## 🚦 Rate Limiting

* API endpoints are rate-limited
* Prevents abuse and accidental overload
* Ready for production hardening

---

## 🧪 Development Workflow

* Feature branches (`feature/ui-fastapi-react`)
* Pull Requests with code reviews
* Clean separation between:

  * Quant logic
  * API layer
  * UI layer

---

## 🧩 Future Enhancements

### 🔮 Backend

* PostgreSQL integration
* Multi-asset portfolios
* User authentication
* Async backtests
* Caching (Redis)

### 📊 Frontend

* Interactive charts (Recharts / Plotly)
* Portfolio dashboards
* CSV download button
* Strategy parameter controls

### 📈 Quant Models

* Risk parity
* CVaR optimization
* Black–Litterman
* Reinforcement learning allocation

---

## 🤝 Contributions

Contributions are welcome!

1. Fork the repo
2. Create a feature branch
3. Commit with clear messages
4. Open a Pull Request with context

---

## 📜 License

MIT License — free to use, modify, and distribute.

---

If you want, next I can:

* ✨ Add **badges** (FastAPI, React, License)
* 📊 Add **architecture diagram**
* 🧪 Add **example API calls**
* 📝 Shorten it for recruiters
* 🧠 Make a **technical deep-dive README**


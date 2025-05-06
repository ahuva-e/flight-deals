# Python Final Project

This project scrapes [The Flight Deal](https://www.theflightdeal.com/) for details of flights, 
and gets weather forecasts from [Weather API](https://www.weatherapi.com/). 

# ✈️ Flight Deals Explorer with ChatGPT

[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](./tests)

This Streamlit application scrapes flight deal data from the web, enriches it with weather forecasts, and includes a chatbot powered by ChatGPT to help users choose a holiday destination. It integrates web scraping, API usage, data visualization with Plotly, and a conversational AI assistant into a single interactive dashboard.

---

## 📦 Project Features

- 🛫 Scrapes real-time flight deals from the web
- 🌤 Shows 7-day weather forecasts at the arrival city
- 📊 Interactive data visualization using Plotly
- 🤖 Includes a holiday recommendation chatbot using Azure OpenAI
- ✅ Full test suite with high coverage using `pytest`

---

## 📋 Project Dependencies


```bash
beautifulsoup4
openai
pandas
pytest
requests
streamlit
```
Dependencies can be downladed by running 
```bash
pip install -r requirements.txt
```
---

## 🛠 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/flight-deals-app.git
cd flight-deals-app
```
### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```
### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install your secrets
Create a .streamlit/secrets.toml file with your API keys:
```bash
OPENAI_API_KEY = "your-azure-openai-api-key"
OPENAI_API_ENDPOINT = "https://your-azure-resource.openai.azure.com"
API_KEY = "your-weatherapi-key"
```

## 🚀 Running the App Locally

```bash
streamlit run streamlit_app.py
```



# ✈️ [Flight Deals Explorer with AI Chatbot](https://flightdeals.streamlit.app)
## Python Final Project - Ahuva Ebert
This project scrapes [The Flight Deal](https://www.theflightdeal.com/) for details of flights, 
and gets weather forecasts from [Weather API](https://www.weatherapi.com/). 

[![Tests](https://github.com/ahuva-e/flight-deals/actions/workflows/python-tests.yml/badge.svg)](https://github.com/ahuva-e/flight-deals/actions/workflows/python-tests.yml)


This Streamlit application scrapes flight deal data from the web, enriches it with weather forecasts, and includes a chatbot powered by Azure OpenAI to help users choose a holiday destination. It integrates web scraping, API usage, data visualization with Plotly, and a conversational AI assistant into a single interactive dashboard.

---

## 📦 Project Features

- 🛫 Scrapes real-time flight deals from the web
- 🌤 Shows 7-day weather forecasts at the arrival city
- 📊 Interactive data visualization using Plotly
- 🤖 Includes a holiday recommendation chatbot using Azure OpenAI
- ✅ Full test suite with high coverage using `pytest`

---

## 🧠 How AI is Integrated and Used

This app uses Azure OpenAI's `gpt-35-turbo-16k` model through the openai Python SDK:

- When a user types in a message, it sends the conversation history to OpenAI.

- The model streams a response back, displayed in the chatbot tab.

- The assistant helps users pick destinations, based on preferences or inspiration.

You can find the integration in `chatbot.py`, inside the `chat()` function.

---

## 📋 Project Dependencies

`beautifulsoup4`  - Parses HTML received by web scraper

`openai` - Allows interaction with AI models

`pandas` - Data analysis and manipulation

`plotly` - Interactive, user-friendly graphs

`pytest` - Simple testing framework for Python

`requests` - Handles HTTP requests for web scraping

`streamlit` - Web framework for Python apps

```bash
beautifulsoup4
openai
pandas
plotly
pytest
requests
streamlit
```
Dependencies can be downloaded by running:
```bash
pip install -r requirements.txt
```
---

## ⚒️ Setup Instructions

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

### 🚀 Running the App Locally

```bash
streamlit run streamlit_app.py
```

### ✅ Run tests with coverage report

```bash
pytest --cov
```

## 🌐 Deployment

The streamlit app has been deployed to the cloud and is available at 
[flightdeals.streamlit.app](https://flightdeals.streamlit.app)

You can also deploy the app yourself using:

• Streamlit Community Cloud
1. Fork this repository
1. Go to [share.streamlit.io/deploy](https://share.streamlit.io/deploy)
1. Connect your repo, set the main file as streamlit_app.py
1. Add secrets via the UI

## 📄 License
This project is licensed under the MIT License.
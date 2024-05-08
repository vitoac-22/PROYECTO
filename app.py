# Importar librerías necesarias
import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import API.datos_empresa as datos

# Título de la aplicación
st.title("Análisis Financiero Interactivo de Stocks")

# Selección de la acción a analizar
stock_symbol = st.sidebar.selectbox("Símbolo del Stock", options=datos.datos_empresa())

# Selección del periodo de tiempo
periodo = st.sidebar.selectbox(
    "Periodo de tiempo", options=["1mo", "3mo", "6mo", "1y", "2y"], index=4
)

# Obtener datos históricos
data = yf.Ticker(stock_symbol)
hist = data.history(period=periodo)

# Calcular cambios de precio y RSI
hist["Price Change"] = hist["Close"].diff()
hist["Gain"] = hist["Price Change"].apply(lambda x: x if x > 0 else 0)
hist["Loss"] = hist["Price Change"].apply(lambda x: abs(x) if x < 0 else 0)

rolling_period = 14
hist["Avg Gain"] = hist["Gain"].rolling(window=rolling_period).mean()
hist["Avg Loss"] = hist["Loss"].rolling(window=rolling_period).mean()
hist["RS"] = hist["Avg Gain"] / hist["Avg Loss"]
hist["RSI"] = 100 - (100 / (1 + hist["RS"]))

# Mostrar gráficos RSI y Precios de Cierre
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(hist.index, hist["Close"], color="blue", label="Precio de cierre")
sobrecompra = hist[hist["RSI"] > 70]
sobreventa = hist[hist["RSI"] < 30]
ax.scatter(sobrecompra.index, sobrecompra["Close"], color="red", label="Sobrecompra")
ax.scatter(sobreventa.index, sobreventa["Close"], color="orange", label="Sobreventa")
ax.set_title(f"RSI y Precio de Cierre {stock_symbol}")
ax.set_xlabel("Fecha")
ax.set_ylabel("Precio de cierre")
ax.legend()
st.pyplot(fig)

# Calculo de MACD
short_ema = hist["Close"].ewm(span=12, adjust=False).mean()
long_ema = hist["Close"].ewm(span=26, adjust=False).mean()
macd_line = short_ema - long_ema
signal_line = macd_line.ewm(span=9, adjust=False).mean()
macd_histogram = macd_line - signal_line

# Mostrar gráfico MACD
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(hist.index, macd_line, color="green", label="MACD")
ax.plot(hist.index, signal_line, color="orange", label="Signal Line")
ax.set_title(f"MACD y Línea de Señal {stock_symbol}")
ax.set_xlabel("Fecha")
ax.set_ylabel("Valor")
ax.legend()
st.pyplot(fig)

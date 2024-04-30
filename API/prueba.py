# Importar librerías
import pandas as pd
import yfinance as yf
import os

# Un valor de RSI por encima de 70 generalmente se considera sobrecomprado,
# mientras que un valor por debajo de 30 se considera sobrevendido.


# Obtener datos históricos
# Prueba con 'MSFT'
msft = yf.Ticker("MSFT")
hist = msft.history(period="24mo")

# Calcular cambios de precio
hist["Price Change"] = hist["Close"].diff()

# Separar cambios de precio en incrementos y decrementos
hist["Gain"] = hist["Price Change"].apply(lambda x: x if x > 0 else 0)
hist["Loss"] = hist["Price Change"].apply(lambda x: abs(x) if x < 0 else 0)

# Calcular promedio de incrementos y decrementos (usando un período de 14 días)
periodo = 14
hist["Avg Gain"] = hist["Gain"].rolling(window=periodo).mean()
hist["Avg Loss"] = hist["Loss"].rolling(window=periodo).mean()

# Calcular relación de fuerza (RS)
hist["RS"] = hist["Avg Gain"] / hist["Avg Loss"]

# Calcular RSI
hist["RSI"] = 100 - (100 / (1 + hist["RS"]))

# Imprimir DataFrame con RSI calculado
# print(hist[["Close", "RSI"]])

##############################
import matplotlib.pyplot as plt

# Crear una figura y ejes
fig, ax = plt.subplots(figsize=(10, 6))

# Graficar los precios de cierre
ax.plot(hist.index, hist["Close"], color="blue", label="Precio de cierre")

# Identificar sobrecompra y sobreventa
sobrecompra = hist[hist["RSI"] > 70]
sobreventa = hist[hist["RSI"] < 30]

# Graficar sobrecompra y sobreventa en rojo
ax.scatter(sobrecompra.index, sobrecompra["Close"], color="red", label="Sobrecompra")
ax.scatter(sobreventa.index, sobreventa["Close"], color="orange", label="Sobreventa")

# Configurar etiquetas y leyenda
ax.set_title("Anomalías de RSI")
ax.set_xlabel("Fecha")
ax.set_ylabel("Precio de cierre")
ax.legend()

# Mostrar la gráfica
plt.show()

####################################33

# Calcular la EMA de corto plazo (generalmente 12 períodos)
short_ema = hist["Close"].ewm(span=12, adjust=False).mean()

# Calcular la EMA de largo plazo (generalmente 26 períodos)
long_ema = hist["Close"].ewm(span=26, adjust=False).mean()

# Calcular la línea MACD
macd_line = short_ema - long_ema

# Calcular la línea de señal (signal line)
signal_line = macd_line.ewm(span=9, adjust=False).mean()

# Calcular el histograma MACD
macd_histogram = macd_line - signal_line

# Imprimir DataFrame con MACD, línea de señal y histograma MACD
print(
    pd.DataFrame(
        {
            "MACD": macd_line,
            "Signal Line": signal_line,
            "MACD Histogram": macd_histogram,
        }
    )
)


#######################################

import matplotlib.pyplot as plt

# Crear una figura y ejes
fig, ax = plt.subplots(figsize=(10, 6))

# Graficar el MACD y la línea de señal
ax.plot(hist.index, macd_line, color="green", label="MACD")
ax.plot(hist.index, signal_line, color="orange", label="Signal Line")

# Configurar etiquetas y leyenda
ax.set_title("MACD y Línea de Señal")
ax.set_xlabel("Fecha")
ax.set_ylabel("Precio de cierre")
ax.legend()

# Mostrar la gráfica
plt.show()

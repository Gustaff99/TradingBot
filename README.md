# TradingBot 🤖 🇬🇧

## Description 📝
TradingBot is an algorithmic trading bot designed to operate in the cryptocurrency market, specifically with Bitcoin. It uses a combination of technical indicators to make buy and sell decisions in a simulated backtesting environment.

## Trading Strategy 📊
The strategy implemented in TradingBot includes the following technical indicators:
- **RSI (Relative Strength Index)**: Used to measure the speed and change of price movements.
- **MACD (Moving Average Convergence Divergence)**: This indicator helps identify changes in strength, direction, momentum, and duration of a trend in the price of an asset.
- **ADX (Average Directional Index)**: Measures the strength of a trend.
- **ATR (Average True Range)**: Provides information on market volatility.
- **Ichimoku Cloud**: Offers a comprehensive view of future price and market action through various components that provide support and resistance levels as well as momentum and trend insights.

The strategy combines signals from these indicators to determine optimal entry and exit points, using a dynamic stop-loss based on the ATR to manage risk.

## Installation 🛠️
To run TradingBot, you will need Python and several specialized libraries.

### Prerequisites
- Python 3.8 or higher
- Pandas
- NumPy
- TA-Lib
- backtesting.py

You can install all the necessary dependencies with pip, using the following command:

```bash
pip install pandas numpy backtesting talib
```

### TA-Lib Installation
The installation of TA-Lib can vary depending on your operating system. Consult [TA-Lib](https://github.com/TA-Lib/ta-lib-python) for specific instructions for your system.

## Usage 🚀
To run the backtest with TradingBot, follow these steps:

1. Place the `DatosBTC.csv` data file on your desktop or update the path in the script.
2. Run the script from the terminal:

```bash
python TradingBot.py
```

The script will automatically perform the backtesting of the strategy with the provided data and display the results in charts and performance summaries.

## Contributing 🤝
If you wish to contribute to the project, please consider cloning the repository, creating a feature branch, and submitting your pull requests for review.

# TradingBot 🤖 🇪🇸

## Descripción 📝
TradingBot es un bot de trading algorítmico diseñado para operar en el mercado de criptomonedas, específicamente con Bitcoin. Utiliza una combinación de indicadores técnicos para tomar decisiones de compra y venta en un entorno simulado de backtesting.

## Estrategia de Trading 📊
La estrategia implementada en TradingBot incluye los siguientes indicadores técnicos:
- **RSI (Relative Strength Index)**: Se utiliza para medir la velocidad y cambio de los movimientos de precios.
- **MACD (Moving Average Convergence Divergence)**: Este indicador ayuda a identificar cambios en la fuerza, dirección, momentum y duración de una tendencia en el precio de un activo.
- **ADX (Average Directional Index)**: Mide la fuerza de una tendencia.
- **ATR (Average True Range)**: Proporciona información sobre la volatilidad del mercado.
- **Ichimoku Cloud**: Ofrece una visión integral del precio y la acción del mercado futuro a través de varios componentes que proporcionan niveles de soporte y resistencia así como insights de momentum y tendencia.

La estrategia combina señales de estos indicadores para determinar puntos óptimos de entrada y salida, utilizando un stop-loss dinámico basado en el ATR para gestionar el riesgo.

## Instalación 🛠️
Para ejecutar TradingBot, necesitarás Python y varias bibliotecas especializadas.

### Prerrequisitos
- Python 3.8 o superior
- Pandas
- NumPy
- TA-Lib
- backtesting.py

Puedes instalar todas las dependencias necesarias con pip, utilizando el siguiente comando:

```bash
pip install pandas numpy backtesting talib
```

### Instalación de TA-Lib
La instalación de TA-Lib puede variar según tu sistema operativo. Consulta [TA-Lib](https://github.com/TA-Lib/ta-lib-python) para obtener instrucciones específicas para tu sistema.

## Uso 🚀
Para ejecutar el backtest con TradingBot, sigue estos pasos:

1. Coloca el archivo de datos `DatosBTC.csv` en tu escritorio o actualiza la ruta en el script.
2. Ejecuta el script desde la terminal:

```bash
python TradingBot.py
```

El script ejecutará automáticamente el backtesting de la estrategia con los datos proporcionados y mostrará los resultados en gráficos y resúmenes de desempeño.

## Contribuir 🤝
Si deseas contribuir al proyecto, por favor considera clonar el repositorio, crear una rama de característica y someter tus pull requests para revisión.

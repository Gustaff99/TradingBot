from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import talib
import pandas as pd
import numpy as np

def cargar_y_preparar_datos(filepath):
    btc = pd.read_csv(filepath, sep=";", decimal=".")
    btc = btc.interpolate(limit_direction='both')
    btc["Date"] = pd.to_datetime(btc["Unix"], unit="s")
    btc = btc.set_index('Date')
    btc['Volume'] = btc['Volume'].replace(r'\.', '', regex=True).astype(float)
    return btc

def seleccionar_datos(btc, inicio, fin):
    btc = btc[inicio:fin]
    btc = btc.resample("1D").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum"
    })
    return btc

def ajustar_precios(btc, factor=10000):
    for col in ["Open", "High", "Low", "Close"]:
        btc[col] /= factor
    return btc

def ichimoku_cloud(high, low, close):
    # Asegúrate de que high, low, y close son Series de pandas
    high = pd.Series(high)
    low = pd.Series(low)
    close = pd.Series(close)

    tenkan_sen = (high.rolling(window=9).max() + low.rolling(window=9).min()) / 2
    kijun_sen = (high.rolling(window=26).max() + low.rolling(window=26).min()) / 2
    senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(26)
    senkou_span_b = ((high.rolling(window=52).max() + low.rolling(window=52).min()) / 2).shift(26)
    chikou_span = close.shift(-26)

    return tenkan_sen, kijun_sen, senkou_span_a, senkou_span_b, chikou_span

class ProfessionalStrategy(Strategy):
    # Definición de parámetros como variables de clase
    tiempo_rsi = 14
    macd_fast = 12
    macd_slow = 26
    macd_signal = 9
    stoch_k = 14
    stoch_d = 3
    atr_period = 14

    def init(self):
        # Indicadores
        self.rsi = self.I(talib.RSI, self.data.Close, self.tiempo_rsi)
        self.macd, self.signal, _ = self.I(talib.MACD, self.data.Close, self.macd_fast, self.macd_slow, self.macd_signal)
        self.adx = self.I(talib.ADX, self.data.High, self.data.Low, self.data.Close, 14)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, self.atr_period)
        # Calcular Ichimoku Cloud externamente
        ichimoku_results = ichimoku_cloud(self.data.High, self.data.Low, self.data.Close)
        self.tenkan_sen = self.I(lambda x: x, ichimoku_results[0])
        self.kijun_sen = self.I(lambda x: x, ichimoku_results[1])
        self.senkou_span_a = self.I(lambda x: x, ichimoku_results[2])
        self.senkou_span_b = self.I(lambda x: x, ichimoku_results[3])
        self.chikou_span = self.I(lambda x: x, ichimoku_results[4])

    def next(self):
        if not self.position:
            if (self.rsi[-1] > 50 and crossover(self.macd, self.signal) and
                self.data.Close[-1] > self.senkou_span_a[-1] and
                self.data.Close[-1] > self.senkou_span_b[-1]):
                sl = self.data.Close[-1] - 2 * self.atr[-1]
                self.buy(sl=sl)
        else:
            if (crossover(self.signal, self.macd) or
                self.data.Close[-1] < self.senkou_span_a[-1] or
                self.data.Close[-1] < self.senkou_span_b[-1]):
                self.position.close()


def ejecutar_backtest(btc, autoajustar):
    bt = Backtest(btc, ProfessionalStrategy, cash=10000, commission=0.001)
    if autoajustar:
        # Asegúrate de definir rangos para al menos algunos parámetros de tu estrategia
        result = bt.optimize(
            tiempo_rsi=range(10, 20, 2),
            macd_fast=range(5, 15, 2),
            macd_slow=range(20, 40, 2),
            macd_signal=range(5, 15, 2),
            stoch_k=range(10, 20, 2),
            stoch_d=range(2, 10, 2),
            atr_period=range(10, 20, 2),
            maximize='Equity Final [$]'
        )
        print("Mejores parámetros:")
        print(result._strategy._params)
        print("Mejores estadísticas de rendimiento:")
        print(result)
        bt.plot()
    else:
        result = bt.run()
        print(result)
        bt.plot()

if __name__ == "__main__":
    filepath = r'C:\Users\Gus\Desktop\Proyectos\Trading Bot\DatosBTC.csv'
    btc = cargar_y_preparar_datos(filepath)
    btc = seleccionar_datos(btc, 1000, 1000000)
    btc = ajustar_precios(btc)
    ejecutar_backtest(btc, True)

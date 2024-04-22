from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import talib
import pandas as pd

# Carga y preparación del dataset
def cargar_y_preparar_datos(filepath):
    btc = pd.read_csv(filepath, sep=";", decimal=".")
    btc = btc.interpolate(limit_direction='both')
    btc["Date"] = pd.to_datetime(btc["Unix"], unit="s")
    btc = btc.set_index('Date')
    btc['Volume'] = btc['Volume'].replace(r'\.', '', regex=True).astype(float)
    return btc

# Selección de una porción del dataset
def seleccionar_datos(btc, inicio, fin):
    btc = btc[inicio:fin]
    btc = btc.resample("60T").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum"
    })
    return btc

# Ajustar los precios para la simulación
def ajustar_precios(btc, factor=10000):
    for col in ["Open", "High", "Low", "Close"]:
        btc[col] /= factor
    return btc

# Estrategia de trading basada en RSI, EMA y Volumen
class RsiConEma(Strategy):
    # Definición de parámetros como variables de clase
    rangosuperior = 70
    rangoinferior = 30
    tiempo_rsi = 14
    EMA = 200
    EMAcorta = 50
    volumen_minimo = 100000

    def init(self):
        self.rsi = self.I(talib.RSI, self.data.Close, self.tiempo_rsi)
        self.ema = self.I(talib.EMA, self.data.Close, self.EMA)
        self.emacorta = self.I(talib.EMA, self.data.Close, self.EMAcorta)

    def next(self):
        if self.data.Volume[-1] < self.volumen_minimo:
            return

        if self.position.pl_pct < -0.01:
            self.position.close()

        if self.position.is_short and self.position.pl_pct > 0.015 and crossover(self.rsi, self.rangoinferior + 10):
            self.position.close()

        if self.position.is_long and self.position.pl_pct > 0.02 and crossover(self.rangosuperior - 20, self.rsi):
            self.position.close()

        if crossover(self.rangosuperior, self.rsi):
            if self.position.is_long:
                self.position.close()
            if self.ema > self.data.Close[-1] and not self.position:
                self.sell()

        elif crossover(self.rsi, self.rangoinferior):
            if self.position.is_short:
                self.position.close()
            if self.ema < self.data.Close[-1] and not self.position:
                self.buy()

# Configuración del Backtest y salida de parámetros óptimos
def ejecutar_backtest(btc, autoajustar):
    bt = Backtest(btc, RsiConEma, cash=10000, commission=0.001)
    if autoajustar:
        stats, param = bt.optimize(
            rangosuperior=range(65, 80, 5),
            rangoinferior=range(25, 40, 5),
            tiempo_rsi=range(12, 20, 2),
            EMA=range(100, 200, 25),
            EMAcorta=range(20, 60, 10),
            volumen_minimo=range(50000, 150000, 25000),
            maximize='Equity Final [$]',
            return_heatmap=True)
        print("Mejores parámetros:", param)
        print(stats)
    else:
        stats = bt.run()
        print(stats)
    bt.plot()

# Principal
filepath = r'C:\Users\Gus\Desktop\Proyectos\Trading Bot\DatosBTC.csv'
btc = cargar_y_preparar_datos(filepath)
btc = seleccionar_datos(btc, 10000, 300000)
btc = ajustar_precios(btc)
autoajustar = True  # Cambiar a False para ejecutar sin optimización
ejecutar_backtest(btc, autoajustar)

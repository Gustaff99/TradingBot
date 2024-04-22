import pandas as pd

# Cambia 'filepath' por la ruta de tu archivo CSV
filepath = 'C:\\Users\\Gus\\Desktop\\Proyectos\\Trading Bot\\bitstampUSD_1-min_data_2012-01-01_to_2021-03-31.csv'
btc = pd.read_csv(filepath, sep=';')

# Limpia y prepara los datos
btc['Date'] = pd.to_datetime(btc['Date'])
btc['Volume'] = btc['Volume'].replace(r'\.', '', regex=True).astype(float)
btc = btc.interpolate(limit_direction='both')

# Asegúrate de que los nombres de las columnas coincidan
btc.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
btc.set_index('Date', inplace=True)

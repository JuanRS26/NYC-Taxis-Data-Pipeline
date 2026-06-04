import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_TRIP_DIR = BASE_DIR / 'data' / 'raw' / 'trip'
CLEAN_DIR = BASE_DIR / 'data' / 'clean'


# ------------------------
# DATAFAMES INFORMATION
# ------------------------


# La siguiente lista contiene los nombres de los DataFrames que existen.
list_names_df = ['yellow_tripdata_2024-01.parquet', 'yellow_tripdata_2024-02.parquet', 
                'yellow_tripdata_2024-03.parquet', 'yellow_tripdata_2024-04.parquet',
                'yellow_tripdata_2024-05.parquet', 'yellow_tripdata_2024-06.parquet', 
                'yellow_tripdata_2024-07.parquet', 'yellow_tripdata_2024-08.parquet', 
                'yellow_tripdata_2024-09.parquet', 'yellow_tripdata_2024-10.parquet', 
                'yellow_tripdata_2024-11.parquet', 'yellow_tripdata_2024-12.parquet', 
                'yellow_tripdata_2025-01.parquet', 'yellow_tripdata_2025-02.parquet', 
                'yellow_tripdata_2025-03.parquet', 'yellow_tripdata_2025-04.parquet', 
                'yellow_tripdata_2025-05.parquet', 'yellow_tripdata_2025-06.parquet', 
                'yellow_tripdata_2025-07.parquet', 'yellow_tripdata_2025-08.parquet', 
                'yellow_tripdata_2025-09.parquet', 'yellow_tripdata_2025-10.parquet', 
                'yellow_tripdata_2025-11.parquet']

# La siguiente lista contiene los nombres de las columnas que existen en los DataFrames.
list_columns = ['VendorID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime', 'passenger_count',
                'trip_distance', 'RatecodeID', 'store_and_fwd_flag', 'PULocationID', 'DOLocationID',
                'payment_type', 'fare_amount', 'extra','mta_tax', 'tip_amount', 'tolls_amount',
                'improvement_surcharge', 'total_amount', 'congestion_surcharge', 'Airport_fee']

column_2025 = 'cbd_congestion_fee'

dates = ['2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01', '2024-05-01', '2024-06-01',
         '2024-07-01', '2024-08-01', '2024-09-01', '2024-10-01', '2024-11-01', '2024-12-01',
         '2025-01-01', '2025-02-01', '2025-03-01', '2025-04-01', '2025-05-01', '2025-06-01', 
         '2025-07-01', '2025-08-01', '2025-09-01', '2025-10-01', '2025-11-01', '2025-12-01']


# ------------------------ 
# CLEANING
# ------------------------


# La siguente funcion remplaza los valores nulos por valores especificos dependiendo de cada columna.
def replace_values_nan():
    
    for name_df in list_names_df:  # este ciclo itera todos los DataFrames que hay.
        
        df = pd.read_parquet(RAW_TRIP_DIR / name_df)    # se lee el DataFrame

        values = {'passenger_count': 0,
                  'RatecodeID': 99, 
                  'store_and_fwd_flag': 'N', 
                  'congestion_surcharge': 0, 
                  'Airport_fee': 0}

        df.fillna(value = values, inplace = True)


# La siguiente funcion transforma el tipo de dato de las columnas
def transform_types():

    for name_df in list_names_df:
        
        df = pd.read_parquet(RAW_TRIP_DIR / name_df)

        df['VendorID'] = df['VendorID'].astype('int32')


def dates_corrections(df, name, position):

    datetime_columns = ['tpep_pickup_datetime', 'tpep_dropoff_datetime']
    
    for column in datetime_columns:

        total_values = df[column].count()

        if column == 'tpep_pickup_datetime':
            df = df[(df[column] >= dates[position]) & (df[column] < dates[position+1])]
        else:
            df = df[df[column] >= dates[0]]
        
        correct_values = df[column].count()
        deleted_values = total_values - correct_values
        
    print('Valores de fechas corregidos...')

    return df


'''
La siguiente funcion corrige los valores negativos que existan para las columnas:

    - fare_amount
    - extra
    - mta_tax
    - tip_amount
    - tolls_amount
    - improvement_surcharge
    - total_amount
    - congestion_surcharge
    - Airport_fee
    - cbd_congestion_fee
'''

def negative_values_correction(df, name, flag = False):

    # Se utiliza la funcino abs() para convertir los valores negativos a absolutos y asi corregirlos.
    df['fare_amount'] = df['fare_amount'].abs()
    df['extra'] = df['extra'].abs()
    df['mta_tax'] = df['mta_tax'].abs()
    df['tip_amount'] = df['tip_amount'].abs()
    df['tolls_amount'] = df['tolls_amount'].abs()
    df['improvement_surcharge'] = df['improvement_surcharge'].abs()
    df['total_amount'] = df['total_amount'].abs()
    df['congestion_surcharge'] = df['congestion_surcharge'].abs()
    df['Airport_fee'] = df['Airport_fee'].abs()

    if flag == True:
        df[column_2025] = df[column_2025].abs() # Esta columna solo se encuentra en los Datasets del año 2025.

    print('Valores negativos corregidos...')

    return df


'''
La funcion main() sera la encargada de ejecutar todas las funciones de limpieza para cada dataset.
'''

def main():

    # El ciclo for funciona para cargar cada DataFrame.
    for i, name_df in enumerate(list_names_df):
        
        df = pd.read_parquet(RAW_TRIP_DIR / name_df) # se lee el DataFrame
        
        print(f'\n----------------------------  {name_df}  ------------------------------------\n')
        # Se genera un condicional ya que hay una columna extra en los datasets del año 2025.
        if i >= 12: 
            # Se envia el flag como True para que se corrija la columna extra.
            df = negative_values_correction(df, name_df, flag = True) 
        else:
            df = negative_values_correction(df, name_df)

        df = dates_corrections(df, name_df, i)
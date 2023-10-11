# Importar Módulos necesarios
from google.cloud import storage
from google.cloud import secretmanager

import wbgapi as wb
import pandas as pd
import numpy as np
import time

# Crear df desde API Banco Mundial

def get_indicators(data, context):
            
    # client creation
    storage_client = storage.Client()
    secrets_client = secretmanager.SecretManagerServiceClient()


    countries_list = ['CHN', 'RUS', 'PHL', 'IND', 'KOR', 'ZAF', 
                    'ARG', 'AUS', 'BRA', 'BOL', 'CHL', 'VEN',
                    'ECU', 'MEX', 'PER', 'SLV', 'URY', 'PRY',
                    'ESP', 'SWE', 'CHE', 'GBR', 'PRT', 'JPN', 
                    'ITA', 'DEU', 'FRA', 'NOR', 'LUX',
                    'CAN', 'COL', 'USA', 'EGY'
                    ]
    
    indicators =  {
                'SP.DYN.LE00.FE.IN': 'Life expectancy at birth, female (years)',
                'SP.DYN.LE00.IN': 'Life expectancy at birth, total (years)',
                'SP.DYN.LE00.MA.IN': 'Life expectancy at birth, male (years)',
                'SP.URB.TOTL.IN.ZS': 'Urban population (% of total population)',
                'SP.RUR.TOTL.ZS': 'Rural population (% of total population)',
                'SP.POP.GROW':'Population growth (annual %)',
                'FP.CPI.TOTL.ZG': 'Inflation, consumer prices (annual %)',
                'NY.GDP.DEFL.KD.ZG': 'Inflation, GDP deflator (annual %)',
                'NY.GDP.MKTP.CD': 'GDP (current US$)',
                'NY.GDP.PCAP.CD': 'GDP per capita (current US$)',
                'NY.GDP.PCAP.KD.ZG': 'GDP per capita growth (annual %)',
                'NY.GNP.MKTP.CD': 'GNI (current US$)',
                'MS.MIL.XPND.GD.ZS': 'Military expenditure (% of GDP)',
                'NE.CON.GOVT.CD':'General government final consumption expenditure (current US$)',
                'TX.VAL.FOOD.ZS.UN':'Food exports (% of merchandise exports)',
                'AG.PRD.FOOD.XD':'Food production index (2014-2016 = 100)',
                'NE.CON.PRVT.ZS': 'Households and NPISHs final consumption expenditure (% of GDP)',
                'SP.DYN.AMRT.FE': 'Mortality rate, adult, female (per 1,000 female adults)',
                'SP.DYN.AMRT.MA': 'Mortality rate, adult, male (per 1,000 male adults)',
                'SP.DYN.IMRT.FE.IN': 'Mortality rate, infant, female (per 1,000 live births)',
                'SP.DYN.IMRT.IN': 'Mortality rate, infant (per 1,000 live births)',
                'SP.DYN.IMRT.MA.IN': 'Mortality rate, infant, male (per 1,000 live births',
                'SP.DYN.CBRT.IN': 'Birth rate, crude (per 1,000 people)',
                'NY.GDY.TOTL.KN': 'Gross domestic income (constant LCU)',
                
                }

    indicator25 = {
            'SL.EMP.MPYR.FE.ZS': 'Employers, female (% of female employment) (modeled ILO estimate)',
            'SL.EMP.MPYR.MA.ZS': 'Employers, male (% of male employment) (modeled ILO estimate)',
            'SL.EMP.MPYR.ZS': 'Employers, total (% of total employment) (modeled ILO estimate)',
            'SL.EMP.OWAC.ZS': 'Own-account workers, total (% of male employment) (modeled ILO estimate)',
            'SL.EMP.SELF.ZS': 'Self-employed, total (% of total employment) (modeled ILO estimate)',
            'SL.EMP.TOTL': 'Total employment, total (ages 15+)',
    }

    def crerate_df_bm(indicators, countries, db=2):
        '''
        Construir Data Frame con información del World Bank.
    
            Args:
                indicators: Lista de diccionarios con los códigos y nombres de indicadores
                countries: Lista con los códigos de los paises según ISO 3166-1
                db: Código base de datos a rastrear por defecto db=2
            
            Returns:
                Data Frame 
        '''
        
        # Crear array vacio
        data = np.array([])
        # Buscar a través de la lista de indicadores y obtener los datos
        for i in indicators.items():
            trans_data = wb.data.fetch(i[0], countries, db=db)
            time.sleep(1)  # Esperar 1 segundo (pausa)
            list_countries = []
            list_years = []
            list_data = []
            # Se agregan los valores obtenidos a cada lista auxiliar y se crea diccionario con estas
            for x in trans_data:
                list_countries.append(x['economy'])
                list_years.append((x['time'][2::]))
                list_data.append((x['value']))
            data_dict = {'name':i[1],
                    'country':list_countries,
                    'year':list_years,
                    'value':list_data
                    }
            # Se Agregan data_dict al array data
            data = np.append(data, data_dict)
            
        # Construcción del data frame    
        df = pd.DataFrame()
        df['country'] = data[0]['country'] 
        df['year'] = data[0]['year'] 
        for i in range(0,len(data)):
            df[data[i]['name']] = data[i]['value']
            
        return df
    
    # Crear listado de Países (economy) que se encuentran en la Base de Datos
    countries = wb.economy.list()
    countries_df = pd.DataFrame(countries)
    # Generar Data Frame de los 34 paises a estudiar
    countries_df = countries_df[countries_df['id'].isin(countries_list)][['id', 'value', 'longitude', 'latitude', 'region', 'lendingType', 'incomeLevel']]
    countries = countries_df['id'].tolist()

    # Obtener datos de API en dos bases de datos
    df = crerate_df_bm(indicators, countries)
    # Cambiar tipo de datos de columna "year"
    # df['year'] = df['year'].astype('int')
    # Eliminar filas donde el año (year) sea anterior a 1990
    # df.drop(df[(df['year'] <= 1980)].index, inplace=True)

    df2 = crerate_df_bm(indicator25, countries, db=25)
    # Cambiar tipo de datos de columna "year"
    # df2['year'] = df2['year'].astype('int')
    # Eliminar filas donde el año (year) sea anterior a 1990
    # df2.drop(df2[(df2['year'] <= 1980)].index, inplace=True)

    # Unir los dos dataframes
    new_df = df.merge(df2, how='left', on=['country', 'year'])

    # Almacenar datos en Bucket
    bucket = storage_client.get_bucket('pf_digital_code_storage')

    # Crear un nombre único para el archivo usando epoch unix timestamp
    # blob = bucket.blob(f'{int(time.time())}_indicators.csv')
    blob = bucket.blob('indicators.csv')
    # Agregar los datos a cloud storage como archivo csv
    blob.upload_from_string(new_df.to_csv(index=False, header=True), 'text/csv')

    messaje = 'Archivo indicators_wb.csv cargado con éxito en el bucket pf_digital_code_storage '
    return messaje

        
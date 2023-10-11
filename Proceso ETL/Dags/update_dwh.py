import pandas as pd
import requests,os
from airflow.models import DAG
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
from airflow.operators.email_operator import EmailOperator


# Constantes
BUCKET_NAME = 'pf_digital_code_storage'
DEFAULT_ARGS = {
    'owner': 'carlos_villarreal',
}

# Variables con path en google cloud storage
data_path = 'gs://pf_digital_code_storage/indicators.csv'
data_output_path = 'gs://pf_digital_code_storage/transform_data.csv'
countries_path = 'gs://pf_digital_code_storage/contries_EVN_Final(2).csv'
countries_output_path = 'gs://pf_digital_code_storage/transform_contries.csv'
region_path = 'gs://pf_digital_code_storage/region.csv'

def transform_data(data_path, data_output_path):

    # crear DataFrame desde archivo csv
    df = pd.read_csv(data_path)

    # Validar datos
    data_type = {
        'country':'object', 
        'year': 'int64',
        'Life expectancy at birth, female (years)': 'float64',
        'Life expectancy at birth, total (years)': 'float64',
        'Life expectancy at birth, male (years)': 'float64',
        'Urban population (% of total population)': 'float64',
        'Rural population (% of total population)': 'float64',
        'Population growth (annual %)': 'float64',
        'Inflation, consumer prices (annual %)': 'float64',
        'Inflation, GDP deflator (annual %)': 'float64',
        'GDP (current US$)': 'float64',
        'GDP per capita (current US$)': 'float64',
        'GDP per capita growth (annual %)': 'float64',
        'GNI (current US$)': 'float64',
        'Military expenditure (% of GDP)': 'float64',
        'General government final consumption expenditure (current US$)': 'float64',
        'Food exports (% of merchandise exports)': 'float64',
        'Food production index (2014-2016 = 100)': 'float64',
        'Households and NPISHs final consumption expenditure (% of GDP)': 'float64',
        'Mortality rate, adult, female (per 1,000 female adults)': 'float64',
        'Mortality rate, adult, male (per 1,000 male adults)': 'float64',
        'Mortality rate, infant, female (per 1,000 live births)': 'float64',
        'Mortality rate, infant (per 1,000 live births)': 'float64',
        'Mortality rate, infant, male (per 1,000 live births': 'float64',
        'Birth rate, crude (per 1,000 people)': 'float64',
        'Gross domestic income (constant LCU)': 'float64',
        'Employers, female (% of female employment) (modeled ILO estimate)': 'float64',
        'Employers, male (% of male employment) (modeled ILO estimate)': 'float64',
        'Employers, total (% of total employment) (modeled ILO estimate)': 'float64',
        'Own-account workers, total (% of male employment) (modeled ILO estimate)': 'float64',
        'Self-employed, total (% of total employment) (modeled ILO estimate)': 'float64',
        'Total employment, total (ages 15+)': 'float64'
    }

    column_modi = []
    for col in df.columns.tolist():
        if df[col].dtype != data_type[col]:
            column_modi.append(col)
            df[col] = df[col].astype(data_type[col])
    if len(column_modi) > 0:
        print('COLUMNAS MODIFICADAS:')
        for v in column_modi:
            print(v)

    # Cambiar tipo de datos de columna "year"
    df['year'] = df['year'].astype('int')
    # Eliminar filas donde el año (year) sea anterior a 1990
    df.drop(df[(df['year'] < 1990)].index, inplace=True)

    # Crear y guardar archivo csv de respaldo 
    df.to_csv(data_output_path, encoding='utf-8',index=False)
    print(f"Output to {data_output_path}")

def transform_countries(countries_path, region_path, countries_output_path):

    # crear DataFrame desde archivo csv
    countries = pd.read_csv(countries_path)
    region = pd.read_csv(region_path)

    test_keys = region['region_id'].unique().tolist()
    test_values = region['name'].unique().tolist()
    res = {test_keys[i]: test_values[i] for i in range(len(test_keys))}

    countries = countries.replace({'region': res}, regex=True)

    # Crear y guardar archivo csv de respaldo 
    countries.to_csv(countries_output_path, encoding='utf-8',index=False)
    print(f"Output to {countries_output_path}")


with DAG(
    'PF_Esperanza_de_Vida',
    default_args=DEFAULT_ARGS,
    start_date=days_ago(1),
    schedule_interval='@daily',
    tags=['indicators','workshop']
) as dag:
    dag.doc_md = "Workflow para extraer datos desde Google Store y cargarlos a data big query (datawarehouse)"

    t1 = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        op_kwargs={'data_path': data_path,
                'data_output_path': data_output_path},
    )

    t2 = PythonOperator(
        task_id='transform_countries',
        python_callable=transform_countries,
        op_kwargs={'countries_path': countries_path,
                   'region_path':region_path,
                'countries_output_path': countries_output_path},
    )

    t3 = GoogleCloudStorageToBigQueryOperator(
            task_id='load_indicator_table',
            bucket=BUCKET_NAME,
            source_objects=["transform_data.csv"],
            source_format='CSV',
            destination_project_dataset_table='ordinal-rig-400703.PF_EV_02.fact_indicator',
            skip_leading_rows = 1,
            autodetect=True,
            write_disposition='WRITE_TRUNCATE',
            create_disposition='CREATE_IF_NEEDED',
            allow_jagged_rows=True, # permite valores faltantes
        )
    
    t4 = GoogleCloudStorageToBigQueryOperator(
            task_id='load_countries_table',
            bucket=BUCKET_NAME,
            source_objects=["transform_contries.csv"],
            source_format='CSV',
            destination_project_dataset_table='ordinal-rig-400703.PF_EV_02.dim_countries',
            skip_leading_rows = 1,
            autodetect=True,
            write_disposition='WRITE_TRUNCATE',
            create_disposition='CREATE_IF_NEEDED',
            allow_jagged_rows=True, # permite valores faltantes
        )
    
    # Envío de email a personal autorizado
    t5 = EmailOperator(
        task_id='send_email',
        to=['villarreal.fx@gmail.com', 'Ivonngonzalez824@gmail.com'],
        subject='El Data Werehouse se actualizó',
        html_content='El Data Werehouse se actualizó, por favor revisa tu dashboard. :)'
    )

    t1 >> t3 >> t5
    t2 >> t4 >> t5
import requests
import boto3
import awswrangler as wr
import pandas
from airflow.models import Variable
from datetime import datetime

API_KEY = Variable.get('key')
BASE_URL = "https://api.weatherbit.io/v2.0/current"
city_name = ['Lagos']

payload = {
    'key':API_KEY,
    'city': city_name
}

response = requests.get(BASE_URL, params=payload)

def get_weather_data(response):
    """
    processes the API response, normalizes the data into a DataFrame,
    cleans and transform selected columns and returns the DataFrame.

    Parameters:
        response: The response object returned from the API request.

    Returns:
        df: A DataFrame containing the weather data.
    """
    if response.status_code == 200:
        data = response.json()['data']
        df = pandas.json_normalize(data)
        df['sources'] = df['sources'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
        df = df.rename(columns={
            'weather.icon':'weather_icon',	
            'weather.description':'weather_description',
            'weather.code':'weather_code'
        })

        session = boto3.Session(
            aws_access_key_id=Variable.get('ACCESS_KEY'),
            aws_secret_access_key=Variable.get('SECRET_KEY'),
            region_name='eu-central-1'
        )
        date_str = datetime.today().strftime('%Y-%m-%d')
        path=f's3://current-weather-data/lagos-weather-api/lagos-{date_str}.parquet'

        wr.s3.to_parquet(
            df=df,
            path= path,
            dataset=False,
            boto3_session=session
        )
        return df
    else:
        raise ValueError(f"There is an error, {response.status_code}")


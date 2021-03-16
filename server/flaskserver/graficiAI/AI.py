import datetime

import numpy as np
import pandas as pd
import sklearn as sk
import matplotlib.pyplot as plt
import seaborn as sns

from fbprophet import Prophet
from  flaskserver.config import Config
user_id= 4

def df_extr(percorso):

    df= pd.read_sql_table('user_data', percorso)
    return df

def df_man(df, user_id):
    # queste modifiche per rendere utilizzabili dati che sono sintetici

    df = df[df['user_id']==user_id].reset_index()
    if df is not None:
        df['day'] = pd.DatetimeIndex(df['date']).day
        df['month'] = pd.DatetimeIndex(df['date']).month
        df['year'] = pd.DatetimeIndex(df['date']).year
        da = []
        first = df.iloc[0]['date']
        print(first + datetime.timedelta(days=2))
        for i,val in enumerate(df):
            da.append(first + datetime.timedelta(days=i))
        print("Stampo DA:")
        print(da)
        d = pd.Series(da)
        d = d.rename('date')
        #da = pd.concat([df.year, df.month, d], axis=1)
        #da = pd.to_datetime(da)
        df.date = d
        print(df)
    #df= df[df.user_id == user_id].copy() # !!!
    # non indispensabile
    df.drop(columns='id', inplace=True)
    return df

def pro_1D(df, user_id):
    # formato voluto da fbprophet
    df = df_man(df, user_id)
    periods =4
    values = [df.temp, df.BPM, df.sat]
    label = ['temp', 'BPM', 'sat']
    result = None
    for i,val in enumerate(values):
        data = pd.concat([df.date, val], axis=1)
        data = data.rename(columns={'date': 'ds', label[i]: 'y'})
        if data.shape[0]<2:
            return None
        model = Prophet(interval_width=0.95, daily_seasonality=True, n_changepoints=2)
        model.fit(data)
        future_dates = model.make_future_dataframe(periods=periods, freq='D')
        forecast = model.predict(future_dates)
        print('Sto Stampando:')
        if result is None:
            result = pd.DataFrame(forecast['ds'], columns={'ds':'date'})
            result[label[i]] = forecast['yhat']
            result['user_id'] = np.ones(forecast['ds'].shape[0])*user_id
        else:
            result[label[i]] = forecast['yhat']
    print(result)
    return result.rename(columns={'ds':'date'})
    # forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(16)



def pro_add(df):

    data = pd.concat([df.date, df.temp], axis=1)
    data = data.rename(columns={'date': 'ds', 'temp': 'y'})
    data['add1'] = df.BPM
    data['add2'] = df.sat

    model = Prophet()
    model.add_regressor("add1")
    model.add_regressor("add2")
    future_dates = model.make_future_dataframe(periods=4, freq='D')
    # come gestisco prophet con più dati, più dimensioni

    # formula calcolo punteggio :
    #=forecast[4][]
    #salute= (temp-37)*1.2 + (sat-100)**2
    #if bat>68:
    #    salute= salute+5
    #print(salute)




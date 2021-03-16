import os
import datetime
import numpy as np
import pandas as pd
import sklearn as sk
import matplotlib.pyplot as plt

from bokeh.io import output_notebook, output_file, show, export_png, save
from bokeh.plotting import figure, gmap

from bokeh.embed import components
from bokeh.models import NumeralTickFormatter, ColumnDataSource, HoverTool, TapTool, GMapOptions
from bokeh.models.annotations import Span, BoxAnnotation, Label
from bokeh.layouts import row, column, gridplot
from bokeh.models.widgets import Slider
from bokeh.resources import CDN
from bs4 import BeautifulSoup

from  flaskserver.config import Config

APIKEY= '2379591071'


def df_extr(percorso):

    df= pd.read_sql_table('user_data', percorso)
    return df


def map(df, API):
    # estraggo valori unici dal df (dati utenti)
    # APIKEY

    map_options = GMapOptions(lat=44.5061, lng=11.3663, map_type='roadmap', zoom=8)
    p = gmap(API, map_options, title='MAPPA EMILIA')

    # unico
    data_lat = np.unique(df.gps_lat)
    data_lon = np.unique(df.gps_lon)
    data = pd.concat([data_lat, data_lon], axis=1)

    # data0= ColumnDataSource(df)

    p.circle(x='lon', y='lat', size=11, fill_color='blue', source=data)

    show(p)
    script, div = components(p)

    return script, div


def df_man(df):
    # intervento per modificare i dati del DB

    df['day'] = pd.DatetimeIndex(df['date']).day
    df['month'] = pd.DatetimeIndex(df['date']).month
    df['year'] = pd.DatetimeIndex(df['date']).year
    d = pd.Series(np.arange(1, 22))
    d = d.rename('day')
    da = pd.concat([df.year, df.month, df.day], axis=1)
    da = da.fillna(method='ffill').fillna(method='bfill')
    da = pd.to_datetime(da)
    df.date = da

    return df


def grafbokeh(df, user_id, date):

    df = df_man(df)

    try :
        df = df[df.user_id == user_id]
    except:
        pass
    # da fare un grafico completo
    # poi ripeterlo per i 3 dati, nello stesso blocco
    print(df)
    source = ColumnDataSource(df)
    print(source)
    hover = HoverTool(  # {1}
        tooltips=[
            ('tempe', '$temp'),
            ('data', '@date')
        ]
    )

    # callback=
    # tap= TapTool(callback=callback)

    # plot_options= dict(tools= ['hover, tap, pan, wheel_zoom, reset, box_zoom'], width=600, plot_height=400)
    TOOLS = 'hover, tap, pan, wheel_zoom, reset, box_zoom'
    p1 = figure(x_axis_type='datetime', title='Grafico 1', tools=TOOLS, width=600, plot_height=400)

    p1.circle('date', 'temp', fill_color='red', alpha=0.6, source=source, legend_label='andamento temperatura', size=8)
    p1.line('date', 'temp', line_width=2, source=source)

    # p.xaxis.formatter= NumeralTickFormatter(format='%Y%m%d')
    p1.xaxis.axis_label = 'Giorno'
    # p.yaxis.formatter= NumeralTickFormatter(format='0.0 °C')
    p1.yaxis.axis_label = 'Temperatura'

    line = Span(location=37, dimension='width', line_color='orange', line_width=2)
    p1.add_layout(line)

    line_time = Span(dimension='height', location=date,line_color='green', line_dash='dashed',line_width=2)
    p1.add_layout(line_time)

    box = BoxAnnotation(bottom=37, fill_color='salmon')
    p1.add_layout(box)
    #
    label = Label(x='01/04', y=37, x_offset=12, text='Febbre')
    p1.add_layout(label)

    #box1 = BoxAnnotation(bottom='2021-02-05', fill_color='blue')
    #p1.add_layout(box1)

    l = figure(title='Etichetta', tools=TOOLS, width=600, plot_height=400)
    lab = Label(text='Febbre')
    l.add_layout(lab)

    x = 0.4
    slider = Slider(start=0, end=1, value=x, step=0.1, title='Gravità salute')

    p2 = figure(x_axis_type='datetime', title='Grafico 2', tools=TOOLS, width=600, plot_height=400)
    p2.xaxis.axis_label = 'Giorno'
    p2.yaxis.axis_label = 'Battito'

    source1 = ColumnDataSource(df)
    p2.line('date', 'BPM', line_width=2, source=source1)
    p2.circle('date', 'BPM', fill_color='red', alpha=0.6, source=source1, legend_label='andamento battiti', size=8)

    box2 = BoxAnnotation(bottom=110, fill_color='salmon')
    p2.add_layout(box2)
    line_time1 = Span(dimension='height', location=date, line_color='green', line_dash='dashed', line_width=2)
    p2.add_layout(line_time1)

    source2 = ColumnDataSource(df)
    p3 = figure(x_axis_type='datetime', title='Grafico 3', tools=TOOLS, width=600, plot_height=400)
    p3.xaxis.axis_label = 'Giorno'
    p3.yaxis.axis_label = 'Saturazione'

    p3.line('date', 'sat', line_width=2, source=source2)
    p3.circle('date', 'sat', fill_color='red', alpha=0.6, source=source2,
              legend_label='andamento ossigenazione del sangue', size=8)

    box3 = BoxAnnotation(top=92, fill_color='salmon')
    p3.add_layout(box3)
    line_time2 = Span(dimension='height', location=date, line_color='green', line_dash='dashed', line_width=2)
    p3.add_layout(line_time2)

    # show(p)
    output_file('flaskserver/graficiAI/plots.html')
    gr = [p1,p2,p3]
    names = ['Temperatura', 'BPM', 'Saturazione']
    graphs =[]
    for i,g in enumerate(gr):
        script, div = components(g)
        graphs.append(Graph(script, div, names[i]))

    return graphs


class Graph:

    def __init__(self, script, div, name):
        self.name = name
        self.script = script
        self.div = div


# MOMENTANEO PER LE PROVE
'''if __name__ =='__main__' :
    percorso = Config.SQLALCHEMY_DATABASE_URI
    print(percorso)
    df= df_extr(percorso)
    # script_map, div_map = map(df, APIKEY) # manca la

    user_id = 4
    s= grafbokeh(df, user_id) # da passare quello corretto dal DB
    # script_boh, div_boh= grafbokeh(df, user_id)
    print(s)'''


# A very simple Flask Hello World app for you to get started with...

import pygal

from flask.templating import render_template
from pygal.style import Style
from pygal.style import DefaultStyle, BlueStyle


from flask import Flask, render_template, request,session, jsonify, send_file
from flask_paginate import Pagination, get_page_args
import pandas as pd
import json
import glob
import io
from io import StringIO , BytesIO

files = glob.glob('static\data_cripto\cripto*.csv')

#files = os.listdir("C:\Users\Mercantil\ironhacks\proyecto_final\static\data_cripto")


#Estilos custom
custom_style = DefaultStyle(
title_font_size = 30.0,
legend_font_size = 20.0,
value_font_size = 10.0,
tooltip_font_size = 20.0,
major_label_font_size = 30.0,
label_font_size = 20.0,
value_label_font_size = 20.0)

custom_style2 = BlueStyle(
title_font_size = 30.0,    
legend_font_size = 20.0,
value_font_size = 10.0,
tooltip_font_size = 20.0,
major_label_font_size = 30.0,
label_font_size = 20.0,
value_label_font_size = 20.0)


#df = pd.read_csv(files, sep="|")

df = pd.concat([pd.read_csv(f,header=0, sep="|") for f in files ], ignore_index = True)
df.columns=['username','trade_count','bank_name','location_string','trade_type','temp_price','source','coin','Timestamp']

#crear dataframes filtrados
df["Timestamp"] = df['Timestamp'].astype('datetime64')
binance = df.loc[df['source']=='Binance'].copy()
localbitcoin = df.loc[df['source']=='LocalBitcoin'].copy()
localcryptos = df.loc[df['source']=='localcryptos'].copy()





#preprocesamineto de datos
localbitcoin['bank_name'] = localbitcoin['bank_name'].fillna('OTROS')
localbitcoin.loc[(localbitcoin['bank_name'].str.contains("EXTERIOR"), 'bank_name' )] = 'BANCO EXTERIOR'
localbitcoin.loc[(localbitcoin['bank_name'].str.contains("BANCAMIGA"), 'bank_name'  )] = 'BANCAMIGA'
#localbitcoin.loc[(localbitcoin['bank_name'].str.contains("MÓVIL|Móvil", 'bank_name')  )] = 'PAGOMOVIL'
localbitcoin.loc[(localbitcoin['bank_name'].str.contains("PAGO|Pago|Recarga|RECARGA"), 'bank_name'  )] = 'OTROS'
localbitcoin.loc[(localbitcoin['temp_price'].str.contains("[aA-zZ]",regex=True), 'temp_price'  )] = '0'

#conversion de tipos
localbitcoin["temp_price"] = localbitcoin['temp_price'].astype('float')
#localbitcoin["Timestamp"] = localbitcoin['Timestamp'].astype('datetime64')
#binance["Timestamp"] = localbitcoin['Timestamp'].astype('datetime64')

#asinacion de los datos
data1 = binance.to_dict(orient = 'records')
data2 = localbitcoin.to_dict(orient = 'records')
data3 = localcryptos.to_dict(orient = 'records')


def get_users(offset, per_page, data):

    return data[offset: offset + per_page]


app = Flask(__name__)



@app.route('/')
def index():
    #return render_template('index.html', tables=[binance.to_html(classes='binance')], titles=df.columns.values)
    
    #Paginacion
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = len(data1)
    pagination_users = get_users(0, 20, data1)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')


    date_chart = pygal.Line(x_label_rotation=20, fill=True, interpolate='cubic', style=custom_style)
    date_chart.title = 'Actividad de Mercados P2P'
    anuncios_by_date = df.groupby(pd.Grouper(key='Timestamp',freq='D'))['source'].value_counts()
    date_chart.x_labels = [str(x[0][0])[0:10] for x in anuncios_by_date.items() if x[0][1] == 'LocalBitcoin']
    #[date_chart.add(str(x[0])[:10], x[1]) for x in mean_by_date.items() if x[0] != 'Timestamp']
    date_chart.add('LocalBitcoin',[x[1] for x in anuncios_by_date.items() if x[0][1] == 'LocalBitcoin'  ] )
    date_chart.add('Binance',[x[1] for x in anuncios_by_date.items() if x[0][1] == 'Binance'  ] )
    date_chart.add('localcryptos',[x[1] for x in anuncios_by_date.items() if x[0][1] == 'localcryptos'  ] )
    date_chart=date_chart.render_data_uri()
    

    return render_template('index.html', data=pagination_users, page=page, per_page=per_page, pagination=pagination, date_chart=date_chart)

@app.route('/localbitcoin')
def ind_localbitcoin():
    #return render_template('index.html', tables=[binance.to_html(classes='binance')], titles=df.columns.values)
    
    #paginacion
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = len(data2)
    pagination_users = get_users(0, 20, data2)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    #Grafico de barras
    bar_chart = pygal.Bar(style=custom_style)
    bar_chart.title = 'Top de los Bancos (metodos de pago) mas utilizados'
   # bar_chart.x_labels = map(str, range(2002, 2013))
    count_by_bank = localbitcoin['bank_name'].value_counts().head(15)
    [bar_chart.add(x[0], x[1]) for x in count_by_bank.items()]
    barchart_data=bar_chart.render_data_uri()

    #grafico de lineas
    date_chart = pygal.Line(x_label_rotation=30, fill=True, interpolate='cubic', style=custom_style)
    date_chart.title = 'Precio Promedio por dia del bitcoin'
    mean_by_date = localbitcoin.groupby(pd.Grouper(key='Timestamp',freq='D'))['temp_price'].mean()
    date_chart.x_labels = [str(x[0])[:10] for x in mean_by_date.items() if x[0] != 'Timestamp']
    #[date_chart.add(str(x[0])[:10], x[1]) for x in mean_by_date.items() if x[0] != 'Timestamp']
    date_chart.add('price mean',[x[1] for x in mean_by_date.items() if x[0] != 'Timestamp'] )
    date_chart= date_chart.render_data_uri()
    

    return render_template('localbitcoin.html', data=pagination_users, page=page, per_page=per_page, pagination=pagination, barchart_data=barchart_data, date_chart=date_chart)

@app.route('/binance')
def ind_binance():
    #return render_template('index.html', tables=[binance.to_html(classes='binance')], titles=df.columns.values)
    
    #paginacion
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = len(data1)
    pagination_users = get_users(0, 20, data1)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    #anuncios de compra y venta por dia
    date_chart = pygal.Line(x_label_rotation=20, fill=True, interpolate='cubic', style=custom_style)
    date_chart.title = 'Volumen de anuncios de compra y venta por dia'
    anuncios_by_date = binance.groupby(pd.Grouper(key='Timestamp',freq='D'))['trade_type'].value_counts()
    date_chart.x_labels = [str(x[0][0])[0:10] for x in anuncios_by_date.items() if x[0][1] != 'ONLY_BUY']
    date_chart.add('anuncios Venta',[x[1] for x in anuncios_by_date.items() if x[0][1] != 'ONLY_BUY'  ] )
    date_chart.add('anuncios Compra',[x[1] for x in anuncios_by_date.items() if x[0][1] != 'ONLY_Sell'  ] )
    date_chart=date_chart.render_data_uri()

    #Precio minimo y maximo de cada dia
    line_chart = pygal.Line(x_label_rotation=20, fill=True, interpolate='cubic', style=custom_style2)
    line_chart.title = 'Precios (max y min) Bitcoin por dia'
    max_by_date = binance.groupby(pd.Grouper(key='Timestamp',freq='D'))['temp_price'].max()
    min_by_date = binance.groupby(pd.Grouper(key='Timestamp',freq='D'))['temp_price'].min()
    line_chart.x_labels = [str(x[0])[:10] for x in max_by_date.items() if x[0] != 'Timestamp']
    line_chart.add('price max',[float(x[1].replace(',',''))   for x in max_by_date.items() ] )
    line_chart.add('price min',[float(x[1].replace(',',''))  for x in min_by_date.items() ] )
    line_chart=line_chart.render_data_uri()
    

    return render_template('binance.html', data=pagination_users, page=page, per_page=per_page, pagination=pagination, date_chart=date_chart, line_chart=line_chart)

@app.route('/localcrypto')
def ind_localcrypto():
    #return render_template('index.html', tables=[binance.to_html(classes='binance')], titles=df.columns.values)
    
    #Paginacion
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = len(data3)
    pagination_users = get_users(0, 20, data3)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    #grafico torta
    pie_chart = pygal.Pie(style=custom_style2)
    pie_chart.title = 'Cantidad de intercamvios (por categoria) en Marzo 2021'
    pie_chart.title = 'Trade Type usage in March 2021 (in %)'
    count_trade = localcryptos['trade_type'].value_counts()
    [pie_chart.add(x[0], x[1]) for x in count_trade.items()]
    pie_chart=pie_chart.render_data_uri()

    line_chart = pygal.HorizontalBar(style=custom_style)
    line_chart.title = 'Top 7 de Uusuarios con mas actividad'
    count_username = localcryptos['username'].value_counts().head(7)
    [line_chart.add(x[0], x[1]) for x in count_username.items()]
    line_chart=line_chart.render_data_uri()

    return render_template('localcrypto.html', data=pagination_users, page=page, per_page=per_page, pagination=pagination, pie_chart=pie_chart, line_chart=line_chart )

@app.route('/about_api')
def ind_api():
    #return render_template('index.html', tables=[binance.to_html(classes='binance')], titles=df.columns.values)
    


    return render_template('about_api.html')


@app.route('/api/v1/resources/source/localbitcoin', methods=['GET'])
def api_localbitcoin():
    result = localbitcoin.head(10000).to_json(orient="records")
    parsed = json.loads(result)
    return jsonify(parsed)

@app.route('/api/v1/resources/source/binance', methods=['GET'])
def api_binance():
    result = binance.head(10000).to_json(orient="records")
    parsed = json.loads(result)
    return jsonify(parsed)

@app.route('/api/v1/resources/source/localcrypto', methods=['GET'])
def api_localcrypto():
    result = localcrypto.head(10000).to_json(orient="records")
    parsed = json.loads(result)
    return jsonify(parsed)

@app.route("/download", methods=[ 'GET'])
def download():
    # Get the CSV data as a string from the session
    
    csv = localbitcoin.head(10000).to_csv(index=False, header=True, sep="|")
    
    # Create a string buffer
    buf_str = io.StringIO(csv)

    # Create a bytes buffer from the string buffer
    buf_byt = io.BytesIO(buf_str.read().encode("utf-8"))
    
    # Return the CSV data as an attachment
    return send_file(buf_byt,
                     mimetype="text/csv",
                     as_attachment=True,
                     attachment_filename="localbitcoin.csv")

#!/usr/bin/env python
# coding: utf-8

# In[11]:


#importando librerias necesarias
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import re
from selenium import webdriver
import time
import json


# ## Localbitcoin Ventas

# In[12]:


i = 0
r = []
#se realiza un ciclo para obtener las primeras 3 paginas del api
while i < 3:
    url = 'https://localbitcoins.com/sell-bitcoins-online/ves/.json?page='+ str(i)
    r.append( requests.get(url).json())
    #se aplica un sleep para evitar que el api bloquee la conexion debido multiples request simultaneos
    time.sleep(10)
    i += 1


# In[13]:


# se crea una nueva lista para guardar los valores aplanados
dflist=[]
i = 0
#se realiza un ciclo por cada pagina obtenida de la api
while i < 3:
    # el json del api devuelve una lista de ofertas
    #vamos a obtener cada oferta y guardarlo en un dataframe
    data = json.dumps(r[i]['data']['ad_list'])
    data2 = json.loads(data)
    df = pd.DataFrame(data2)
#print(df['data'])
    #se obtienen los valores de las listas internas en json de las columnas
    df1 = pd.DataFrame(df['data'].values.tolist())
    df2 = pd.DataFrame(df1['profile'].values.tolist())
#display (df2)
    # se guarda los valores en una lista, eliminando los valores originales que aplanamos
    dflist.append( pd.concat([df1.drop('profile', axis=1), df2], axis=1) )
    i += 1


# In[14]:


#se crea un dataframe para limpieza y
df1 = pd.DataFrame(df['data'].values.tolist())
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
#display (df1)


# In[15]:


#se verifica el tamaño de registros obtenidos por la pagina
#al realizar la ejecucion continuamente se nota que los anuncios tienen un tiempo determinado
# por lo que cada 15 min se obtienen nuevos anuncios si se ejecuta el proceso
dfsell = pd.concat(dflist, ignore_index=True)
#numero de registros
len(dfsell)


# In[16]:


#Limpieza de atributos en la columna de banco
#La idea es normalizar los nombre si se encuentra alguna frase que haga mencion a los bancos mas importantes en venezuela
dfsell.loc[(dfsell['bank_name'].str.contains("mercantil|Mercantil|MERCANTIL"), 'bank_name' )] = 'MERCANTIL'
dfsell.loc[(dfsell['bank_name'].str.contains("banesco|Banesco|BANESCO"), 'bank_name' )] = 'BANESCO'
dfsell.loc[(dfsell['bank_name'].str.contains("BOD|bod|Bod"), 'bank_name' )] = 'BOD'
dfsell.loc[(dfsell['bank_name'].str.contains("VENEZUELA|venezuela|Venezuela|BDV"), 'bank_name' )] = 'VENEZUELA'
dfsell.loc[(dfsell['bank_name'].str.contains("provincial|Provincial|PROVINCIAL"), 'bank_name' )] = 'PROVINCIAL'
dfsell.loc[(dfsell['bank_name'].str.contains("BVC|bvc|Venezolano|VENEZOLANO"), 'bank_name' )] = 'BVC'
dfsell.loc[(dfsell['bank_name'].str.contains("BNC|bnc|Credito|credito|Crédito|crédito|CREDITO|CRÉDITO"), 'bank_name' )] = 'BNC'
dfsell.loc[(dfsell['bank_name'].str.contains("bicentenario|Bicentenario|BICENTENARIO"), 'bank_name' )] = 'BICENTENARIO'
dfsell.loc[(dfsell['bank_name'].str.contains("Tesoro|tesoro|TESORO"), 'bank_name' )] = 'TESORO'
dfsell.loc[(dfsell['bank_name'].str.contains("Caribe|caribe|CARIBE|bancaribe|BANCARIBE"), 'bank_name' )] = 'BANCARIBE'
dfsell.loc[(dfsell['bank_name'].str.contains("FONDO|Fondo|fondo|BFC"), 'bank_name' )] = 'FONDOCOMUN'
dfsell.loc[(dfsell['bank_name'].str.contains("banplus|Banplus|BANPLUS"), 'bank_name' )] = 'BANPLUS'
dfsell.loc[(dfsell['bank_name'].str.contains("petro|Petro|PETRO"), 'bank_name' )] = 'PETRO'
dfsell.loc[(dfsell['bank_name'].str.contains("movil|Movil|MOVIL|movíl|Movíl|MOVÍL"), 'bank_name' )] = 'PAGOMOVIL'
dfsell = dfsell.replace('\n',' ', regex=True)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
#display (dfcomplete)
#dfcomplete.groupby('bank_name').size()


# In[17]:


#se eliminan las columnas sin relevancia para el analisis
del dfsell['require_feedback_score']
del dfsell['hidden_by_opening_hours']
del dfsell['first_time_limit_btc']
del dfsell['require_trusted_by_advertiser']
del dfsell['visible']
del dfsell['is_low_risk']
del dfsell['atm_model']
del dfsell['name']
dfsell['Timestamp']= pd.Timestamp.now()
#display (dfcomplete)


# In[18]:


# dataframe resultante con las ofertas de venta del dia
dfsell.head()


# ## Localbitcoin Compra

# In[19]:


# Se aplica el mismo proceso pero en este caso se trabajara con las ofertas ce compra
i = 0
r = []
#se realiza un ciclo para obtener las primeras 3 paginas del api
while i < 3:
    url = 'https://localbitcoins.com/buy-bitcoins-online/ves/.json?page='+ str(i)
    r.append( requests.get(url).json())
    #se aplica un sleep para evitar que el api bloquee la conexion debido multiples request simultaneos
    time.sleep(10)
    i += 1


# In[20]:


dflist=[]
i = 0
while i < 3:
    data = json.dumps(r[i]['data']['ad_list'])
    data2 = json.loads(data)
    df = pd.DataFrame(data2)
#print(df['data'])
    df1 = pd.DataFrame(df['data'].values.tolist())
    df2 = pd.DataFrame(df1['profile'].values.tolist())
#display (df2)
    dflist.append( pd.concat([df1.drop('profile', axis=1), df2], axis=1) )
    i += 1


# In[21]:


df1 = pd.DataFrame(df['data'].values.tolist())
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
#display (df1)


# In[22]:


dfbuy = pd.concat(dflist, ignore_index=True)
#longitud de registros
len(dfbuy)


# In[23]:


#Se aplica el mismo tipo de limpieza del nombre de las entidades bancarias
dfbuy.loc[(dfbuy['bank_name'].str.contains("mercantil|Mercantil|MERCANTIL"), 'bank_name' )] = 'MERCANTIL'
dfbuy.loc[(dfbuy['bank_name'].str.contains("banesco|Banesco|BANESCO"), 'bank_name' )] = 'BANESCO'
dfbuy.loc[(dfbuy['bank_name'].str.contains("BOD|bod|Bod"), 'bank_name' )] = 'BOD'
dfbuy.loc[(dfbuy['bank_name'].str.contains("VENEZUELA|venezuela|Venezuela|BDV"), 'bank_name' )] = 'VENEZUELA'
dfbuy.loc[(dfbuy['bank_name'].str.contains("provincial|Provincial|PROVINCIAL"), 'bank_name' )] = 'PROVINCIAL'
dfbuy.loc[(dfbuy['bank_name'].str.contains("BVC|bvc|Venezolano|VENEZOLANO"), 'bank_name' )] = 'BVC'
dfbuy.loc[(dfbuy['bank_name'].str.contains("BNC|bnc|Credito|credito|Crédito|crédito|CREDITO|CRÉDITO"), 'bank_name' )] = 'BNC'
dfbuy.loc[(dfbuy['bank_name'].str.contains("bicentenario|Bicentenario|BICENTENARIO"), 'bank_name' )] = 'BICENTENARIO'
dfbuy.loc[(dfbuy['bank_name'].str.contains("Tesoro|tesoro|TESORO"), 'bank_name' )] = 'TESORO'
dfbuy.loc[(dfbuy['bank_name'].str.contains("Caribe|caribe|CARIBE|bancaribe|BANCARIBE"), 'bank_name' )] = 'BANCARIBE'
dfbuy.loc[(dfbuy['bank_name'].str.contains("FONDO|Fondo|fondo|BFC"), 'bank_name' )] = 'FONDOCOMUN'
dfbuy.loc[(dfbuy['bank_name'].str.contains("banplus|Banplus|BANPLUS"), 'bank_name' )] = 'BANPLUS'
dfbuy.loc[(dfbuy['bank_name'].str.contains("petro|Petro|PETRO"), 'bank_name' )] = 'PETRO'
dfbuy.loc[(dfbuy['bank_name'].str.contains("movil|Movil|MOVIL|movíl|Movíl|MOVÍL"), 'bank_name' )] = 'PAGOMOVIL'
dfbuy = dfbuy.replace('\n',' ', regex=True)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
#display (dfcomplete)
#dfcomplete.groupby('bank_name').size()


# In[24]:


#se eliminan la misma cantidad de columnas para que  concuerden con el anterior dataframe y permita el merge
del dfbuy['require_feedback_score']
del dfbuy['hidden_by_opening_hours']
del dfbuy['first_time_limit_btc']
del dfbuy['require_trusted_by_advertiser']
del dfbuy['visible']
#del dfcomplete['is_low_risk']
del dfbuy['atm_model']
del dfbuy['name']
dfbuy['Timestamp']= pd.Timestamp.now()
#display (dfcomplete)


# In[25]:


#dataframe con ofertas de compra
dfbuy.head()


# In[26]:


#concatenacion de los dataframe de anuncios de venta y compra
#dataframe general de la pagina
dflocalbitcoin= pd.concat([dfsell, dfbuy])


# In[27]:


#añadiendo como columna la fuente de los datos
dflocalbitcoin['source'] = 'LocalBitcoin'
dflocalbitcoin['coin']= 'bitcoin'
# dataframe general de la pagina
dflocalbitcoin = dflocalbitcoin[['username','trade_count','bank_name','location_string','trade_type','temp_price','source','coin','Timestamp']]
dflocalbitcoin.head()


# ## Localcryptos compra

# In[28]:


#obtener las ofertas de compra
url ='https://localcryptos.com/Bitcoin/Venezuela/Buy'
html = requests.get(url).content


# In[29]:


soup = BeautifulSoup(html, "lxml")
# Buscar la informacion por el tag y clase
elem = [elem.text if 'Venezuela' in elem.text else None for elem in soup.find_all('div', {'class':'_HChx0m _2UfjJ2'})]
#limpieza de valores null
elem = list(filter(None,elem))
#limpieza de campos y colocacion de | como separador
elem = [ re.sub(r'No trades yet', r'||' ,i) for i in elem  ]
elem = [ re.sub(r'~(.*)trades', r'|\1|' ,i) for i in elem  ]
elem = [ re.sub(r' (.*)trades', r'|\1|' ,i) for i in elem  ]
elem = [ re.sub('"Venezuela', '|Venezuela ' ,i) for i in elem  ]
elem = [ re.sub(r'Caracas', r'Caracas|' ,i) for i in elem  ]
elem = [ re.sub(r'Maracay', r'Maracay|' ,i) for i in elem  ]
elem = [ re.sub(r'Porlamar', r'Porlamar|' ,i) for i in elem  ]
elem = [ re.sub(r'Táchira', r'Táchira|' ,i) for i in elem  ]
elem = [ re.sub(r'Cristóbal', r'Cristóbal| ' ,i) for i in elem  ]
elem = [ re.sub(r'Barinas', r'Barinas|' ,i) for i in elem  ]
elem = [ re.sub(r'Guasipati', r'Guasipati|' ,i) for i in elem  ]
elem = [ re.sub(r'Barquisimeto', r'Barquisimeto|' ,i) for i in elem  ]
elem = [ re.sub(r'Buy', r'|Buy' ,i) for i in elem  ]
#elem = [ re.sub(r'Bs', r'|Bs' ,i) for i in elem  ]
#elem = [ re.sub(r'$', r'|$' ,i) for i in elem  ]
#elem = [ re.sub(r'€', r'|€' ,i) for i in elem  ]
elem = [ i.split('|') for i in elem  ]
#elem


# In[30]:


#columns=[['user','cant_trades','metodo_pago','']]
dfbuy = pd.DataFrame(elem)
del dfbuy[6]
#renombre de columnas y agregacion de columnas predefinadas
dfbuy.columns =['username','trade_count','bank_name','location_string','temp_price','trade_type']
dfbuy['trade_type']= 'ONLY_BUY'
dfbuy['source']= 'localcryptos'
dfbuy['coin']= 'bitcoin'
dfbuy['Timestamp']= pd.Timestamp.now()


# ## Localcryptos venta

# In[31]:


#obtener las ofertas de Venta
url ='https://localcryptos.com/Bitcoin/Venezuela/Sell'
html = requests.get(url).content


# In[32]:


soup = BeautifulSoup(html, "lxml")
# Buscar la informacion por el tag y clase
elem = [elem.text if 'Venezuela' in elem.text else None for elem in soup.find_all('div', {'class':'_HChx0m _2UfjJ2'})]
#limpieza de valores null
elem = list(filter(None,elem))
#limpieza de campos y colocacion de | como separador
elem = [ re.sub(r'No trades yet', r'||' ,i) for i in elem  ]
elem = [ re.sub(r'~(.*)trades', r'|\1|' ,i) for i in elem  ]
elem = [ re.sub(r' (.*)trades', r'|\1|' ,i) for i in elem  ]
elem = [ re.sub('"Venezuela', '|Venezuela ' ,i) for i in elem  ]
elem = [ re.sub(r'Caracas', r'Caracas|' ,i) for i in elem  ]
elem = [ re.sub(r'Maracay', r'Maracay|' ,i) for i in elem  ]
elem = [ re.sub(r'Porlamar', r'Porlamar|' ,i) for i in elem  ]
elem = [ re.sub(r'Táchira', r'Táchira|' ,i) for i in elem  ]
elem = [ re.sub(r'Cristóbal', r'Cristóbal| ' ,i) for i in elem  ]
elem = [ re.sub(r'Barinas', r'Barinas|' ,i) for i in elem  ]
elem = [ re.sub(r'Guasipati', r'Guasipati|' ,i) for i in elem  ]
elem = [ re.sub(r'Barquisimeto', r'Barquisimeto|' ,i) for i in elem  ]
elem = [ re.sub(r'Sell', r'|Sell' ,i) for i in elem  ]
#elem = [ re.sub(r'Bs', r'|Bs' ,i) for i in elem  ]
#elem = [ re.sub(r'$', r'|$' ,i) for i in elem  ]
#elem = [ re.sub(r'€', r'|€' ,i) for i in elem  ]
elem = [ i.split('|') for i in elem  ]
#elem


# In[33]:


#columns=[['user','cant_trades','metodo_pago','']]
dfsell = pd.DataFrame(elem)
#del dfsell[6]
#renombre de columnas y agregacion de columnas predefinadas
dfsell.columns =['username','trade_count','bank_name','location_string','temp_price','trade_type']
dfsell['trade_type']= 'ONLY_SELL'
dfsell['source']= 'localcryptos'
dfsell['coin']= 'bitcoin'
dfsell['Timestamp']= pd.Timestamp.now()


# In[34]:


# Dataframe global de la pagina
dflocalcryptos= pd.concat([dfsell, dfbuy])


# In[35]:


dflocalcryptos.head()


# ## Binance buy

# In[36]:


#para ocultar el navegador
options = webdriver.FirefoxOptions()
options.headless = True
browser = webdriver.Firefox(options=options)
#browser = webdriver.Firefox()
browser.get('https://c2c.binance.com/es/trade/buy/BTC')
time.sleep(5)


# In[37]:


#funciona para obtener una valor usando selenium a partir de una clave en css
def obtener_valor(browser,css):
    lists= browser.find_elements_by_css_selector(css)
    list_r = []
    for l in lists:
        list_r.append(l.text)
    return list_r


# In[38]:


#funciona para obtener una valor usando selenium a partir de una tag id
def obtener_valor_id(browser,ids):
    lists= browser.find_elements_by_id(ids)
    list_r = []
    for l in lists:
        list_r.append(l.text)
    return list_r


# In[39]:


#funciona para obtener los bancos
def obtener_binance_banco(browser,x,y):
    lists_caja= browser.find_elements_by_css_selector("div[class='css-1w5q6ud']")
    i =0
    list_banco = []
    for l in lists_caja:
        lists= l.find_elements_by_css_selector("div[class='css-uj9ajp'][data-bn-type='text']")
        s = ''
        for listitem in lists:
            s += listitem.get_attribute('title')+', '
        list_banco.append(s)
    return list_banco   


# In[40]:


# funcion para verificar si nos encontramos en la ultima pagina de las ofertas
def ultimapagina(browser):
    try:
        browser.find_element_by_css_selector("button[aria-label='Next page'][disabled='']")
    except NoSuchElementException:
        #verificar que este entrando en la excepcion
        #print('siguiente pagina')
        return True
    return False


# #### cambiar a moneda VES

# In[41]:


#selecionar el boton para cambio de moneda
time.sleep(2)
button = browser.find_element_by_id('C2Cfiatfilter_searhbox_fiat')
button.click()


# In[42]:


#ingresar VES para cambiar de moneda
time.sleep(2)
menu1 = browser.find_element_by_css_selector("input[placeholder='']")
menu1.send_keys('VES', Keys.ENTER)


# ### Extraccion con varias paginas

# In[44]:


#bloque de codigo con todas las busquedas que se realiza en 1 pagina, para que se ejecute automaticamente
# este bloque genera varias listas con la informacion de todas las paginas de oferta de compra
list_user = []
list_trade = []
list_banco = []
list_price = []
c = 0
siguiente = True
time.sleep(10)
while siguiente:
    list_user+= obtener_valor_id(browser,'C2Cofferlistsell_link_merchant')
    list_trade+= obtener_valor(browser,"div[class='css-1a0u4z7']")
    list_banco+= obtener_binance_banco(browser,"div[class='css-1w5q6ud']","div[class='css-uj9ajp'][data-bn-type='text']")
    list_price+= obtener_valor(browser, "div[class='css-1m1f8hn']" )
    button = browser.find_element_by_css_selector("button[aria-label='Next page']")
    button.click()
    if ultimapagina(browser) == False and c == 0:
        c = 1
    elif ultimapagina(browser) == False and c == 1:
        siguiente = False
    else:
        pass
    time.sleep(5)


# #### username (1 pagina)

# In[45]:


#list_user = obtener_valor_id(browser,'C2Cofferlistsell_link_merchant')


# In[46]:


#list_user


# #### trade_count (1 pagina)

# In[47]:


#list_trade= obtener_valor(browser,"div[class='css-1a0u4z7']")


# In[48]:


#list_trade


# #### bank_name (1 pagina)

# In[49]:


#list_banco= obtener_binance_banco(browser,"div[class='css-1w5q6ud']","div[class='css-uj9ajp'][data-bn-type='text']")


# In[50]:


#list_banco


# ### temp_price (1 pagina)

# In[51]:


#list_price = obtener_valor(browser, "div[class='css-1m1f8hn']" )


# In[52]:


#list_price


# ### concatenacion de todas las listas

# In[53]:


#concatenacion de todas las listas para generar el dataframe
dfbuy = pd.DataFrame(list(zip(list_user, list_trade, list_banco , list_price)), 
               columns =['username', 'trade_count', 'bank_name', 'temp_price' ])
#creacion de columnas generadas por defecto
dfbuy['location_string'] = 'Venezuela'
dfbuy['trade_type']= 'ONLY_BUY'
dfbuy['source']= 'Binance'
dfbuy['coin']= 'bitcoin'
dfbuy['Timestamp']= pd.Timestamp.now()
#dataframe general de compra de binance
dfbuy = dfbuy[['username', 'trade_count', 'bank_name','location_string','trade_type', 'temp_price','source','coin','Timestamp']]
dfbuy.head()


# ## Binance sell

# In[54]:


#mover selenium a la pagina de ofertas de venta
browser.get('https://c2c.binance.com/es/trade/sell/BTC')
time.sleep(5)


# #### cambiar a moneda VES

# In[55]:


#mismo procedimiento para cambiar el tipo de moneda
time.sleep(2)
button = browser.find_element_by_id('C2Cfiatfilter_searhbox_fiat')
button.click()


# In[56]:


time.sleep(2)
menu1 = browser.find_element_by_css_selector("input[placeholder='']")
menu1.send_keys('VES', Keys.ENTER)


# ### Extraccion con varias paginas

# In[57]:


#bloque de codigo con todas las busquedas que se realiza en 1 pagina, para que se ejecute automaticamente
# este bloque genera varias listas con la informacion de todas las paginas de oferta de venta
list_user = []
list_trade = []
list_banco = []
list_price = []
c = 0
siguiente = True
time.sleep(10)
while siguiente:
    list_user+= obtener_valor_id(browser,"C2Cofferlistbuy_link_merchantdetail")
    list_trade+= obtener_valor(browser,"div[class='css-1a0u4z7']")
    list_banco+= obtener_binance_banco(browser,"div[class='css-1w5q6ud']","div[class='css-uj9ajp'][data-bn-type='text']")
    list_price+= obtener_valor(browser, "div[class='css-1m1f8hn']" )
    button = browser.find_element_by_css_selector("button[aria-label='Next page']")
    button.click()
    if ultimapagina(browser) == False and c == 0:
        c = 1
    elif ultimapagina(browser) == False and c == 1:
        siguiente = False
    else:
        pass
    time.sleep(5)


# #### username (1 pagina)

# In[58]:


#list_user= obtener_valor_id(browser,"C2Cofferlistbuy_link_merchantdetail")


# In[59]:


#list_user


# #### trade_count (1 pagina)

# In[60]:


#list_trade= obtener_valor(browser,"div[class='css-1a0u4z7']")


# In[61]:


#list_trade


# #### bank_name (1 pagina)

# In[62]:


#list_banco = obtener_binance_banco(browser,"div[class='css-1w5q6ud']","div[class='css-uj9ajp'][data-bn-type='text']")


# In[63]:


#list_banco


# ### temp_price (1 pagina)

# In[64]:


#list_price = obtener_valor(browser, "div[class='css-1m1f8hn']" )


# In[65]:


#list_price


# ### concatenacion de todas las listas

# In[73]:


#concatenacion de todas las listas para generar el dataframe
dfsell = pd.DataFrame(list(zip(list_user, list_trade, list_banco , list_price)), 
               columns =['username', 'trade_count', 'bank_name', 'temp_price' ])
#creacion de columnas generadas por defecto
dfsell['location_string'] = 'Venezuela'
dfsell['trade_type']= 'ONLY_Sell'
dfsell['source']= 'Binance'
dfsell['coin']= 'bitcoin'
dfsell['Timestamp']= pd.Timestamp.now()
#dataframe general de ventas de binance
dfsell = dfsell[['username', 'trade_count', 'bank_name','location_string','trade_type', 'temp_price','source','coin','Timestamp']]
dfsell.head()


# #### concatenar ambos dataframe para crear el general

# In[67]:


dfbinance= pd.concat([dfsell, dfbuy])
dfbinance.head()


# In[68]:


#cerrrar el navegador
browser.close()


# ## Dataframe merge de las 3 fuentes

# In[69]:


dftotal= pd.concat([dflocalbitcoin, dflocalcryptos, dfbinance])
dftotal= dftotal.reset_index(drop=True)


# In[70]:


dftotal.head()


# ## Export a CSV

# In[78]:


#fecha de la extraccion 
date= str(pd.Timestamp.now())[:19].replace(' ','_').replace(':','')


# In[82]:



#exportar en CSV con | como separador
dftotal.to_csv('C:\\Users\\Mercantil\\ironhacks\\data_cripto\\cripto'+date+'.csv', encoding='utf-8', index=False, sep='|')


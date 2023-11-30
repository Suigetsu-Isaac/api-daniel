import requests

import datetime

KEY = '350218a4a1cacc93515a7671a43a5793'
def requisicaojson(metodo, url, mapa=False):
    site = 'https://api.openweathermap.org/'
    saida = site
    if (mapa):
        saida+='geo/1.0/'
    else:
        saida+='data/2.5/'
    saida+=metodo+'?'+url
    
    requisicao = requests.get(saida)
    return requisicao.json()

def lat_lon(cidade,estado='Pernambuco',pais="br"):
    
    mapa = requisicaojson('direct',f'q={cidade}&limit=5&appid={KEY}',mapa=True)
   
    
    for e in mapa:
        if e['state'] == estado:
         
            return [e['lat'], e['lon']]

    return "Não encontrado"

def celsus(temp):
    return int(round(temp -273,0))

def datahoje():
    data = datetime.datetime.now()
    data = str(data).split(' ')
    dia = data[0]
    horario = data[1]
    horario = horario.split('.')
    horario = horario[0]
    
    return [dia,horario]

def agora(lat,lon):
   
    agora = requisicaojson('weather',f'lat={lat}&lon={lon}&appid={KEY}&lang=pt')

    clima = agora['weather'][0]
    main = agora['main']
    try:
        chuva = main['rain'].values(),
    except:
        chuva = 0
        
    data = datahoje()
    return {
        'data': {
            'dia': data[0],
            'horario': data[1]
            
        },
        'principal':{
            'temp': celsus(main['temp']),
            'max': celsus(main['temp_max']),
            'min': celsus(main['temp_min']),
            'sensacao': celsus(main['feels_like']),
            'umidade': main['humidity'],
            'chuva': chuva,
            'vento': kmh(agora['wind']['speed'])
        },
        'clima': {
            'main': traducao(clima['main']),
            'desc': clima['description']
        }
    }  

def kmh(milhas):
    return int(round(milhas * 1.6,0))

def traducao(texto):
    
    if texto == 'Clouds':
        return 'Nublado'
    if texto == "Clear":
        return 'Limpo'
    return 'Chuvendo'



    

def previsao5dias(lat,lon):
    
   

    url = requisicaojson('forecast',f'lat={lat}&lon={lon}&appid={KEY}&lang=pt')

    lista = url['list']

    dic={
        'data': {
            'dia': '',
            'horario': []
            },
        'principal':{
            'temp': [],
            'min': [],
            'max': [],
            'umidade': [],
            'vento': [],
            'chuva': [],
        },
        'clima': {
            'main': [],
            'desc': [],
            
            
        } 
    }
    


    lista_principal=[
    ]




    dia = ''
    for e in lista:
        main = e['main']
    
        data = e['dt_txt']
        data = data.split(' ')
        horario = data[1]
        horario = horario.split(":")
        horario = horario[0]
        data = data[0]

        if (dia != data.split('-')[2]):
            lista_principal.append(dic)
            dic={
                'data': {
                'dia': '',
                'horario': []
                },
                'principal':{
                    'temp': [],
                    'min': [],
                    'max': [],
                    'umidade': [],
                    'vento': [],
                    'chuva': [],
                },
                'clima': {
                    'main': [],
                    'desc': [],

                } 
            }

   
        dic['data']['horario'].append(horario)
        dia = data.split('-')[2]
 
        dic['data']['dia'] = data
    

        dic['principal']['temp'].append(celsus(main['temp']))
        dic['principal']['umidade'].append(main['humidity'])
        dic['principal']['min'].append(celsus(main['temp_min']))
        dic['principal']['max'].append(celsus(main['temp_max']))
        clima = e['weather'][0]
   
        dic['clima']['main'].append(traducao(clima['main']))
        dic['clima']['desc'].append(clima['description'])
    
        dic['principal']['vento'].append(kmh(e['wind']['speed']))
    
        dic['principal']['chuva'].append(e.get('rain') )
       
        
    return lista_principal



if __name__ == '__main__':
    
    
    latlon = lat_lon('Salgueiro','Pernambuco')

    
    now = agora(latlon[0],latlon[1])


    pr = previsao5dias(latlon[0],latlon[1])
    del pr[0]
    
    print('agora: ',now)
    print('previsao: ',pr)
    
from flask import Flask, render_template, request,flash, redirect, url_for, session, Request
import datetime
from utils import estado
from funcoes import lat_lon,agora,previsao5dias
from collections import Counter

app = Flask(__name__)

@app.route('/')
@app.get('/index')
def index():
   
  
   # template tendo a cidade salgueiro pernambuco 
   lat_lon = pegarCidade(cidade='Salgueiro',estado='Pernambuco')
   clima_agora = pegar_agora(lat_lon[0],lat_lon[1])
   clima_previsao = previsao(lat_lon[0],lat_lon[1])
   
   horario=clima_agora['data']['horario']
   horario = dia_noite(horario)
   print(horario)
   bg_body = ''
   bg_button = ''
   if (horario == 'noite'):
      bg_body = 'bg-f-azul-escuro'
      bg_button = 'bg-f-azul-claro'
   else:
      bg_body = 'bg-f-azul-claro'
      bg_button = 'bg-f-verde'
   
   
   print(bg_body)
   print(bg_button)
   semana = []
   
   for e in clima_previsao:
      semana.append( pegar_dia_da_semana(e['data']['dia']))
   dia = pegar_dia_da_semana(clima_agora['data']['dia']) 
   
   return render_template('index.html', estados=estado(),
                           bg_body=bg_body, bg_button=bg_button, horario=horario, 
                          dia_hoje=dia, dia_previsao = semana,
                          agora = clima_agora, previsao=clima_previsao
                          )

def dia_noite(horario):
   horario = horario.split(':')
   horario = int(horario[0])
   if horario >= 6 and horario <=18:
      return 'dia'
   return 'noite'
   
@app.post('/index')
def clima():
   
   cidade = request.form['cidade']
   state = request.form['estado']
   lat_lon = pegarCidade(cidade=cidade,estado=state)
   
   clima_agora = pegar_agora(lat_lon[0],lat_lon[1])
   
   clima_previsao = previsao(lat_lon[0],lat_lon[1])
   horario=clima_agora['data']['horario']
   horario = dia_noite(horario)
   print(horario)
   bg_body = ''
   bg_button = ''
   if (horario == 'noite'):
      bg_body = 'bg-f-azul-escuro'
      bg_button = 'bg-f-azul-claro'
   else:
      bg_body = 'bg-f-azul-claro'
      bg_button = 'bg-f-verde'
   
   
   print(bg_body)
   print(bg_button)
   semana = []
   
   for e in clima_previsao:
      semana.append( pegar_dia_da_semana(e['data']['dia']))
   dia = pegar_dia_da_semana(clima_agora['data']['dia']) 

   return render_template('index.html', estados=estado(),
                          bg_body=bg_body, bg_button=bg_button, horario=horario, 
                          dia_hoje=dia, dia_previsao = semana,
                          agora = clima_agora, previsao=clima_previsao)
    


def pegarCidade(cidade='Salgueiro',estado='PE'):
    latlon = lat_lon(cidade,estado)

    return latlon

def pegar_agora(lat,lon): 
    return agora(lat,lon)

def previsao(lat,lon):
    pr = previsao5dias(lat,lon)
    del pr[0]
    return pr

def pegar_dia_da_semana(data):
   
   semana = ['Segunda','Terça','Quarta','Quinta','Sexta','Sábado','Domingo']
   
   data = str(data)

   data = data.split('-')
   dia = int(data[2])
   mes = int(data[1])
   ano = int(data[0])
   num = datetime.date(ano,mes,dia).weekday()
   return semana[num]

def elemento_mais_repetido(lista):
    contador = Counter(lista)
    return contador.most_common(1)[0][0]

app.jinja_env.globals.update(elemento_mais_repetido=elemento_mais_repetido)


if __name__ == '__main__':
    app.secret_key = "admin123"
    app.run(debug=True)
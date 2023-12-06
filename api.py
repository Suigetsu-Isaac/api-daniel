import datetime

data = '2023-11-28'

data = data.split('-')
dia = int(data[2])
mes = int(data[1])
ano = int(data[0])
num = datetime.date(ano,mes,dia).weekday()

print(num)


lista=[1,2,4,6]


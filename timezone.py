import pytz

sao_paulo_timezone = pytz.timezone('America/Sao_Paulo')
# supondo que minha_data_hora tenha um datetime no formato UTC 
data_hora =  minha_data_hora.astimezone(sao_paulo_timezone)
print(data_hora) #mostra na tela a data hora convertido para o meu fuso horario desejado
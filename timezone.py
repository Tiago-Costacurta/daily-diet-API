import pytz

def AdjustTimezone(date):
    sao_paulo_timezone = pytz.timezone('America/Sao_Paulo')

    return date.astimezone(sao_paulo_timezone).strftime('%Y-%M-%D %H:%M:%S')

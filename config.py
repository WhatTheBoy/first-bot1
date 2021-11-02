
TOKEN = '2040207007:AAFnxtDn17ZkI3nDALppEHiAAI7d7I1v-14'

URL = 'https://api.telegram.org/bot{token}/{method}'


UPDATE_METH = 'getUpdates'
SEND_METH = 'sendMessage'

MY_ID = 809726762

UPDATE_ID_FILE_PATH = 'update_id'

with open(UPDATE_ID_FILE_PATH) as file:
    data = file.readline()
    if data:
        data = int(data)
    UPDATE_ID = data


WEATHER_TOKEN = '65ff1c67155c8fe82ae7fcf9fc506204'

WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={token}'


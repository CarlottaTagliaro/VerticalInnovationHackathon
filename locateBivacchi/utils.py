import requests
import json
import math

headers = {'Authorization':'Bearer QAFYq4Vd-oNSQJ92UpVhSg_ZwxYoq3kkmmJAXxdeFvzqb_M9rqmGBtSM1TR1Cz8nB21oQtm3837RK-jriYPINEfuexH_4gBCRTVrL08H3q1Q-6vXZOphfih4A_lbcBihqvlhNXT-uWPFn8iPPK4oVENjI9B2GMKI6ubG_Go9m4EzaCfHW1PE4I9BMwAfF55oUt-N2qITCyX3Y_0F3WE9p6iyr5KbBaFGelD6SE7ii26uGcMXmxFb4t6EGtbuuQo3xzDh_A7uXINt0T8Jdex6noWbTxv1ys-A0N0yw7JUbZ3jwmBLxwKjPLHN33yWay9RMYoCg0kVGBAM_d3nItyMGUg1vvtpGK11YIhW9xLSJSQNJcW7ycnfjTCPA4vowwbcOCupBCE3EjBLyXIjen8T3G-226SXCpmKtaf0CT92AhgTA-TCUS-u8aCfgRd0iEAv7r5nm66V8QIqc8D5wR1UHLK-IKE7DnEmuX1XaQ3pUka2sdTL9ez4-6mPHA5xi8PJ2PBAWqx-QG4S10CodJMQyzqqCtT_isOYuVfnmSghbvlrcRoCuXlak1mkrktBHe_1'}

def get_data():
    r = requests.get('http://tourism.opendatahub.bz.it/api/Weather/Realtime?language=en', headers=headers).content.decode()
    return json.loads(r)

def get_nearest_station(lat, lon):
    d = get_data()
    min = -1
    nearest = -1
    for i in d:
        if min == -1 or math.sqrt((lat-i['latitude'])**2+(lat-i['longitude'])**2)<min:
            min = math.sqrt((lat-i['latitude'])**2+(lon-i['longitude'])**2)
            nearest = i
    return nearest
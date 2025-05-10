from flask import Flask, request
from datetime import datetime
import joblib
import sqlite3

App = Flask(__name__)
model = joblib.load('model/Modelo_Floresta_Aleatorio_v100.pkl')

@App.route('/', methods=['GET'])
def home():
    return {'Response':'Ok'}

@App.route('/api/predictive/<area>;<rooms>;<bathroom>;<parking_spaces>;<floor>;<animal>;<furniture>;<hoa>;<property_tax>', methods=['GET'])
def api_predictive(area, rooms, bathroom, parking_spaces, floor, animal, furniture, hoa, property_tax):
    start_date = datetime.now()
    params_list = [float(area), float(rooms), float(bathroom), float(parking_spaces), float(floor), float(animal), float(furniture), float(hoa), float(property_tax)]
    try:
        prevision = model.predict([params_list])
        params_list.append((prevision[0]))

        input_str = ''
        for param in params_list:
            input_str = input_str + ';' + str(param)

        input_str = input_str[1:]

        end_date = datetime.now()
        process_time = end_date - start_date

        db_conn = sqlite3.connect('api.db')
        cursor = db_conn.cursor()

        cursor.execute(f'''
            INSERT INTO log_api (inputs, start_date, end_date, process_time) 
            VALUES ('{input_str}', '{start_date}', '{end_date}', '{process_time}')
        ''')
        db_conn.commit()
        cursor.close()

        return {'response' : str(prevision[0])}
    except:
        return {'error' : f'fail to load rental value'}

if __name__ == "__main__":
    App.run(debug=True)

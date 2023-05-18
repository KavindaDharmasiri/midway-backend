from flask import Blueprint, request, jsonify
import pandas as pd
import requests
import mysql.connector as connection
db = connection.connect(host='database-midway.cnjonpzevrxo.us-east-1.rds.amazonaws.com',user='admin', password='root1234', database= 'midway')

search_bp = Blueprint('search', __name__)




@search_bp.route('/searchByName', methods=['GET'])
def search_location():
    location = request.args.get('location')

    # Perform location filtering using OpenStreetMap Nominatim service
    filtered_results = filter_location(location)

    # Return the filtered results as JSON response

    return jsonify(filtered_results)

def filter_location(location):
    base_url = 'https://nominatim.openstreetmap.org/search'
    params = {'q': location, 'format': 'json', 'limit': 10,'countrycodes':'LK'}
    del params['limit']
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        filtered_results = []
        for result in data:
            place = {
                'Name': result.get('display_name'),
                'latitude': result.get('lat'),
                'longitude': result.get('lon'),
                'Type': result.get('type')
            }
            filtered_results.append(place)
        
        return filtered_results
    else:
        return []
    


def execute_query(query):
    from app import connection2
    cursor = connection2.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    return result


def delete():
    from app import connection2

    cursor = connection2.cursor()
    cursor.execute("delete from saveSuggest")
    cursor.execute()
    cursor.close()
    

@search_bp.route('/savetype', methods=['GET'])
def save_location():
    type = request.args.get('type')
    name = request.args.get('name')

    print(type)
    print(name)

    from app import connection2

   

    cursor = connection2.cursor()

    delete_query = "DELETE FROM saveSuggest"
    cursor.execute(delete_query)
    
    qury = 'insert into saveSuggest(name,type) value (%s,%s)'
    value = (name,type)
    cursor.execute(qury, value)

    connection2.commit()

    cursor.close()
    



    return "done"


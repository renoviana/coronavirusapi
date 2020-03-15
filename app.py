import os
from flask import Flask, jsonify, request, Response, redirect
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)
CORS(app)


def conversor(arrayTd):    
    return {
        'pais': arrayTd[0].text if arrayTd[0].text != " " else "0",
        'totalCasos': float(arrayTd[1].text.replace(',','') if arrayTd[1].text != " " else "0"),
        'novosCasos': float(arrayTd[2].text[2:-1].replace(',','') if arrayTd[2].text != " " else "0"),
        'totalMortes': float(arrayTd[3].text[1:-1].replace(',','') if arrayTd[3].text != " " else "0"),
        'novasMortes': float(arrayTd[4].text[1:-1].replace(',','') if arrayTd[4].text != " " else "0"),
        'totalCurados': float(arrayTd[5].text[:-1].replace(',','') if arrayTd[5].text != " " else "0"),
        'casosAtivos': float(arrayTd[6].text[1:-1].replace(',','') if arrayTd[6].text != " " else "0"),
        'casosGraves': float(arrayTd[7].text[:-1].replace(',','') if arrayTd[7].text != " " else "0"),
        'Total/1M pop': float(arrayTd[8].text if arrayTd[8].text != "" else "0")
    }

@app.route('/')
def init():
    soup = BeautifulSoup(requests.get('https://www.worldometers.info/coronavirus').text, 'html.parser')
    coronaData = [conversor(tr.find_all('td') ) for tr in soup.find('table',{'id':'main_table_countries'}).find_all('tr')[1:]]
    return jsonify(coronaData)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

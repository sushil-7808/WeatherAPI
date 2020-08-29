import requests
import configparser
from flask import Flask, render_template, request

# name= name of this application which is replaced in runtime
app = Flask(__name__)


# mapping this web page to this specific route home page '/'

# declarative joins both function and syntax together
@app.route('/')
def render_weather_dashboard():
    return render_template("home.html")


@app.route('/results', methods=['POST'])
def render_results():
    zip_code = request.form['zipCode']

    api_key = get_api_key()
    data = get_weather_results(zip_code, api_key)
    temp = "{0:.2f}".format(data["main"]["temp"])
    feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    # getting first value of API [0]
    weather = data["weather"][0]["main"]
    location = data["name"]

    return render_template('results.html', location=location, temp=temp, feels_like=feels_like, weather=weather)


# render results
def get_weather_results(zip_code, api_key):
    api_url = "http://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()


# function to get api from from config file
def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']


# ensuring flask run only once , multiple instances are not created
if __name__ == '__main__':
    app.run()

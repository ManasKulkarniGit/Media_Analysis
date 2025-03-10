import os
import requests
import csv
import pandas as pd
from flask import Flask, render_template, url_for, request
app = Flask(__name__)

from dotenv import load_dotenv

global newsObject

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        api_key = os.environ.get('API_KEY', '')


        headers = {'Authorization': api_key}

        everything = 'https://newsapi.org/v2/everything?'


        kwds = request.form.get("company")

        sources = ['business-insider', 'google-news', 'financial-post',
                'reuters', 'nbc-news', 'techcrunch', 'the-wall-street-journal']

        sortby = 'popularity'
        params = {
            'q': kwds,
            'apiKey': api_key,
            'sortBy': sortby,
            'language': 'en',
            'page': 1
                }

        response = requests.get(url=everything, headers=headers, params=params)

        output = response.json()
        # print(output)

        articles = output['articles']

        df = pd.DataFrame(articles)
        df.to_csv('news_data.csv')
       
        import projectModel
        with open('COMMON-PROCESSED.csv', 'r', encoding="utf8") as file:
            rows = []
            reader = csv.DictReader(file)
            for row in reader:
                rows.append(row)
        return render_template('csv.html', rows=rows)


    return render_template('index.html')


@app.route("/team")
def about():
    return render_template('team.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/services")
def services():
    return render_template('services.html')

@app.route("/db")
def dashboard():
    import plotlyGraph
    return render_template('db.html')

app.run(debug=True)

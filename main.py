from flask import Flask, jsonify, request
import pandas as pd
from demographic_filtering import output 
from content_filtering import get_recommendations


article_data = pd.read_csv("articles.csv")

all_articles = article_data[['title', 'url', 'time_stamp', 'Content_type', 'lang']]
liked_articles = []
disliked_articles = []
unread_articles = []

def get_data():
    data = {
        'title' : all_articles.iloc[0,12],
        'url' : all_articles.iloc[0,11],
        'time_stamp' : all_articles.iloc[0,2] or 'N/A',
        'duration' : all_articles.iloc[0,3],
        'language' : all_articles.iloc[0,4]/2
    }
    return data

app = Flask(__name__)
@app.route('/articles')
def movies():
    articles_data = get_data()
    return jsonify({'data':articles_data})

@app.route('/liked', methods = ['POST'])
def like():
    global all_articles
    data = get_data()
    liked_articles.append(data)
    all_articles.drop([0], inplace = True)
    all_articles = all_articles.reset_index(drop = True)
    return jsonify({
        'status' : 'success'
    })

@app.route('/disliked', methods = ['POST'])
def dislike():
    global all_articles
    data = get_data()
    disliked_articles.append(data)
    all_articles.drop([0], inplace = True)
    all_articles = all_articles.reset_index(drop = True)
    return jsonify({
        'status' : 'success'
    })

@app.route('/unread', methods = ['POST'])
def unwatched():
    global all_articles
    data = get_data()
    unread_articles.append(data)
    all_articles.drop([0], inplace = True)
    all_articles = all_articles.reset_index(drop = True)
    return jsonify({
        'status' : 'success'
    })

@app.route('/popular-articles')

def popular_movies():
    popular_data =[]
    for i, data in output.iterrows():
        d = {
            'title' :data['title'],
            'url' : data['url'],
            'time_stamp' : data['time_stamp'] or 'N/A',
            'duration' : data['Content_type'],
            'language' : data['lang']

        }
        popular_data.append(d)
    return jsonify({'data' : popular_data})

@app.route('/recommended-movies')
def recommended_movies():
    global liked_articles
    names = ['title','url','Content_type','time_stamp','lang']
    recommendations = pd.DataFrame(columns = names)
    for i in liked_articles:
        output = get_recommendations(i['title'])
        recommendations = recommendations.append(output)
    recommendations.drop_duplicates(subset = ['title'],inplace = True)
    recommended_data =[]
    for i, data in recommendations.iterrows():
        d = {
            'title' :data['title'],
            'url' : data['url'],
            'time_stamp' : data['time_stamp'] or 'N/A',
            'duration' : data['Content_type'],
            'language' : data['lang']

        }
        recommended_data.append(d)
    return jsonify({'data' : recommended_data})


app.run()
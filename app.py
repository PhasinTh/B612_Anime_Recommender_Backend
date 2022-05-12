from datetime import datetime
import json
import math
from flask import Flask, request, jsonify

app = Flask(__name__)
f = open('data/anime.json', 'r', encoding='utf-8')
animes = json.load(f)
sorted(animes, key=lambda k: k if len(k['start_date']) < 8 else datetime.strptime(k['start_date'], "%Y-%m-%d %H:%M:%S"))

def get_datas(datas, offset=0, per_page=10):
    return datas[offset: offset + per_page]

@app.route("/anime")
def get_anime():
    q = request.args.get("q", "", type=str)
    searchData = animes
    if q:
        searchData = [x for x in animes if q.lower() in x['title'].lower()]
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    offset = (page - 1) * per_page
    count = len(searchData)
    pages = math.ceil(len(searchData) / per_page)
    pagination_animes = get_datas(searchData, offset=offset, per_page=per_page)
    result = {
        "data": pagination_animes,
        "page": page,
        "pages": pages,
        "per_page": per_page,
        "count": count
    }
    return jsonify(result)

@app.route("/anime/count")
def count_anime():
    return jsonify(len(animes))

if __name__ == '__main__':
    app.run(debug=True)
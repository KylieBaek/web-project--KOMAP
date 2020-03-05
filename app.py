from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup
from operator import itemgetter
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbproject


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


# @app.route('/regionpage')
# def regionpage():
#      return render_template('region.html')


## 1. main page 지역 listing API
@app.route('/main', methods=['GET'])
def listing():
    regions = list(db.region.find({}, {'_id': 0}))
    sort_region = sorted(regions, key=itemgetter('visitcount', 'region_ko'))  # visitcount기준으로 오름차순정렬
    sort_region.reverse()
    for s in sort_region:
        print(s)
    return jsonify({'result': 'success', 'regions': sort_region})


# 2. 지역별 상세 page로 이동 API

@app.route('/region', methods=['GET'])
def regiondetail():
    region_receive = request.args.get('region_give')

    # locations = list(db.location.find({'region': region_receive}, {'_id': 0}))
    # sort_location = sorted(locations, key=itemgetter('visitcount', 'name'))  # visitcount기준으로 오름차순정렬
    # sort_location.reverse()
    #
    # for s in sort_location:
    #     print(s)

    # locations_data = json.dumps(sort_location, ensure_ascii=False)

    data = {'region': region_receive}
    return render_template('region.html', data=data)



@app.route('/region-locations', methods=['GET'])
def regiondetail_locations():
    region_receive = request.args.get('region_give')

    locations = list(db.location.find({'region': region_receive}, {'_id': 0}))
    sort_location = sorted(locations, key=itemgetter('visitcount', 'name'))  # visitcount기준으로 오름차순정렬
    sort_location.reverse()

    for s in sort_location:
        print(s)

    return jsonify({'result': 'success', 'region': region_receive, 'locations':sort_location})
#
# @app.route('/region',methods = ['GET'])
# def region_detail():
#     region_receive = request.args.get('region_give')
#     locations = list(db.location.find({'region': region_receive}, {'_id': 0}))
#     sort_location = sorted(locations, key=itemgetter('visitcount', 'name'))  # visitcount기준으로 오름차순정렬
#     sort_location.reverse()
#
#     for s in sort_location:
#         print(s)
#
#     return jsonify({'result': 'success', 'locations':sort_location})


if __name__ == '__main__':
    app.run('localhost', port=5000, debug=True)
# flask 서버 구축
from flask import Flask, request
from routes import register_routes

app = Flask(__name__)
register_routes(app)

#index
@app.route('/')
def index():
    return {"Hello" : "Flask!"}

#API
@app.route('/api/v1/feeds', methods = ['GET']) #GET /api/v1/feeds
def show_all_feeds():
    data = {'result' : 'success', 
            'data' : {'feed1': 'data1', 'feed2' : 'data2'}
            } #python의 Dict
    
    return data #Dict를 Jsonify해준다.

@app.route('/api/v1/feeds/<int:feed_id>', methods = ['GET'])
def show_one_feed(feed_id):
    data = {'result' : 'success', 'data' : f'feed ID : {feed_id}'}
    return data

@app.route('/api/v1/feeds', methods = ['POST'])
def create_feed():
    email = request.form['email']
    content = request.form['content']
    
    data = {'result' : 'success', 'data' : {'email':email, 'content' : content}}
    
    return data
    
#서버 실행
if __name__ == "__main__":
    app.run(debug = True)
    
    #마이크로 서비스 아키텍처(기능 하나당 서버 한개)
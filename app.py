from flask import Flask,render_template,request,redirect  #unable to import flask ctrl+shift+p python select interpreter base
from collections import defaultdict
from uuid import uuid4
from db import VoteDB

app=Flask(__name__)
db=VoteDB()

#topics = dict({
#    'abc123':{ #topicid,key
#        'name':'Hotel for holiday',
#        'data': {
#          'Hotel A':0,
#            'Hotel B':1
#        }
#    },
#})

@app.route('/')
def index():
    topics = db.gettopicnames()
    print(topics)
    return render_template("index.html",topic=topics)

#@app.route('/addTopic',methods=["POST"])
#def add_new_topic():
    topic_id=str(uuid4())
    name=request.form.get('name')
    topics[topic_id]={
        'name':name,
        'data': defaultdict(int)
    }
    #print(topic_id,name)
    return redirect('/')

@app.route('/addTopic',methods=["POST"])
def add_new_topic():
    name = request.form.get('name')
    db.add_topic(topic_name=name)
    return redirect('/')


@app.route('/newtopic')
def new_topic():
    return render_template('newtopic.html')

#@app.route('/topic/<topic_id>',methods=['GET']) #get respondข้อมูลให้ html by return html=server
#def get_topic_page(topic_id):
    #topic_data = topics[topic_id]
    #print(topic_data)
    #return render_template('topic.html',topic_id=topic_id,topic=topic_data)

@app.route('/topic/<topic_id>',methods=['GET']) #get respondข้อมูลให้ html by return html=server
def get_topic_page(topic_id):
    topic_data,topic_name = db.get_topic(topic_id)
    print(topic_data)
    return render_template('topic.html',topic_id=topic_id,topic=topic_data,topic_name=topic_name)

#@app.route('/topic/<topic_id>/newChoice',methods=["POST"]) #post getข้อมูลจาก html มาให้ server ผ่านname
#def new_choice(topic_id):
#    choice_name = request.form.get('choice_name')
#    topics[topic_id]['data'][choice_name]=0
#    print(topics)
#    return redirect(f'/topic/{topic_id}')

@app.route('/topic/<topic_id>/newChoice',methods=["POST"]) #post getข้อมูลจาก html มาให้ server ผ่านname
def new_choice(topic_id):
    choice_name = request.form.get('choice_name')
    db.add_choice(choice_name=choice_name,topic_id=topic_id) #ส่งค่าให้ function addchoiceในdb db=py
    return redirect(f'/topic/{topic_id}')

#@app.route('/topic/<topic_id>/vote',methods=["POST"])
#def vote_topic(topic_id):
    #choice_name = request.form.get('choice_name')
    #topics[topic_id]['data'][choice_name] += 1
    #return redirect(f'/topic/{topic_id}')

@app.route('/topic/<topic_id>/vote',methods=["POST"])
def vote_topic(topic_id):
    choice_id = request.form.get('choice')
    db.vote(choice_id=choice_id,topic_id=topic_id)
    return redirect(f'/topic/{topic_id}')


#if __name__ == "__main__":   #สั่ง start server
#    app.run(debug=True)
#    app.run(host="0.0.0.0",port=5000)
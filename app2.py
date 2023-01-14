from flask import Flask,render_template,request,redirect  #unable to import flask ctrl+shift+p python select interpreter base
from collections import defaultdict
from uuid import uuid4
from model import db,Votes,Topics

app=Flask(__name__)

@app.route('/')
def index():
    topics = list(Topics.select())
    #print(topics)
    return render_template("index.html",topics=topics)

@app.route('/addTopic',methods=["POST"])
def add_new_topic():
    topic_id=str(uuid4())
    name=request.form.get('name')
    Topics.create(id=topic_id,name=name)
    return redirect('/')

@app.route('/newtopic')
def new_topic():
    return render_template('newtopic.html')


@app.route('/topic/<topic_id>',methods=['GET']) #get respondข้อมูลให้ html by return html=server
def get_topic_page(topic_id):
    topic= list(Topics.select().where(Topics.id == topic_id))
    print(topic)
    votes=list(Votes.select().where(Votes.topic == topic[0]))
    return render_template('topic.html',topic_id=topic_id,topic=topic[0],votes=votes)

@app.route('/topic/<topic_id>/newChoice',methods=["POST"]) #post getข้อมูลจาก html มาให้ server ผ่านname
def new_choice(topic_id):
    cname = request.form.get('choice_name')
    Votes.create(topic=Topics.get_by_id(topic_id),choice_name=cname)
    return redirect(f'/topic/{topic_id}')

@app.route('/topic/<topic_id>/vote',methods=["POST"])
def vote_topic(topic_id):
    choice_id = request.form.get('choice')
    query=Votes.update(choice_count=Votes.choice_count+1).where(Votes.id==choice_id)
    query.execute()
    return redirect(f'/topic/{topic_id}')


if __name__ == "__main__": 
    db.connect()
    db.create_tables([Topics,Votes])
    app.run(debug=True)
    app.run(host="0.0.0.0",port=5000)
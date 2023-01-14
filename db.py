import sqlite3
from uuid import uuid4

class VoteDB:
    def __init__(self):
        self.conn = sqlite3.connect('vote.db',check_same_thread=False) #connect
        self.create_table() #run function

    def create_table(self):  #สร้าง table
        create_topic_query = """
        CREATE TABLE IF NOT EXISTS Topics(
            id VARCHAR(64) primary key not null,
            name varchar(50) not null
        );
        """
        create_vote_query = """
        CREATE TABLE IF NOT EXISTS Votes(
            id INTEGER primary key AUTOINCREMENT not null,
            topic VARCHAR(64),
            choice_name VARCHAR(50),
            choice_count INT,
            FOREIGN KEY(topic) REFERENCES Topics(id)
        );
        """
        self.conn.execute(create_topic_query) #run คำสั่ง
        self.conn.execute(create_vote_query)
        self.conn.commit() #save

    def add_topic(self, topic_name): #add values in table
        topic_id = str(uuid4())
        query = """
        INSERT INTO Topics (
            id,name
        ) VALUES (
             ?,?
        )"""                    
        #?ใช้ป้องกันการhack db
        self.conn.execute(query, (topic_id,topic_name)) #ใส่ค่า?
        self.conn.commit()

    def gettopicnames(self): #อ่าน db ส่ง vote topic กลับ
        """
        [
            {
                "topic_id":str,
                "topic_name":str
            }
        ]
        """
        query= """
        SELECT * FROM Topics
        """
        result = self.conn.execute(query)
        ret = []
        for data in result:
            print(data)
            ret.append({
                "topic_id":data[0],
                "topic_name":data[1]
            })
        return ret
    
    def get_topic(self,topic_id):
        """
        (
            [
            (vote_id,choice_name,choice_count)
            ]
            ,
            topic_name
        )
        """
        topic_name_query = """
        SELECT name FROM Topics
        WHERE Topics.id = ?
        """
        topic_name_result = self.conn.execute(topic_name_query,(topic_id, )).fetchone() #ต้องการ result เดียว
        topic_name = topic_name_result[0]
        query = """
        SELECT id,choice_name,choice_count
        FROM Votes v
        WHERE v.topic = ?
        """

        result = self.conn.execute(query,(topic_id, )) #tuple มี ,
        ret = []
        for data in result:
            cid,cname,ccount=data
            ret.append((cid , cname,ccount))
        return ret,topic_name

    def add_choice(self, choice_name,topic_id):
        query = """
        INSERT INTO Votes (topic,choice_name,choice_count)
        VALUES ( ?,?,?)
        """
        self.conn.execute(query,(topic_id,choice_name,0))
        self.conn.commit()
    
    def vote(self,choice_id,topic_id):
        query = """
        UPDATE Votes SET choice_count = choice_count + 1
        WHERE topic = ? and id = ?
        """

        self.conn.execute(query,(topic_id,choice_id))
        self.conn.commit()
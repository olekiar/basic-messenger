import flask
import mysql.connector
from flask import request, jsonify

app = flask.Flask(__name__)
db_connection = None

def create_database_connection():
    return mysql.connector.connect(user='system_user', password='qwerty',
                              host='localhost',
                              database='basic_messenger',
                              auth_plugin='mysql_native_password')

@app.route('/api/v1/message', methods=['POST'])
def create_message():
    data = {}
    if 'ConversationID' in request.form and 'SenderID' in request.form and 'Message' in request.form:
        with db_connection.cursor() as cursor:
            query = ("INSERT INTO Message (ConversationID, SenderID, Message) VALUES (%s, %s, %s)")
            cursor.execute(query, (int(request.form['ConversationID']),int(request.form['SenderID']), request.form['Message']))
            db_connection.commit()
        return jsonify(data)
    else:
        return jsonify(data), 400

@app.route('/api/v1/conversation', methods=['POST'])
def create_conversation():
    data = {}
    if 'UserID1' in request.headers and 'UserID2' in request.headers:
        with db_connection.cursor() as cursor:
            query = ("INSERT INTO Conversation (UserID1, UserID2) VALUES (%s, %s)")
            cursor.execute(query, (int(request.headers['UserID1']),int(request.headers['UserID2'])))
            db_connection.commit()
        return jsonify(data)
    else:
        return jsonify(data), 400

@app.route('/api/v1/conversations', methods=['GET'])
def get_conversations():
    data = []
    if 'UserID' in request.headers:
        with db_connection.cursor() as cursor:
            query = ("SELECT ConversationID, UserID2, CreatedDate FROM Conversation WHERE UserID1 = %s")
            cursor.execute(query, (int(request.headers['UserID']),))
            for (conversation_id, user_id, created_date) in cursor:
                entry = {}
                entry['ConversationID'] = conversation_id
                entry['FriendUserID'] = user_id
                entry['CreatedDate'] = created_date
                data.append(entry)
            query = ("SELECT ConversationID, UserID1, CreatedDate FROM Conversation WHERE UserID2 = %s")
            cursor.execute(query, (int(request.headers['UserID']),))
            for (conversation_id, user_id, created_date) in cursor:
                entry = {}
                entry['ConversationID'] = conversation_id
                entry['FriendUserID'] = user_id
                entry['CreatedDate'] = created_date
                data.append(entry)
        return jsonify(data)
    else:
        return jsonify(data), 400

@app.route('/api/v1/conversation', methods=['GET'])
def get_conversation():
    data = []
    if 'ConversationID' in request.headers:
        with db_connection.cursor() as cursor:
            query = ("SELECT MessageID, SenderID, Message, CreatedDate FROM Message WHERE ConversationID = %s")
            cursor.execute(query, (int(request.headers['ConversationID']),))
            for (message_id, sender_id, message, created_date) in cursor:
                entry = {}
                entry['MessageID'] = message_id
                entry['SenderID'] = sender_id
                entry['Message'] = message
                entry['CreatedDate'] = created_date
                data.append(entry)
        return jsonify(data)
    else:
        return jsonify(data), 400

@app.route('/api/v1/user', methods=['POST'])
def create_user():
    data = {}
    if 'UserName' in request.headers:
        with db_connection.cursor() as cursor:
            query = ("INSERT INTO User (UserName) VALUES (%s)")
            cursor.execute(query, (request.headers['UserName'],))
            db_connection.commit()
        return jsonify(data)
    else:
        return jsonify(data), 400

@app.route('/api/v1/user', methods=['GET'])
def get_user():
    data = {}
    if 'UserName' in request.headers:
        with db_connection.cursor() as cursor:
            query = ("SELECT UserID, UserName, CreatedDate FROM User WHERE UserName = %s")
            cursor.execute(query, (request.headers['UserName'],))
            for (user_id, user_name, created_date) in cursor:
                data['UserID'] = user_id
                data['UserName'] = user_name
                data['CreatedDate'] = created_date
        return jsonify(data)
    else:
        return jsonify(data), 400
    

if __name__ == "__main__":
    print(("* Flask starting server..."
        "please wait until server has fully started"))
    db_connection = create_database_connection()
    app.run()
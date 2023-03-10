# from flask import Flask, render_template, request
# import sqlite3

# app = Flask(__name__)

# # @app.route("/")
# # def hello_world():
# #    return "<h1>Hello World</h1>"  


# # @app.route("/ask/", methods=['POST', 'GET'])
# # def ask():
# #     if request.method == 'GET':
# #         # if the user just visits the url
# #         return render_template('ask.html')
# #     else:
# #         # if the user submits the form
# #         name = request.form['name']
# #         student = request.form['student']
# #         return render_template('ask.html', name=name, student=student)
    

# def get_message_db():
#    # check if there is database called message_db in g attribute in app
#    """
#    Creates the database of messages
#    Returns the database connection
#    """
#    try:
#       return g.message_db
#    except:
#       g.message_db = sqlite3.connect("messages_db.sqlite")
#       cmd = 'CREATE TABLE IF NOT EXISTS messages(id INT, handle TEXT, message TEXT)' # replace this with your SQL query
#       cursor = g.message_db.cursor()
#       cursor.execute(cmd)
#       return g.message_db
   
# def insert_message(request):
#    """
#    Inserts message into the database of messages
#    """
#    # ensure template creates these fields
#    # request.form["message"]
#    db = sqlite3.connect("get_message_db")
#    cmd = f"""
#       INSERT INTO messages (id, handle, message)
#       VALUES ('{request.form['id']}', '{request.form['handle']}', '{request.form['message']}')
#    """
#    # ensure id number of each message is unique
#    # id = 1 + current number of rows
#    cursor = db.cursor()
#    db.commit()
#    cursor.execude(cmd)

#    db.close()

# @app.route("/", methods=['POST', 'GET'])
# def ask():
#    if request.method == 'GET':
#       return render_template('submit.html')
#    else:
#       # thank user for submission
#       id = request.form['id']
#       handle = request.form['handle']
#       message = request.form['message']
#       insert_message(request)
#       return render_template('submit.html', id=id, handle=handle, message=message)


from flask import Flask, render_template, request
from flask import url_for, g
import sqlite3

app = Flask(__name__)

# @app.route("/") # decorators
# def main():
#    return render_template('submit.html')


@app.route("/", methods=['POST', 'GET'])
def ask():
   if request.method == 'GET':
      # if the user just visits the url
      return render_template('submit.html')
   else:
      # if the user submits the form
      message = request.form['message']
      handle = request.form['handle']
      insert_message(request)
      return render_template('submit.html', message=message, handle=handle)


def get_message_db():
   # check if there is database called message_db in g attribute in app
   """
   Creates the database of messages
   Returns the database connection
   """

   try:
      return g.message_db
   except:
      g.message_db = sqlite3.connect("messages_db.sqlite")
      cmd = 'CREATE TABLE IF NOT EXISTS messages(id INT, handle TEXT, message TEXT)'
      cursor = g.message_db.cursor()
      cursor.execute(cmd)
      return g.message_db
   
   
def insert_message(request):
   """
   Inserts message into the database of messages
   """

   # connect to database
   db = get_message_db()

   # compute id
   cursor = db.cursor()
   cmd = "SELECT count(*) FROM messages"
   id_num = 1 # + cursor.execute(cmd)
   cmd = f"""
      INSERT INTO messages
      VALUES ({id_num}, '{request.form['handle']}', '{request.form['message']}')
   """
   
   cursor.execute(cmd)
   db.commit()

   # close connection
   db.close()

def random_submissions(n):
   """
   Returns a collection of n random messages from the database
   """

   db = get_message_db()
   cursor = db.cursor()
   cmd = f"""
      SELECT *
      FROM messages
      ORDER BY RANDOM() LIMIT {n}
   """
   cursor.execute(cmd)
   m = cursor.fetchall()
   db.close()

   return m

@app.route('/view/')
def view():
   messages = random_submissions(2)
   return render_template('view.html', messages=messages)

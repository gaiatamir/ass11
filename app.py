from flask import Flask, redirect, url_for, render_template, flash, jsonify
from flask import request
from flask import session
import mysql.connector

app = Flask(__name__)
app.secret_key = '123'


def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         passwd='gaIa2112!',
                                         database='gaiaproject')
    cursor = connection.cursor(named_tuple=True)
    cursor.execute(query)

    if query_type == 'commit':
        connection.commit()
        return_value = True

    if query_type == 'fetch':
        query_result = cursor.fetchall()
        return_value = query_result

    connection.close()
    cursor.close()
    return return_value

@app.route('/')
@app.route('/assignment11/users')
def jasonUserslist():
    query= "select * from users"
    query_result = interact_db(query=query,query_type='fetch')
    if (len(query_result)==0):
        return jsonify({
            'success':'false',
            'elart':'no such user'
        })
    else:
        return jsonify({
            'success': 'true',
            'data':query_result
        })



@app.route('/assignment11/users/selected',defaults={'userID':1})
@app.route('/assignment11/users/selected/<int:userID>')
def jasonUser(userID):
    query= "select * from users where ID = '%s'" % userID
    query_result = interact_db(query=query,query_type='fetch')
    if (len(query_result)==0):
        return jsonify({
            'success':'false',
            'elart':'no such user'
        })
    else:
        return jsonify({
            'success': 'true',
            'data':{"id":query_result.name}
        })






@app.route('/assignment10', methods=['GET', 'POST'])
def assignment10():
    query = "select * from users"
    query_result = interact_db(query=query, query_type='fetch')
    return render_template('assignment10.html', users=query_result)


@app.route('/insert_user', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        Fname = request.form['name']
        lastName = request.form['lastname']
        id = request.form['id']
        query = "INSERT INTO users(ID,fname,lname) VALUES ('%s','%s','%s')" % (id, Fname, lastName)
        interact_db(query, 'commit')
        flash('New User Signed just Now')
    return redirect('assignment10')




@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        lastname = request.form['lastname']
        query = "UPDATE users SET fname= '%s' WHERE ID='%s'" % (name, id)
        query = "UPDATE users SET lname= '%s' WHERE ID='%s'" % (lastname, id)
        interact_db(query, 'commit')
        flash('User updat successfully!')
    return redirect('assignment10')



@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'GET':
        id = request.args['id']
        query = "DELETE FROM users WHERE ID='%s'" % id
        interact_db(query, 'commit')
        flash('user delet successfully')
    return redirect('assignment10')


from assignment10.assignment10 import assignment10
app.register_blueprint(assignment10)
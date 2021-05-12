from flask import Flask, request, render_template, jsonify, redirect, url_for
import mysql.connector
app = Flask(__name__)
app.config['MYSQL_USER'] = "task"
app.config['MYSQL-HOST'] = "localhost"
app.config['MYSQL_PASSWORD'] = "password123"
app.config['MYSQL-DB'] = 'nba'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mydb = mysql.connector.connect(host=app.config['MYSQL-HOST'] , database = app.config['MYSQL-DB'] ,user=app.config['MYSQL_USER'], password=app.config['MYSQL_PASSWORD'], auth_plugin='mysql_native_password')

@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('home.html')

@app.route('/get_player_data/',methods=['POST'])
def get_data():
	temp = request.form['name']
	other = temp.split(" ")
	firstname = other[0]
	lastname = other[1]
	second_message = request.form['Option']
	return redirect(url_for("multi", firstname = firstname, lastname = lastname, second_message = second_message))

@app.route('/<string:firstname>/<string:lastname>/<int:second_message>',methods=['GET'])
def multi(firstname, lastname, second_message):
	exists = False
	not_player = True
	name = firstname +" " + lastname
	mycursor = mydb.cursor(buffered=True) 
	if second_message == 1:
		mycursor.execute("select seasons_stats.Year from seasons_stats where player = \'" + name + "\'")
		if mycursor.rowcount == 0: 
			name += "*"
			mycursor.execute("select seasons_stats.Year from seasons_stats where player = \'" + name + "\'")
			if mycursor.rowcount == 0:
				not_player = False
			else:
				exists = True
		year = ""
		for row in mycursor:
			print(type(row))
			print(int(*row))
			prev_year = int(*row) - 1
			year += (str(prev_year) + "-" + str(*row) + " ")
		if exists == True:
			return jsonify({name[:-1]: year})
		else:
			if not_player == True:
				return jsonify({name: year})
			else:
				return jsonify({name[:-1]: "Not Available"})
	elif (second_message == 2):
		my_points = 0
		mycursor.execute("select seasons_stats.pts from seasons_stats where player = \'" + name + "\'")
		if mycursor.rowcount == 0: 
			name += "*"
			mycursor.execute("select seasons_stats.pts from seasons_stats where player = \'" + name + "\'")
			if mycursor.rowcount == 0:
				not_player = False
			else:
				exists = True
		for row in mycursor:	
			integer = str(*row)  # a tuble cannot be converted to a int but can with string so i covert it to string and then to int with int() function
			if (int(integer) > my_points):
				my_points = int(integer)
		if exists == True:
			return jsonify({"Most points in a season by " + name[:-1] : my_points})
		else:
			if not_player == True:	
				return jsonify({"Most points in a season by " + name: my_points})
			else: 
				return jsonify({name[:-1]: "Not Available"})
	elif (second_message == 4):
		line_count = 0
		team_list = []
		team = " "
		mycursor.execute("select seasons_stats.tm from seasons_stats where player = \'" + name + "\'")
		if mycursor.rowcount == 0: 
			name += "*"
			mycursor.execute("select seasons_stats.tm from seasons_stats where player = \'" + name + "\'")
			if mycursor.rowcount == 0:
				not_player = False
			else:
				exists = True
		for row in mycursor:
			if (line_count == 0):
				team_list.append(str(*row))
			else:
				if str(*row) not in team_list:
					team_list.append(str(*row))
				line_count += 1
		for t in team_list:
			team += " " + t
		if exists == True:
			return jsonify({"The team(s) " + name[:-1] + " has played for are/is": team})
		else:
			if not_player == True:
				return jsonify({"The team(s) " + name + " has played for are/is": team})
			else:
				return jsonify({name[:-1]: "Not Available"})


if __name__ == '__main__':
	app.run(debug=False)

    

from flask import Flask, render_template, request
from model import connect_to_db, db, State

app = Flask(__name__)



@app.route('/sample_state', methods=['GET'])
def render_state():
	state = db.session.query(State).first()
	return render_template("test.html", color_or_state=state.name)

# Below are several sample Flask routes to reference
@app.route('/test', methods=['GET'])
def print_test():
	html = "<html><body>Hello World 2</body></html>"
	return html

@app.route('/test2', methods=['GET'])
def print_test_2():
	strvar_to_insert = 'blue'
	return render_template("test.html", color_or_state=strvar_to_insert)

@app.route('/test3/<captured_arg>', methods=['GET'])
def print_captured_arg(captured_arg):
	print(captured_arg)
	return render_template("test.html", color_or_state=captured_arg)

################################################################################################
if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True)  # set to false before deploying

from flask import Flask, render_template, redirect, request
import EmotionalSupportAnimal as EMA
import time
import demo

app = Flask(__name__, static_folder='assets')

def dummy_func():
	time.sleep(5)
	return

@app.route("/")
def home():
	return redirect("/home")

@app.route("/Home_Good.html")
def home_good_template():
	return redirect("/home")

@app.route("/Home_Bad.html")
def home_bad_template():
	return redirect("/home")

@app.route("/home")
def home_template():
	BP = EMA.getBPM_BT()
	thres = int(demo.get_thresh())
	# If not having a breakdown
	if BP < thres:
		return render_template("Home_Good.html", BPM=BP, Thresh=thres)
	# If having breakdown
	else:
		return render_template("Home_Bad.html", BPM=BP, Thresh=thres)

@app.route("/Past.html")
def past_template():
	return render_template("Past.html")

@app.route("/Live.html", methods=['POST', 'GET'])
def live_template():
	# If trying to change the threshold
	if request.method==('POST'):
		new_thresh = request.form['new_treshold']
		demo.change_HR(new_thresh)
		print("threshold is now ", demo.get_thresh())
		return render_template("Live.html", Threshold=new_thresh)
	return render_template("Live.html", Threshold=demo.get_thresh())

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True, threaded=True)

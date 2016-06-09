from flask import Flask, render_template, send_from_directory
import util
import os
app = Flask(__name__)

app_path = os.path.dirname(os.path.realpath('__file__'))

@app.route('/fire_data')
def obtain_fire_data():
    # hard coded for now, to get the choose the input file
    output_file = app_path + '/static/data/output_test.csv'
    return util.fire_out_file_processing(output_file)

@app.route('/')
def index_page():
    return render_template("index.html")

@app.route('/display_veg')
def obtain_veg_data():
    # hard coded for now, to get the choose the input file
    output_file = app_path + '/static/data/veg_data.csv'
    return util.veg_out_file_processing(output_file)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
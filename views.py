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

@app.route('/api/fire_data/metadata')
def obtain_fire_meta_data():
    # hard coded for now, to get the choose the input file
    output_file = app_path + '/static/data/output_test.csv'
    return util.get_fire_meta_data(output_file)

@app.route('/api/fire_frame_data/<start>/<end>')
def obtain_fire_frame_data(start='',end=''):
    # hard coded for now, to get the choose the input file
    output_file = app_path + '/static/data/output_test.csv'
    return util.get_fire_data_by_timestep(output_file,int(start),int(end))

@app.route('/')
def index_page():
    return render_template("index.html")

# @app.route('/api/onfire_cell_json/<timestep>')
# def api_onfire_json():
# 	'''
# 	this is an api to return onfire cell
# 	the json format is like this
# 	{'onfire':[[col0,row0],[col1,row1],[col2,row2]...]}
# 	'''
#     return render_template("index.html")    

@app.route('/display_veg')
def obtain_veg_data():
    # hard coded for now, to get the choose the input file
    output_file = app_path + '/static/data/veg_data.csv'
    return util.veg_out_file_processing(output_file)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
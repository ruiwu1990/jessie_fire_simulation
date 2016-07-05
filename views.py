from flask import Flask, render_template, send_from_directory, request
import util
import os
app = Flask(__name__)

app_path = os.path.dirname(os.path.realpath('__file__'))

@app.route('/api/veg_data')
def obtain_veg_data():
    # hard coded for now, to get the choose the input file
    output_file = app_path + '/static/data/veg_data.csv'
    # also I should get a fnuction to get output data col and row num
    return util.veg_out_file_processing(output_file,642,906)

@app.route('/api/fire_data')
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

@app.route('/api/update_veg_file', methods=['POST'])
def update_veg_file_post():
    '''
    This function update the veg file and rerun the model
    with the updated info
    '''
    veg_meta = request.json['veg_meta']
    veg_2D_grid = request.json['veg_2D_grid']

    # TODO hard coded file name and location here
    output_file = app_path + '/static/data/test_veg_output.csv'

    util.update_veg_file(output_file,veg_meta,veg_2D_grid)

    # TODO add the model run part
    return 'success'

@app.route('/api/get_update_veg')
def get_update_veg():
    # hard coded for now, to get the choose the input file
    filename = 'test_veg_output.csv'
    folder = app_path + '/static/data/'
    return send_from_directory(folder,filename)


@app.route('/')
def index_page():
    # hard coded for now, to get the choose the input file
    output_file = app_path + '/static/data/veg_data.csv'
    a,veg_option,c = util.get_veg_types(output_file)
    return render_template("index.html",veg_option=veg_option)

# @app.route('/api/onfire_cell_json/<timestep>')
# def api_onfire_json():
# 	'''
# 	this is an api to return onfire cell
# 	the json format is like this
# 	{'onfire':[[col0,row0],[col1,row1],[col2,row2]...]}
# 	'''
#     return render_template("index.html")    


@app.route('/upload')
def upload_file_page():
    '''
    use this function to display upload html page
    '''
    return render_template("upload_input_file.html")

@app.route('/upload_process', methods=['POST'])
def upload_file_process():
    '''
    use this function to process upload files
    '''
    # TODO check file extension
    file1 = request.files['file1']
    file2 = request.files['file2']
    app_root = os.path.dirname(os.path.abspath(__file__))
    data_folder = app_root + '/static/data'
    #file_full_path = data_folder + '/temp_upload_data'
    file_full_path1 = data_folder + '/temp_upload_data1'
    file_full_path2 = data_folder + '/temp_upload_data2'
    #file.save(file_full_path)
    file1.save(file_full_path1)
    file2.save(file_full_path2)
    return render_template("index.html")

@app.route('/api/update_fire_info', methods=['POST'])
def update_fire_info():
    '''
    this function receives the updated the fire information
    and creates a new input files for the fire simulation lib
    '''
    fire_info_arr = request.json['fire_info_arr']
    num_cols = request.json['num_cols']
    num_rows = request.json['num_rows']

    fire_file = app_path + '/static/data/fire_info.csv'
    # TODO add all metadata into this function param part
    util.update_onfire_file(fire_file, fire_info_arr)

    return 'success'

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
from flask import Flask, render_template, send_from_directory, request
import util
import os
import shutil
import time
app = Flask(__name__)

app_path = os.path.dirname(os.path.abspath(__file__))

@app.route('/api/veg_data')
def obtain_veg_data():
    # start////////
    output_file = app_path + '/static/data/temp_upload_fuel'
    # also I should get a fnuction to get output data col and row num
    return util.veg_out_file_processing(output_file,642,906)

@app.route('/api/fire_data')
def obtain_fire_data():
    # replace veg with the original one
    temp_data_folder = app_path + '/../firesim/data/'
    shutil.move(temp_data_folder+'origin_fixed.fuel',temp_data_folder+'fixed.fuel')
    shutil.copy(temp_data_folder+'fixed.fuel',temp_data_folder+'origin_fixed.fuel')

    output_file = app_path + '/../firesim/out/final_tests.csv'

    return util.fire_out_file_processing(output_file)

@app.route('/api/fire_data/metadata')
def obtain_fire_meta_data():
    output_file = app_path + '/static/data/temp_final_tests.csv'
    return util.get_fire_meta_data(output_file)

@app.route('/api/fire_frame_data/<start>/<end>')
def obtain_fire_frame_data(start='',end=''):
    output_file = app_path + '/static/data/temp_final_tests.csv'
    return util.get_fire_data_by_timestep(output_file,int(start),int(end))

@app.route('/api/update_veg_file', methods=['POST','GET'])
def update_veg_file_post():
    '''
    This function update the veg file and rerun the model
    with the updated info
    '''
    if request.method == 'POST':
        veg_meta = request.json['veg_meta']
        veg_2D_grid = request.json['veg_2D_grid']

        # TODO hard coded file name and location here
        # output_file = app_path + '/static/data/test_veg_output.csv'
        # this will be replaced by argv[]
        output_file = app_path + '/static/data/temp_upload_fuel'

        util.update_veg_file(output_file,veg_meta,veg_2D_grid)

        util.exec_model()
        return 'success'

    elif request.method == 'GET':
        # this is where I store the results
        output_file = app_path + '/static/data/temp_final_tests.csv'

        return util.fire_out_file_processing(output_file)



@app.route('/api/get_update_veg')
def get_update_veg():
    # hard coded for now, to get the choose the input file
    filename = 'test_veg_output.csv'
    folder = app_path + '/static/data/'
    return send_from_directory(folder,filename)


@app.route('/fire_vis/<folder_name>')
def fire_vis_func(folder_name=''):
    temp_folder = app_path + '/static/data/existing/' + folder_name;
    shutil.move(temp_folder+'/temp_upload_fuel',temp_folder+'/../../temp_upload_fuel')
    shutil.copy(temp_folder+'/../../temp_upload_fuel',temp_folder+'/temp_upload_fuel')

    shutil.move(temp_folder+'/temp_upload_onfire',temp_folder+'/../../temp_upload_onfire')
    shutil.copy(temp_folder+'/../../temp_upload_onfire',temp_folder+'/temp_upload_onfire')

    veg_file = app_path + '/static/data/temp_upload_fuel'
    a,veg_option,c = util.get_veg_types(veg_file)

    util.exec_model()
    return render_template("fire_vis.html",veg_option=veg_option)
  

@app.route('/upload')
def upload_file_page():
    '''
    use this function to display upload html page
    '''
    existing_folder = app_path + '/static/data/existing'
    dataset_name_list = os.listdir(existing_folder)
    return render_template("upload_input_file.html", dataset_name_list=dataset_name_list)

@app.route('/upload_process', methods=['POST'])
def upload_file_process():
    '''
    use this function to process upload files
    '''
    # TODO check file extension
    file1 = request.files['file1']
    file2 = request.files['file2']

    data_folder = app_path + '/static/data'
    #file_full_path = data_folder + '/temp_upload_data'
    file_full_path1 = data_folder + '/temp_upload_fuel'
    file_full_path2 = data_folder + '/temp_upload_onfire'
    #file.save(file_full_path)
    file1.save(file_full_path1)
    file2.save(file_full_path2)
    # do the process and exec here
    a,veg_option,c = util.get_veg_types(file_full_path1)
    util.exec_model()
    return render_template("fire_vis.html",veg_option=veg_option)

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
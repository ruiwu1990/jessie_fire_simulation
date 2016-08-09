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
    # # replace veg with the original one
    # temp_data_folder = app_path + '/../firesim/data/'
    # shutil.move(temp_data_folder+'origin_fixed.fuel',temp_data_folder+'fixed.fuel')
    # shutil.copy(temp_data_folder+'fixed.fuel',temp_data_folder+'origin_fixed.fuel')

    data_folder = app_path + '/static/data'
    output_file = data_folder+'/temp_final_tests.csv'

    return util.fire_out_file_processing(output_file)

@app.route('/api/wind_data')
def obtain_wind_data():
    '''
    this function is used to get the wind data
    '''
    data_folder = app_path + '/static/data'
    wind_x_file = data_folder+'/temp_windx.fuel'
    wind_y_file = data_folder+'/temp_windy.fuel'

    return util.wind_file_processing(wind_x_file,wind_y_file)

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

        output_file = app_path + '/static/data/temp_upload_fuel'

        util.update_veg_file(output_file,veg_meta,veg_2D_grid)

        util.exec_model()
        return 'success'

    elif request.method == 'GET':
        # this is where I store the results
        output_file = app_path + '/static/data/temp_final_tests.csv'

        return util.fire_out_file_processing(output_file)


@app.route('/fire_vis_modified')
def rerun_fire_sim_with_modification():
    util.exec_model()
    return render_template("fire_vis.html")

@app.route('/api/update_fire_file', methods=['POST','GET'])
def update_fire_file_post():
    '''
    This function update the fire file and rerun the model
    with the updated info
    '''
    if request.method == 'POST':
        fire_2D_grid = request.json['fire_2D_grid']

        output_file = app_path + '/static/data/temp_upload_onfire'

        util.update_on_fire_file(output_file,fire_2D_grid)

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

@app.route('/api/update_wind',methods=['POST'])
def post_update_veg():
    # hard coded for now, to get the choose the input file
    wind_x = 'temp_windx.fuel'
    wind_y = 'temp_windy.fuel'
    folder = app_path + '/static/data/'
    wind_x_data = request.json['wind_x_data']
    wind_y_data = request.json['wind_y_data']
    util.update_wind_file(folder+wind_x,folder+wind_y,wind_x_data,wind_y_data)
    return 'success'


@app.route('/fire_vis/<folder_name>')
def fire_vis_func(folder_name=''):
    temp_folder = app_path + '/static/data/existing/' + folder_name;
    shutil.move(temp_folder+'/temp_upload_fuel',temp_folder+'/../../temp_upload_fuel')
    shutil.copy(temp_folder+'/../../temp_upload_fuel',temp_folder+'/temp_upload_fuel')

    shutil.move(temp_folder+'/temp_upload_onfire',temp_folder+'/../../temp_upload_onfire')
    shutil.copy(temp_folder+'/../../temp_upload_onfire',temp_folder+'/temp_upload_onfire')

    shutil.move(temp_folder+'/temp_windx.fuel',temp_folder+'/../../temp_windx.fuel')
    shutil.copy(temp_folder+'/../../temp_windx.fuel',temp_folder+'/temp_windx.fuel')

    shutil.move(temp_folder+'/temp_windy.fuel',temp_folder+'/../../temp_windy.fuel')
    shutil.copy(temp_folder+'/../../temp_windy.fuel',temp_folder+'/temp_windy.fuel')

    veg_file = app_path + '/static/data/temp_upload_fuel'
    a,veg_option,c = util.get_veg_types(veg_file)

    util.exec_model()
    return render_template("fire_vis.html")
  


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
    file3 = request.files['file3']
    file4 = request.files['file4']

    data_folder = app_path + '/static/data'
    #file_full_path = data_folder + '/temp_upload_data'
    file_full_path1 = data_folder + '/temp_upload_fuel'
    file_full_path2 = data_folder + '/temp_upload_onfire'
    file_full_path3 = data_folder + '/temp_windx.fuel'
    file_full_path4 = data_folder + '/temp_windy.fuel'
    #file.save(file_full_path)
    file1.save(file_full_path1)
    file2.save(file_full_path2)
    file3.save(file_full_path3)
    file4.save(file_full_path4)
    # do the process and exec here
    a,veg_option,c = util.get_veg_types(file_full_path1)
    util.exec_model()
    return render_template("fire_vis.html",veg_option=veg_option)

@app.route('/upload_scenario', methods=['POST'])
def upload_scenario_process():
    '''
    this function is used to process the upload scenario zip
    '''
    file1 = 'temp_windx.fuel'
    file2 = 'temp_windy.fuel'
    file3 = 'temp_upload_fuel'
    file4 = 'temp_upload_onfire'
    file_list = [file1,file2,file3,file4]
    # save scenario zip file
    scenario_file = request.files['scenario_file']
    data_folder = app_path + '/static/data'
    scenario_file_name = 'scenario_zip'
    scenario_file_path = data_folder + '/' + scenario_file_name
    scenario_file.save(scenario_file_path)
    # extract files from zip file
    util.process_scenario_file(file_list,scenario_file_name)
    # do the process and exec here
    veg_file = app_path + '/static/data/temp_upload_fuel'
    a,veg_option,c = util.get_veg_types(veg_file)
    util.exec_model()
    return render_template("fire_vis.html",veg_option=veg_option)

@app.route('/api/scenario_zip')
def download_scenario_zip():
    scenario_file = 'scenario_zip'
    
    file1 = 'temp_windx.fuel'
    file2 = 'temp_windy.fuel'
    file3 = 'temp_upload_fuel'
    file4 = 'temp_upload_onfire'
    file_list = [file1,file2,file3,file4]
    util.download_scenario_file(file_list,scenario_file)
    folder = app_path + '/static/data/'
    return send_from_directory(directory=folder, filename=scenario_file)

@app.route('/upload_files', methods=['POST'])
def upload_fire_file():
    '''
    use this function to process upload files
    '''
    # TODO check file extension
    file1 = request.files['file1']
    file2 = request.files['file2']
    file3 = request.files['file3']
    file4 = request.files['file4']

    data_folder = app_path + '/static/data'
    #file_full_path = data_folder + '/temp_upload_data'
    file_full_path1 = data_folder + '/temp_upload_fuel'
    file_full_path2 = data_folder + '/temp_upload_onfire'
    file_full_path3 = data_folder + '/temp_windx.fuel'
    file_full_path4 = data_folder + '/temp_windy.fuel'
    #file.save(file_full_path)
    file1.save(file_full_path1)
    file2.save(file_full_path2)
    file3.save(file_full_path3)
    file4.save(file_full_path4)

    return 'success'

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

@app.route('/api/get_final_results', methods=['GET'])
def get_fire_results():
    '''
    this function is used to get the final fire results
    '''
    filename = 'temp_final_tests.csv'
    folder = app_path + '/static/data/'
    util.exec_model()
    return send_from_directory(directory=folder, filename=filename)

@app.route('/api/get_log', methods=['GET'])
def get_log():
    filename = 'log.txt'
    folder = app_path + '/'
    return send_from_directory(directory=app_path, filename=filename)

@app.route('/api/get_err_log', methods=['GET'])
def get_err_log():
    filename = 'err_log.txt'
    folder = app_path + '/'
    return send_from_directory(directory=app_path, filename=filename)

@app.route('/wind_modification')
def modify_wind():
    return render_template('modify_wind.html')

@app.route('/veg_modification')
def modify_veg():
    veg_file = app_path + '/static/data/temp_upload_fuel'
    a,veg_option,c = util.get_veg_types(veg_file)

    return render_template("modify_veg.html",veg_option=veg_option,veg_total_num=len(veg_option))

@app.route('/api/get_veg_info')
def veg_info():
    return util.json_veg_info()

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
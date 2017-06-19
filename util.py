import json
import math
import subprocess
import os
import sys
import zipfile



# this function process the input csv file and generate json file
def fire_out_file_processing(fire_out_file):
    # I am kind of hard coded here to grab meta data
    # without using pandas, coz jessie file is not quit csv style
    fp = open(fire_out_file)
    # get let top lat, and remove \n in the end of string
    let_top_lat = fp.readline().strip().split(':')[1]
    # get other metadata
    left_top_long = fp.readline().strip().split(':')[1]
    right_bottom_lat = fp.readline().strip().split(':')[1]
    right_bottom_long = fp.readline().strip().split(':')[1]
    num_rows = fp.readline().strip().split(':')[1]
    num_cols = fp.readline().strip().split(':')[1]
    max_val = fp.readline().strip().split(':')[1]
    notsetfire_val = fp.readline().strip().split(':')[1]

    fire_data = []
    for line in fp:
        temp_list = line.strip().split(',')
        # need to pop the last element, coz each row of the output file 
        # is like this '...,', so the last element will be '' after split(',')
        temp_list.pop()
        fire_data.append(temp_list)

    json_dict = {'let_top_lat':let_top_lat,\
                 'left_top_long':left_top_long,\
                 'right_bottom_lat':right_bottom_lat,\
                 'right_bottom_long':right_bottom_long,\
                 'num_rows':num_rows,\
                 'num_cols':num_cols,\
                 'max_val':max_val,\
                 'notsetfire_val':notsetfire_val,\
                 'fire_data':fire_data}
    fp.close()
    return json.dumps(json_dict)


def wind_file_processing(wind_x_file,wind_y_file):
    '''
    this function process the input csv file and generate json file
    '''
    # I am kind of hard coded here to grab meta data
    # without using pandas, coz jessie file is not quit csv style
    a,unique_x = wind_file_process(wind_x_file)
    a,unique_y = wind_file_process(wind_y_file)
    fp1 = open(wind_x_file)
    fp2 = open(wind_y_file)
    
    num_cols = fp1.readline().strip().split(' ')[-1]
    num_rows = fp1.readline().strip().split(' ')[-1]
    let_top_lat = fp1.readline().strip().split(' ')[-1]
    left_top_long = fp1.readline().strip().split(' ')[-1]
    cell_size = fp1.readline().strip().split(' ')[-1]
    no_data_value = fp1.readline().strip().split(' ')[-1]
    
    wind_data_x = []
    for line in fp1:
        
        temp_list = line.strip().split(' ')
        # do this coz the last line can be empty
        if temp_list != ['']:
            temp_list = [int(i) for i in temp_list]
        wind_data_x.append(temp_list)

    # still hard coded here to get rid of the meta data
    num_cols = fp2.readline().strip().split(' ')[-1]
    num_rows = fp2.readline().strip().split(' ')[-1]
    let_top_lat = fp2.readline().strip().split(' ')[-1]
    left_top_long = fp2.readline().strip().split(' ')[-1]
    cell_size = fp2.readline().strip().split(' ')[-1]
    no_data_value = fp2.readline().strip().split(' ')[-1]
    
    wind_data_y = []
    for line in fp2:
        temp_list = line.strip().split(' ')
        # do this coz the last line can be empty
        if temp_list != ['']:
            temp_list = [int(i) for i in temp_list]
        wind_data_y.append(temp_list)

    json_dict = {'let_top_lat':let_top_lat,\
                 'left_top_long':left_top_long,\
                 'num_rows':num_rows,\
                 'num_cols':num_cols,\
                 'cell_size':cell_size,\
                 'no_data_value':no_data_value,\
                 'wind_data_x':wind_data_x,\
                 'wind_data_y':wind_data_y,\
                 'unique_x':unique_x,\
                 'unique_y':unique_y}
    fp1.close()
    fp2.close()
    return json.dumps(json_dict)

def generate_onfire_cell(aim_file, base_file):
    '''
    this function returns a file contains 2D on fire cells
    '''
    # less or equal this time tick is on fire
    time_tick = 710
    fp1 = open(base_file)
    fp2 = open(aim_file,'w')
    # I am hard coded here
    # the metadata has 8 lines
    for i in range(8):
        fp2.write(fp1.readline())
    # rewrite fp2 based on f1 values
    for line in fp1:
        temp_list = line.strip().split(',')
        # need to pop the last element, coz each row of the output file 
        # is like this '...,', so the last element will be '' after split(',')
        temp_list.pop()
        for m in range(len(temp_list)):
            if int(temp_list[m]) == time_tick:
                temp_list[m] = '1'
            else:
                temp_list[m] = '0'
        fp2.write(','.join(temp_list))
    fp1.close()
    fp2.close()
    return 'success'

def get_fire_meta_data(fire_out_file):
    '''
    this function returns the meta data
    '''
    # I am kind of hard coded here to grab meta data
    # without using pandas, coz jessie file is not quit csv style
    fp = open(fire_out_file)
    # get let top lat, and remove \n in the end of string
    let_top_lat = fp.readline().strip().split(':')[1]
    # get other metadata
    left_top_long = fp.readline().strip().split(':')[1]
    right_bottom_lat = fp.readline().strip().split(':')[1]
    right_bottom_long = fp.readline().strip().split(':')[1]
    num_rows = fp.readline().strip().split(':')[1]
    num_cols = fp.readline().strip().split(':')[1]
    max_val = fp.readline().strip().split(':')[1]
    notsetfire_val = fp.readline().strip().split(':')[1]

    json_dict = {'let_top_lat':let_top_lat,\
                 'left_top_long':left_top_long,\
                 'right_bottom_lat':right_bottom_lat,\
                 'right_bottom_long':right_bottom_long,\
                 'num_rows':num_rows,\
                 'num_cols':num_cols,\
                 'max_val':max_val,\
                 'notsetfire_val':notsetfire_val}
    fp.close()
    return json.dumps(json_dict)

def get_fire_data_by_timestep(fire_out_file,start_time,end_time):
    '''
    start_time and end_time should be int
    '''
    if start_time > end_time:
        return json.dumps({'error':'start is bigger then end time'})
    fp = open(fire_out_file)
    # get let top lat, and remove \n in the end of string
    let_top_lat = fp.readline().strip().split(':')[1]
    # get other metadata
    left_top_long = fp.readline().strip().split(':')[1]
    right_bottom_lat = fp.readline().strip().split(':')[1]
    right_bottom_long = fp.readline().strip().split(':')[1]
    num_rows = fp.readline().strip().split(':')[1]
    num_cols = fp.readline().strip().split(':')[1]
    max_val = fp.readline().strip().split(':')[1]
    notsetfire_val = fp.readline().strip().split(':')[1]
    fire_data = [[[]]*int(num_rows)]*(end_time-start_time+1)
    count = 0
    for line in fp:
        # doing this coz andy's program generates strange file, each line, ends with ,
        temp_bad_list = line.strip().split(',')
        # remove the final element ''
        temp_bad_list.pop()
        temp_list = map(int,temp_bad_list)
        
        for i in range(len(fire_data)):
            temp_item = []
            for m in temp_list:
                if m < start_time:
                    # -1 means before start, on fire
                    temp_item.append(-1)
                elif m<=(i+start_time):
                    # 1 means on fire
                    temp_item.append(1)
                else:
                    # 0  means not on fire
                    temp_item.append(0)            
            #fire_data[i].append(temp_item)
            fire_data[i][count] = temp_item
        count = count + 1
    json_dict = {'fire_data':fire_data}
    fp.close()
    return json.dumps(json_dict)

def update_onfire_file(fire_file, fire_arr):
    '''
    this function is used to
    update the current on fire file
    '''

    fp = open(fire_file,'w')
    # TODO redo this part, metadata should from the function param
    fp.write('left_top_lat:61.8819050\n')
    fp.write('left_top_long:40.17204368\n')
    fp.write('right_bottom_lat:62.7417377\n')
    fp.write('right_bottom_long:40.11111514\n')
    fp.write('numrows:642\n')
    fp.write('numcols:906\n')
    fp.write('lmaxval:1862\n')
    fp.write('notsetfire:32767\n')

    # update fire array of the file
    for i in fire_arr:
        fp.write(','.join(i)+'\n')

    fp.close()
    return 'success'

def update_veg_file(veg_file,meta_data,veg_2D_grid):
    fp = open(veg_file, 'wb')
    # write meta data
    for item in meta_data:
        item.append('\n')
        fp.write(' '.join(item))

    for item in veg_2D_grid:
        line = [str(i) for i in item]
        line.append('\n')
        fp.write(' '.join(line))

    fp.close()

def fit_high_resolution_into_low(high_rows,high_cols,low_rows,low_cols,cur_row,cur_col):
    '''
    this function is used to change high resolution into low
    (len/high_cols)*aim_col = (len/low_cols)*cur_col =>aim_col = (high_cols*cur_col)/low_cols
    '''
    # aim_col will be int since low_cols, cur_col, and high_cols are ints
    # aim_col = (high_cols*cur_col)/low_cols
    # aim_row = (high_rows*cur_row)/low_rows
    aim_col = int(round(float(low_cols*cur_col)/high_cols))
    aim_row = int(round(float(low_rows*cur_row)/high_rows))
    return aim_row,aim_col

def update_wind_file(wind_x_file,wind_y_file,wind_x_data,wind_y_data):
    '''
    this function is used to update wind file
    '''
    fp_x = open(wind_x_file,'wb')
    fp_y = open(wind_y_file,'wb')
    # hard coded write meta data into file
    fp_x.write('ncols        287\n')
    fp_x.write('nrows        203\n')
    fp_x.write('xllcorner    618828.217566499952\n')
    fp_x.write('yllcorner    4011107.642806999851\n')
    fp_x.write('cellsize     30.000000000000\n')
    fp_x.write('NODATA_value  -9999\n')

    fp_y.write('ncols        287\n')
    fp_y.write('nrows        203\n')
    fp_y.write('xllcorner    618828.217566499952\n')
    fp_y.write('yllcorner    4011107.642806999851\n')
    fp_y.write('cellsize     30.000000000000\n')
    fp_y.write('NODATA_value  -9999\n')

    for line in wind_x_data:
        temp_list = [str(i) for i in line]
        fp_x.write(' '.join(temp_list)+'\n')

    for line in wind_y_data:
        temp_list = [str(i) for i in line]
        fp_y.write(' '.join(temp_list)+'\n')

    fp_x.close()
    fp_y.close()

def update_on_fire_file(fire_file,fire_2D_grid):
    fp = open(fire_file, 'wb')
    # write meta data
    # I hard coded here to write metadata
    fp.write('left_top_lat:61.8819050\n')
    fp.write('left_top_long:40.17204368\n')
    fp.write('right_bottom_lat:62.7417377\n')
    fp.write('right_bottom_long:40.11111514\n')
    fp.write('numrows:642\n')
    fp.write('numcols:906\n')
    fp.write('lmaxval:1862\n')
    fp.write('notsetfire:32767\n')
    # this part is also hard coded, should be extracted from files or as inputs
    dem_rows = 642
    dem_cols = 906
    veg_rows = 203
    veg_cols = 287

    # cannot use this final_fire_2D_grid = [[0]*dem_cols]*dem_rows, coz it will cauze a[0][0]=1 then all the a[0][_] will be 1
    final_fire_2D_grid = [[0]*dem_cols for _ in range(dem_rows)]

    # for r in range(dem_rows):
    #     for c in range(dem_cols):
    #         temp_row, temp_col = fit_high_resolution_into_low(dem_rows,dem_cols,veg_rows,veg_cols,r,c)
    #         # if the cell is 2 set fire by users
    #         if int(fire_2D_grid[temp_row][temp_col]) == 2:
    #             print 'row is:'+str(r)+'; col is:'+str(c)+'; temp_row is:'+str(temp_row)+'; temp_col is:'+str(temp_col)
    #             final_fire_2D_grid[r][c] = 1

    count = 0
    count1 = 0
    for row in range(veg_rows):
        for col in range(veg_cols):
            if int(fire_2D_grid[row][col]) == 2:
                count = count + 1
                for r in range(dem_rows):
                    for c in range(dem_cols):
                        temp_row, temp_col = fit_high_resolution_into_low(dem_rows,dem_cols,veg_rows,veg_cols,r,c)
                        # if the cell is 2 set fire by users
                        if temp_row==row and temp_col==col:
                            print 'row is:'+str(r)+'; col is:'+str(c)+'; temp_row is:'+str(temp_row)+'; temp_col is:'+str(temp_col)
                            if final_fire_2D_grid[r][c] != 1:
                                final_fire_2D_grid[r][c] = 1

    print count
    for r in range(dem_rows):
        for c in range(dem_cols):
            if final_fire_2D_grid[r][c] == 1:
                print 'row is:'+str(r)+'; col is:'+str(c)+';'
                count1 = count1 + 1
    print count1



    # change veg resolution into dem resolution
    for item in final_fire_2D_grid:
        line = [str(i) for i in item]
        # line.append('\n')
        fp.write(','.join(line)+'\n')

    fp.close()

def get_veg_types(veg_out_file):
    '''
    # this function is used to get possible vegtation types
    '''
    # use this list to record all the possible veg types
    result_list = []
    # this records the meta data info
    meta_data = []
    # this records the two dimensional veg grid data
    veg_grid_data = []
    file_handle = open(veg_out_file)
    meta_data_line_num = 6
    # for current version skip meta data part
    for i in range(meta_data_line_num):
        line = file_handle.readline().strip().split()
        meta_data.append(line)
    while True:
        line = file_handle.readline().strip()
        if line == '':
            # either end of file or just a blank line.....
            # For all jessie fire files, it should be eof
            break
        else:
            temp_list = line.split(' ')
            veg_grid_data.append(temp_list)
            for i in temp_list:
                if i not in result_list:
                    result_list.append(i)
    # convert all the element into int
    result_list = [int(m) for m in result_list]
    # sort
    result_list.sort()
    file_handle.close()
    return meta_data, result_list, veg_grid_data

def wind_file_process(wind_file):
    '''
    this function is used to get possible wind values
    '''
    # use this list to record all the possible veg types
    result_list = []
    # this records the meta data info
    meta_data = []
    # this records the two dimensional veg grid data
    # veg_grid_data = []
    file_handle = open(wind_file)
    meta_data_line_num = 6
    # for current version skip meta data part
    for i in range(meta_data_line_num):
        line = file_handle.readline().strip().split()
        meta_data.append(line)
    while True:
        line = file_handle.readline().strip()
        if line == '':
            # either end of file or just a blank line.....
            # For all jessie fire files, it should be eof
            break
        else:
            temp_list = line.split(' ')
            # veg_grid_data.append(temp_list)
            for i in temp_list:
                if i not in result_list:
                    result_list.append(i)
    # convert all the element into int
    result_list = [int(m) for m in result_list]
    # sort
    result_list.sort()
    file_handle.close()
    return meta_data, result_list
    # return meta_data, result_list, veg_grid_data

def veg_out_file_processing(veg_out_file,num_rows,num_cols):
    '''
    this function extracts values from veg file and if veg_row <= num_rows
    and veg_col<=num_cols, the program will map veg grid into a bigger map
    '''
    meta_data, veg_code, veg_grid_data = get_veg_types(veg_out_file)
    nrows = int(veg_grid_data[1][1])
    ncols = int(veg_grid_data[0][1])
    if num_rows<=nrows or num_cols<=ncols:
        raise Exception('try to map bigger veg map into a smaller')
    '''
    # here is the method to map smaller veg map into bigger map
    # total_rows = numrow * vegrow, total_rows*m/vegrow = total_rows*n/numrow
    # m is the current veg row num, n is the bigger map num
    final_veg_grid_data = []
    # total_rows = num_rows * nrows
    # total_cols = num_cols * ncols
    for n in range(num_rows):
        temp_row_index = int(math.floor((nrows*n)/num_rows))
        temp_arr = []
        for m in range(num_cols):
            temp_col_index = int(math.floor((ncols*n)/num_cols))
            temp_arr.append(veg_grid_data[temp_row_index][temp_col_index])
            # print veg_grid_data[temp_row_index][temp_col_index]
        #print temp_arr
        final_veg_grid_data.append(temp_arr)
    '''
    #json_dict = {'meta_data':meta_data,'veg_code':veg_code,'grid_data':final_veg_grid_data}
    json_dict = {'meta_data':meta_data,'veg_code':veg_code,'grid_data':veg_grid_data}
    return json.dumps(json_dict)

def execute(directory, command, log_path=None, err_log_path=None):
    '''
    This functino is used to execute c++
    This function is from Moinul
    https://github.com/VirtualWatershed/vw-py/blob/master/vwpy/prms_runner.py
    '''
    if not log_path:
        print 'NO log file provided!'
        #log_path = '/dev/null'
    if not os.path.exists(os.path.dirname(log_path)):
        os.makedirs(os.path.dirname(log_path))

    with open(log_path, 'wb') as process_out, open(log_path, 'rb', 1) as reader, open(err_log_path, 'wb') as err_out:
        process = subprocess.Popen(
            command, stdout=process_out, stderr=err_out, cwd=directory)
        
    # this waits the process finishes
    process.wait()
    return True

def exec_model():
    '''
    This function is used to exec fire model
    with different inputs and outputs
    '''
    app_root = os.path.dirname(os.path.abspath(__file__))
    log_path = app_root + '/log.txt'
    err_log_path = app_root + '/err_log.txt'
    data_folder = app_root + '/static/data/'
    command = ['./simulator','temp_upload_fuel','temp_upload_onfire','temp_final_tests.csv','temp_windx.fuel','temp_windy.fuel', data_folder]
    exec_dir = app_root + '/fire_sim_lib/build/'
    execute(exec_dir, command, log_path, err_log_path)

def json_veg_info():
    '''
    hard coded the infor here
    '''
    # this is not the full info, I am just tired to manually copy paste today
    veg_info_dict = {
        '1': 'Short (1 ft) grass',
        '2': 'Timber',
        '3': 'Tall (>2.5 ft) grass',
        '4': 'Chapparral (6 ft)',
        '5': 'Brush (2 ft)',
        '6': 'Dormant brush, hardwood slash',
        '7': 'Southern rough',
        '8': 'Closed timber litter',
        '9': 'Hardwood litter',
        '10': 'Timber (litter and understory)',
        '11': 'Light logging slash',
        '12': 'Medium logging slash',
        '13': 'Heavy logging slash',
        '91': 'Urban/Developed',
        '92': 'Snow/Ice',
        '93': 'Agricultural',
        '98': 'Open Water',
        '99': 'Bare Ground',
        '101': 'Short, Sparse Dry Climate Grass (Dynamic)',
        '102': 'Low Load, Dry Climate Grass (Dynamic)',
        '103': 'Low Load, Very Coarse, Humid Climate Grass (Dynamic)',

        '141': 'Low Load Dry Climate Shrub (Dynamic)',
        '142': 'Moderate Load Dry Climate Shrub',
        '165': 'Very High Load, Dry Climate Timber-Shrub'

    }
    return json.dumps(veg_info_dict)


def download_scenario_file(file_list,scenario_file):
    # the zip function is kind of from http://stackoverflow.com/questions/11240728/zipping-files-in-python
    # hard coded the zip file name, should get from the config file
    app_root = os.path.dirname(os.path.abspath(__file__))
    data_folder = app_root + '/static/data/'
    zip_name = zipfile.ZipFile(data_folder+'/'+scenario_file,'w')
    for i in file_list:
        full_path = data_folder+'/'+i
        zip_name.write(full_path,i)

def process_scenario_file(file_list,scenario_file):
    # this function is basically from http://stackoverflow.com/questions/9431918/extracting-zip-file-contents-to-specific-directory-in-python-2-7
    app_root = os.path.dirname(os.path.abspath(__file__))
    data_folder = app_root + '/static/data/'
    zip_name = zipfile.ZipFile(data_folder+'/'+scenario_file,'r')
    outpath = data_folder + '/'
    for name in zip_name.namelist():
        zip_name.extract(name,outpath)

# def line_prepender(filename, line):
#     '''
#     This function is from http://stackoverflow.com/questions/5914627/prepend-line-to-beginning-of-a-file
#     I used it to prepend some metadata in the file
#     '''
#     with open(filename, 'r+') as f:
#         content = f.read()
#         f.seek(0, 0)
#         f.write(line.rstrip('\r\n') + '\n' + content)

# /cse/hpcvis/vrdemo/Desktop/fire_folder/firesim/build/simulator
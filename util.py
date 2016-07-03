import json
import math

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
        temp_list = line.strip().split(',')
        # need to pop the last element, coz each row of the output file 
        # is like this '...,', so the last element will be '' after split(',')
        temp_list.pop()
        for i in range(len(fire_data)):
            temp_item = []
            for m in temp_list:
                if m<=(i+start_time):
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



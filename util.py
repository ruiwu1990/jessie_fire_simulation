import json

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

# this function is used to get possible vegtation types
def get_veg_types(veg_out_file):
    # use this list to record all the possible veg types
    result_list = []
    # this record the meta data info
    meta_data = []
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
            for i in temp_list:
                if i not in result_list:
                    result_list.append(i)
    # convert all the element into int
    result_list = [int(m) for m in result_list]
    # sort
    result_list.sort()
    file_handle.close()
    return [meta_data,result_list]

# TODO combine this fun with get_veg_types
def veg_out_file_processing(veg_out_file):
    meta_result = get_veg_types(veg_out_file)
    return'aaa'



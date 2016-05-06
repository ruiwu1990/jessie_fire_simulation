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
    return json.dumps(json_dict)
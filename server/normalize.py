SeaLevelPressure = 900

def pressure_to_height(pressure):
    height = ((pressure/SeaLevelPressure)**(1/5.275)-1)*(15+273.15)/0.0065
    return height

def height_to_angle(height1, height2):
    angle = math.asin(height1-height2)
    return angle

def normalize(csv_file):
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        angle_list = []
        normalized_list = []
        for raw in reader:
#            angle_list.append(height_to_angle(pressure_to_height(float(raw[1])), pressure_to_height(float(raw[2]))))
            angle_list.append(height_to_angle(float(raw[1])) - pressure_to_height(float(raw[2])))
        max_length = max(angle_list)
        for angle in angle_list:
            angle = height_to_angle(angle/max_length)
        max_angle = max(angle_list)
        min_angle = min(angle_list)
        for index, angle in enumerate(angle_list):
            normalized_list.append([reader[index][0], str((angle-min_angle)/(max_angle-min_angle))])
        print(normalized_list)
    return normalized_list

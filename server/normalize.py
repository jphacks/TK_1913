import csv
import math

SeaLevelPressure = 900

def pressure_to_height(pressure):
    height = ((pressure/SeaLevelPressure)**(1/5.275)-1)*(15+273.15)/0.0065
    return height

def height_to_angle(diff_height):
    angle = math.asin(diff_height)
    return angle

def normalize(csv_file):
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        height_list = []
        angle_list = []
        normalized_list = []
        time_list = []
        for raw in reader:
#            angle_list.append(height_to_angle(pressure_to_height(float(raw[1])), pressure_to_height(float(raw[2]))))
            height_list.append(pressure_to_height(float(raw[2])) - pressure_to_height(float(raw[1])))
            time_list.append(raw[0])
        print(height_list)
        max_length = max(height_list)
        for height in height_list:
            angle_list.append(height_to_angle(height/max_length))
#        print(angle)
        print(angle_list)
        max_angle = math.pi/2
        min_angle = min(angle_list)
        for index, angle in enumerate(angle_list):
            if angle <= 90-min_angle:
                normalized_list.append([time_list[index], str((angle-min_angle)/(max_angle-min_angle))])
            else:
                normalized_list.append([time_list[index], str(1)])

    with open('normalized_data/' + csv_file.split('/')[1], 'w') as wf:
        writer = csv.writer(wf)
        for normalized_data in normalized_list:
            writer.writerow(normalized_data)
    return normalized_list

def main():
    return

if __name__ == '__main__':
    main()

import csv
import math

SeaLevelPressure = 101000

def pressure_to_height(pressure):
    height = ((SeaLevelPressure/pressure)**(1/5.275)-1)*(15+273.15)/0.0065
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
            height_list.append(float(raw[2]) - float(raw[1]))
            time_list.append(raw[0])
        print(height_list)
        max_length = max(height_list)
        for height in height_list:
            angle_list.append(height_to_angle(height/max_length))
#        print(angle)
        print(angle_list)
#        max_angle = math.pi/2
#        min_angle = min(angle_list)
        for index, angle in enumerate(angle_list):
            if 0 <=  math.pi/2 - angle <= 2*math.pi/9:
                normalized_list.append([time_list[index], 9*(math.pi/2-angle)/(4*math.pi)])
            elif 2*math.pi/9 <= math.pi/2 - angle <= math.pi/2:
                normalized_list.append([time_list[index], 9*(math.pi/2-angle)/(5*math.pi)-1/10])
            elif math.pi/2 - angle < 0:
                normalized_list.append([time_list[index], 0])
            else:
                normalized_list.append([time_list[index], 1])

    with open('normalized_data/' + csv_file.split('/')[1], 'w') as wf:
        writer = csv.writer(wf)
        for normalized_data in normalized_list:
            writer.writerow(normalized_data)
    return normalized_list

def main():
    return

if __name__ == '__main__':
    main()

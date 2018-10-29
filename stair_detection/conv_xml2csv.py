import xml.etree.ElementTree as ET
import os
import cv2

def parse_xml(path):
    xmin = 0
    xmax = 0
    ymin = 0
    ymax = 0
    height = 0
    width = 0
    tree = ET.parse(path)
    root = tree.getroot()
    path = ''

    for i in root.iter('annotation'):
        folder = i.find('folder').text
        filename = i.find('filename').text
        path = i.find('path').text

    # image parameters
    for j in root.iter('size'):
        height = j.find('height').text
        width = j.find('width').text
        depth = j.find('depth').text

    # bounding box parameters
    for m in root.iter('bndbox'):
        xmin = m.find('xmin').text
        xmax = m.find('xmax').text
        ymin = m.find('ymin').text
        ymax = m.find('ymax').text
        # casting to a base 10 integer
        xmin = int(xmin, 10)
        xmax = int(xmax, 10)
        ymin = int(ymin, 10)
        ymax = int(ymax, 10)
        # converting to centre coordinates from corner coordinates
        x = (float(xmin + xmax) / 2)
        y = (float(ymin + ymax) / 2)
        # normalizing
        x = float(float(x) / int(width, 10))
        y = float(float(y) / int(height, 10))

        box_width = (float(xmax - xmin) / int(width, 10))
        box_height = (float(ymax - ymin) / int(height, 10))

        print(x, y, box_width, box_height)
        # filename[:-4] implies dropping last 4 characters since
        # -4 index means 4th character from the end
        fullpath = 'train/' + filename[:-4] + ".txt"
        full_flipped_path = 'train/' + filename[:-4] + "_flipped.txt"
        with open(fullpath, 'a') as text_file:
            # writing in the format - class x y box_width box_height
            label = str(0) + " " + str(x) + " " + str(y) + " " + str(box_width) + " " + str(box_height) + "\n"
            text_file.writelines(label)

        with open(full_flipped_path, 'a') as text_file:
            label = str(0) + " " + str(1 - x) + " " + str(y) + " " + str(box_width) + " " + str(box_height) + "\n"
            text_file.writelines(label)

    with open('train_filenames.txt', 'a') as text_file:
        ultrapath = '/home/nvidia/darknet/data/' + 'train/' + filename + '\n'
        text_file.writelines(ultrapath)
        ultra_flipped_path = "/home/nvidia/darknet/data/" + 'train/' + filename[:-4] + '_flipped.jpg' + '\n'
        text_file.writelines(ultra_flipped_path)

def main():
    path = 'train/'
    for filename in os.listdir(path):
        if not filename.endswith('.xml'):
            continue
        fullname = os.path.join(path, filename)
        parse_xml(fullname)

    for filename in os.listdir(path):
        if filename.endswith('.jpg' or '.JPG'):
            img = cv2.imread(os.path.join(path, filename))
            img = cv2.flip(img, 1)
            final_path = filename[:-4] + '_flipped.jpg'
            print(os.path.join(path, final_path))
            cv2.imwrite(str(os.path.join(path, final_path)), img)

if __name__ == '__main__':
    main()

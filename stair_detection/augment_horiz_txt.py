import os
import cv2

path = 'train'
for filename in os.listdir(path):
    if filename.endswith('.jpg' or '.JPG'):
        img = cv2.imread(os.path.join(path, filename))
        img = cv2.flip(img, 1)
        flipped_path = filename[:-4] + '_flipped.jpg'
        cv2.imwrite(os.path.join(path, flipped_path), img)

    if filename.endswith('.txt'):
        # gets the lines from text file
        y = [x.rstrip() for x in open(os.path.join(path, filename))]
        # iterating over all lines
        for line in y:
            # split the 5 parameters separated by spaces
            elems = line.split(' ')
            print(elems[1])

            flipped_name = filename[:-4] + '_flipped.txt'

            with open(os.path.join(path, flipped_name), 'a') as text_file:
                labels = elems[0] + ' ' + str(1 - float(elems[1])) + ' ' + elems[2] + ' ' + elems[3] + ' ' + elems[4]
                text_file.writelines(labels)

    with open('train_filenames.txt', 'a') as text_file:
        if filename.endswith('.jpg' or '.JPG'):
            ultrapath = '/home/nvidia/darknet/data/' + 'train/' + filename + '\n'
            text_file.writelines(ultrapath)
            ultra_flipped_path = "/home/nvidia/darknet/data/" + 'train/' + filename[:-4] + '_flipped.jpg' + '\n'
            text_file.writelines(ultra_flipped_path)

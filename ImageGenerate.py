from datetime import datetime
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw



#Top-left corner coordinates of selected area, (x, y)
top_left = (544, 21)

#Bottom-right corner coordinates of selected area, (x, y)
bottom_right = (682, 85)

#Zoom, value is height and width of each pixel
zoom = 10

#How many pixels should be painted before 1 image is generated, since theres around 160,000,000 pixels total a value of 100,000 gives about 1600 images
pixels_placed_interval = 100000

img = Image.new('RGB', ((bottom_right[0] - top_left[0]) * zoom, (bottom_right[1] - top_left[1]) * zoom), color='white')
imgDraw = ImageDraw.Draw(img)

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

#Process a chunk of data, bunch of pixels gets painted based on chunk size and when whole chunk is done generates 1 image
def process_data_chunk(data, index):
    for i in range(len(data)):
        if int(len(data[i][3])) < 100:
            x = list(map(int, data[i][3].split(",")))[0] * zoom - top_left[0] * zoom
            y = list(map(int, data[i][3].split(",")))[1] * zoom - top_left[1] * zoom

            shape = [(x, y), (x + zoom - 1, y + zoom - 1)]
            imgDraw.rectangle(shape, hex_to_rgb(data[i][2]))
    filename = str(index).zfill(6)
    img.save('DataImages/' + filename + '.png')


#Function that return 2d-array of dates and file names, sorted by dates on the first column, needed because the files in the dataset is not sorted but the data inside is
def get_file_order():
    
    file_start_dates = [[0]*2 for i in range(78)]

    for i in range(0, 78):
        indexfile = str(i).zfill(12)
        dataRead = pd.read_csv('Data/2022_place_canvas_history-' + indexfile + '.csv.gzip', nrows=1, compression='gzip', error_bad_lines=False)
        data = np.array(dataRead)

        date_time_string = data[0][0].strip(' UTC')
        date_time = datetime.strptime(date_time_string, '%Y-%m-%d %H:%M:%S.%f')

        file_start_dates[i][0] = date_time
        file_start_dates[i][1] = 'Data/2022_place_canvas_history-' + indexfile + '.csv.gzip'
    

    file_start_dates = sorted(file_start_dates, key=lambda x: x[0])
    return file_start_dates

running = True
indexfile = 0
index = 0

sorted_filename_list = get_file_order()

while running:
    
    for i in range(0, 78):
        print(i)

        for dfChunk in pd.read_csv(sorted_filename_list[i][1], chunksize=pixels_placed_interval, compression='gzip', error_bad_lines=False):
            data = np.array(dfChunk)
            process_data_chunk(data, index)
            index = index + 1
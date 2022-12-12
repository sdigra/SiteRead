from PIL import Image
import numpy as np
import math
def sheet_to_notes(filename, num_bars, measures_per_bar):
    image = Image.open(filename).convert('L')
    # pixel_values = list(image.getdata())
    # pixel_values = np.array(pixel_values).reshape((width, height))
    # pixel_values = ((pixel_values / 17)).astype(int).astype(float)
    pixel_values = np.asarray(image)
    pixel_values = pixel_values[:,140:-80]
    # plt.imshow(pixel_values, cmap='Greys_r')
    # plt.show()
    height, width = pixel_values.shape
    bar_height = int(height/num_bars)
    measure_width = int(width/measures_per_bar)
    notes = []
    for i in range(num_bars):
        bar = pixel_values[i*bar_height:(i+1)*bar_height,:]
        for j in range(measures_per_bar):
            measure = bar[:,j*measure_width:(j+1)*measure_width]
            for k in range(4):
                note = measure[:,k*int(measure_width/4):(k+1)*int(measure_width/4)]
                notes.append(note[int(120-7.5*i):int(300-7.5*i),:])
    return notes

def remove_lines(notes):
    data = np.array(notes)
    images_temp = []
    for i in data:
        i[i <= 15] = 0
        i[i > 15] = 1
        if np.sum(i) < 50:
            continue
        pad_width = 95 - i.shape[1]
        pad_height = 205 - i.shape[0]
        temp = np.pad(i, [(math.ceil(pad_height/2), math.floor(pad_height/2)), (math.ceil(pad_width/2), math.floor(pad_width/2))], mode='constant', constant_values = (1))
        temp = 1-temp
        images_temp.append(temp)
    images = np.array(images_temp)
    X_test = images.reshape((len(images), -1))
    # targets = [0]*4 + [1]*4 + [3]*4 + [2]*4
    
    return X_test


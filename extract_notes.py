import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def sheet_to_notes(filename, num_bars, measures_per_bar):
    image = Image.open(filename).convert('L')
    pixel_values = np.asarray(image)
    pixel_values = pixel_values[:,70:-40]
    plt.imshow(pixel_values, cmap='Greys_r')
    plt.show()
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
                notes.append(note[int(40-2.5*i):int(100-2.5*i),:])
    return notes

notes = sheet_to_notes('./test-sheet.jpg', 8, 4)

# %%
fig = plt.figure(figsize=(50, 50))  # width, height in inches

for i in range(128):
    sub = fig.add_subplot(8, 16, i + 1)
    sub.imshow(notes[i], cmap='Greys_r')
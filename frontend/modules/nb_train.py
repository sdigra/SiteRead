# MUSICMA tutorial: https://muscima.readthedocs.io/en/latest/Tutorial.html
# imports important 
# %%
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def get_key(note):
    # notes just a 2d array representing the grayscale pixels
    # we can maybe just find the middle coord of the note
    # and use that to determine the key?

    height, width = note.shape
    left, right = 0, width-1

    bwnote = [[0 for j in range(width)] for i in range(height)]

    for i in range(height):
        for j in range(width):
            if note[i,j] > 247:
                bwnote[i][j] = 255
    # print("bwnote")
    # for i in range(height):
    #     print(bwnote[i][0])

    # figure out which rows are the staff lines so we can ignore those
    staff_pixels = [0 for i in range(height)] 

    for i in range(height):
        if(bwnote[i][2] == 0):
            staff_pixels[i] = 1

    for i in range(height):
        for j in range(2):
            bwnote[i][j] = 255
        for j in range(6):
            bwnote[i][width-1-j] = 255

    # for i in range(height):
    #     for j in range(width):
    #         print(str(bwnote[i][j]), end=" ")
    #     print()

    # for i in staff_pixels:
    #     print(i)
    
    # looking for left and right pixels of the note
    i = left

    while left == 0:
        for j in range(height):
            if(bwnote[j][i] == 0 and staff_pixels[j] == 0):
                left = i
                break
        i += 1
    i = right
    while right == width-1:
        for j in range(height):
            if(bwnote[j][i] == 0 and staff_pixels[j] == 0):
                right = i
                break
        i -= 1
    # print(str(left) + " " + str(right) + " " + str(width))

    # look for the y coordinate at the middle
    # we can probably use that to figure out the key
    # as long as we know the coords of the measure
    y1 = 0
    y2 = height-1
    for j in range(height):
        if(bwnote[j][(left+right)//2] == 0 and staff_pixels[j] == 0):
            y1 = j
            break
    for j in range(height):
        if(bwnote[height-1-j][(left+right)//2] == 0 and staff_pixels[height-1-j] == 0):
            y2 = height-1-j
            break
    first_staff = 0
    last_staff = 0
    for i in range(len(staff_pixels)):
        if staff_pixels[i] == 1:
            last_staff = i
            if first_staff == 0:
                first_staff = i
    # print("last staff: " + str(last_staff))
    note_height = (last_staff-first_staff)/4

    # just in case the image is ass and it couldnt find the top or bottom of the note i shoulda dropped this class i hate everything
    # if(y1 == 0 and y2 != height-1):
    #     y1 = y2 - note_height
    # elif(y2 == height-1 and y1 != 0):
    #     y2 = y1 + note_height

    last_staff = last_staff - first_staff
    x = 8/last_staff
    # print("note height = " + str(note_height))
    # print(str(y1) + " " + str(y2) + " " + str(height))
    y = (y1+y2)//2
    y = (y-first_staff)*x
    # print("y = " + str(y))

    return round(y)

# keys = [get_key(np.asarray(i)) for i in note_images]
# print(keys[0])
# image = Image.open("noteuno.jpeg").convert('L')
# pixel_values = np.asarray(image)
# print("key: " + str(get_key(pixel_values)))
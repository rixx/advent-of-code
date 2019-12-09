"""
Part 1: Image Checksum
"""
total_length = len(image_data)
rows = 6
columns = 25
single_length = rows * columns
layer_count = total_length / single_length

total_zeroes = 9999
score = None

for n in range(int(layer_count)):
    layer_data = image_data[n * single_length:(n + 1) * single_length]
    zero_count = layer_data.count('0')
    if zero_count < total_zeroes:
        total_zeroes = zero_count
        score = layer_data.count('1') * layer_data.count('2')


"""
Part 2: Image decoding
"""
import copy

rows = 6
columns = 25

total_length = len(image_data)
single_length = rows * columns
layer_count = total_length / single_length

image_map = {0: "█", 1: "░", 2: " "}
image = [
    [" " for _ in range(columns)]    
    for __ in range(rows)
]
for n in range(int(layer_count)):
    layer_data = image_data[n * single_length:(n + 1) * single_length]
    for row in range(rows):
        for column in range(columns):
            if image[row][column] != " ":
                continue
            digit = layer_data[row * columns + column]
            image[row][column] = image_map[int(digit)]

for row in image:
    print("".join(row))

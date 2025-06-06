import pandas as pd
import sys

def partition(images, parts):
    length = len(images)

    images = images.sort_values(by='resolution', kind="mergesort")

    part_size = length //parts
    partitions = []

    for i in range(parts):
        start = i*part_size
        if i < parts-1:
            end = (i+1)*part_size
        else:
            end = length
        partitions.append(images.iloc[start:end].reset_index(drop=True))
    
    return partitions

def output(partitions):
    i = 0
    for set in partitions:
        i+=1
        pd.DataFrame(data=set, columns=['filename', 'image_path', 'width', 'height', 'resolution']).to_csv(f"Part{i}.csv", index=False)


df = pd.read_csv(sys.argv[1]) #csv of resolutions outputted by parser
output(partition(df, int(sys.argv[2]))) #number of parts

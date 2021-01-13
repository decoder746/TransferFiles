import sys
import os
import random
import commands
import csv
import json
import numpy as np
import math
import argparse
from csv import reader

csv_path=sys.argv[1]
domain = sys.argv[2]

to_compute_min_mean_max = ["importanceScore", "megaEventContinuityScore", "diversityTimeScore", "diversitySceneScore", "diversityConceptScore", "diversitySimScore", "normalized_vis_cont", "normalized_uniformity"]

grand_master_csv_results = [["configuration", "video", "budget", "avgf1", "maxf1", "importanceScore", "megaEventContinuityScore", "diversityTimeScore", "diversitySceneScore", "diversityConceptScore", "diversitySimScore", "normalized_vis_cont", "normalized_uniformity"]]

algos = ["random", "human", "vis-cont-max", "uniformity", "auto", "proportional"]

# algos = ["mixture-cfg1", "mixture-cfg2", "mixture-cfg4", "mixture-cfg6"]

# read csv file as a list of lists
with open(csv_path, 'r') as read_obj:
    csv_reader = reader(read_obj)
    list_of_rows = list(csv_reader)

for algo in algos:
    master_without_header = []
    for i in range(len(list_of_rows)):
        row = list_of_rows[i][1:]
        #print(row)
        #sys.exit()
        if algo == "human":
            if row[1].isdigit():
                temp = map(lambda x:float(x) if not x.isalpha() and "_" not in x and "-" not in x else x, row)
                master_without_header.append(temp)
        else:
            if row[0] == algo:
                temp = map(lambda x:float(x) if not x.isalpha() and "_" not in x and "-" not in x else x, row)
                master_without_header.append(temp)
    #print(master_without_header[0])
    #print(master_without_header[1])
    transposed = map(list, zip(*master_without_header))
    transposed = transposed[3:]
    minRow = [algo+"-min", "xxx", "xxx"]
    meanRow = [algo+"-mean", "xxx", "xxx"]
    maxRow = [algo+"-max", "xxx", "xxx"]
    for i in range(len(transposed)):
        min_i = min(transposed[i])
        mean_i = round(sum(transposed[i])/len(transposed[i]),4)
        max_i = max(transposed[i])
        if i == 3 or i == 8:
            min_i = round(math.sqrt(min_i), 4)
            mean_i = round(math.sqrt(mean_i), 4)
            max_i = round(math.sqrt(max_i), 4)
        minRow.append(min_i)
        meanRow.append(mean_i)
        maxRow.append(max_i)
    grand_master_csv_results.append(minRow)
    grand_master_csv_results.append(meanRow)
    grand_master_csv_results.append(maxRow)


    
   
    # column_names = master_csv_results.pop(0)
    # df = pd.DataFrame(master_csv_results, columns = column_names)
    # minRow = [algo+"-min", "xxx", "xxx"]
    # for column in to_compute_min_mean_max:
    #     if column == "megaEventContinuityScore" or column == "normalized_vis_cont":
    #         minRow.append(round(math.sqrt(df[column].min()), 4))
    #     else:
    #         minRow.append(round(df[column].min(), 4))
    # #master_csv_results.append(minRow)
    # grand_master_csv_results.append(minRow)
    # meanRow = [algo+"-mean", "xxx", "xxx"]
    # for column in to_compute_min_mean_max:
    #     if column == "megaEventContinuityScore" or column == "normalized_vis_cont":
    #         meanRow.append(round(math.sqrt(df[column].mean()), 4))
    #     else:
    #         meanRow.append(round(df[column].mean(), 4))
    # #master_csv_results.append(meanRow)
    # grand_master_csv_results.append(meanRow)
    # maxRow = [algo+"-max", "xxx", "xxx"]
    # for column in to_compute_min_mean_max:
    #     if column == "megaEventContinuityScore" or column == "normalized_vis_cont":
    #         maxRow.append(round(math.sqrt(df[column].max()), 4))
    #     else:
    #         maxRow.append(round(df[column].max(), 4))
    # #master_csv_results.append(maxRow)
    # grand_master_csv_results.append(maxRow)

# Write results to csv file
with open(domain + "_final_human_normalized_master.csv", "wb") as f:
    writer = csv.writer(f)
    for result in grand_master_csv_results:
        writer.writerow(result)
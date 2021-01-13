import sys
import os
import random
import commands
import csv
import json
import numpy as np
import math
import argparse
import pandas as pd
from csv import reader

parser = argparse.ArgumentParser()
parser.add_argument('--path', type=str, help="Master data path")
parser.add_argument('--domain', type=str, help="Domain")
parser.add_argument('--algos', nargs="*", type=str, help="List of algos")
parser.add_argument('--pre-normalize', action='store_true', help="Should normalization be done based on existing norms constant?" )
parser.add_argument('--frame-norms', type=str, help="Path of frame norms file for this domain")
parser.add_argument('--ignore-missing', action='store_true', help="Set if you want to ignore absence of scores for ome auto or random summaries")
args = parser.parse_args()

to_compute_min_mean_max = ["importanceScore", "megaEventContinuityScore", "diversityTimeScore", "diversitySceneScore", "diversityConceptScore", "diversitySimScore", "normalized_vis_cont", "normalized_uniformity"]

path = args.path
normsJsonFile = args.frame_norms
domain = args.domain
algos = args.algos
pre_normalize = args.pre_normalize
ignore_missing = args.ignore_missing

# read norms file
with open(normsJsonFile) as norms_json:
    norms = json.load(norms_json)

budgets = [60, 90, 120, 150, 180]

grand_master_csv_results = [["configuration", "video", "budget", "avgf1", "maxf1", "importanceScore", "megaEventContinuityScore", "diversityTimeScore", "diversitySceneScore", "diversityConceptScore", "diversitySimScore", "normalized_vis_cont", "normalized_uniformity"]]

master_csv_results = [["configuration", "video", "budget", "avgf1", "maxf1", "importanceScore", "megaEventContinuityScore", "diversityTimeScore", "diversitySceneScore", "diversityConceptScore", "diversitySimScore", "normalized_vis_cont", "normalized_uniformity"]]

for algo in algos:
    for budget in budgets:
        algoPath = os.path.join(path, domain, str(budget), algo)
        #Either we directly have summaries in this path, or we have video folders
        files = os.listdir(algoPath)
        temp = os.path.join(algoPath, files[0])
        if os.path.isfile(temp):
            if not algo.startswith("dr-dsn"):
                print("Not possible!!!")
                sys.exit()
            summaries = files
            for algoSummary in summaries:
                algoSummaryPath = os.path.join(algoPath, algoSummary)
                video = algoSummary.split(algo)[0][:-1]
                with open(algoSummaryPath, "r") as f:
                    algoSummaryJson = json.load(f)
                scores = [algo, video, budget]
                scores.append(round(algoSummaryJson["frame_scores"]["avgf1auto"], 4))
                scores.append(round(algoSummaryJson["frame_scores"]["maxf1auto"], 4))
                if pre_normalize:
                    scores.append(
                        round(algoSummaryJson["frame_scores"]["imp"]/norms[video_name][str(budget)]["importanceScore"], 4))
                    scores.append(round(algoSummaryJson["frame_scores"]["mega-cont"]/norms[video_name][str(budget)]["megaEventContinuityScore"], 4))
                    scores.append(
                        round(algoSummaryJson["frame_scores"]["div-time"]/norms[video_name][str(budget)]["diversityTimeScore"], 4))
                    scores.append(round(algoSummaryJson["frame_scores"]["div-scene"]/norms[video_name][str(budget)]["diversitySceneScore"], 4))
                    scores.append(
                        round(algoSummaryJson["frame_scores"]["div-concept"]/norms[video_name][str(budget)]["diversityConceptScore"], 4))
                    scores.append(
                        round(algoSummaryJson["frame_scores"]["div-sim"]/norms[video_name][str(budget)]["diversitySimScore"], 4))
                else:
                    scores.append(
                        round(algoSummaryJson["frame_scores"]["imp"], 4))
                    scores.append(round(algoSummaryJson["frame_scores"]["mega-cont"], 4))
                    scores.append(
                        round(algoSummaryJson["frame_scores"]["div-time"], 4))
                    scores.append(round(algoSummaryJson["frame_scores"]["div-scene"], 4))
                    scores.append(
                        round(algoSummaryJson["frame_scores"]["div-concept"], 4))
                    scores.append(
                        round(algoSummaryJson["frame_scores"]["div-sim"], 4))
                scores.append(round(algoSummaryJson["frame_scores"]["norm-vis-cont"], 4))
                scores.append(round(algoSummaryJson["frame_scores"]["norm-uniform"], 4))
                master_csv_results.append(scores)
        else:
            videos = files
            for video in videos:
                scores = [[], [], [], [], [], [], [], [], [], []]
                video_name = video
                summariesPath = os.path.join(algoPath, video)
                print("Processing ", algo, " summaries of ", video_name, budget)
                algoSummaries = os.listdir(summariesPath)
                for algoSummary in algoSummaries:
                    if not algoSummary.endswith("json"):
                        continue
                    algoSummaryPath = os.path.join(summariesPath, algoSummary)
                    with open(algoSummaryPath, "r") as f:
                        algoSummaryJson = json.load(f)
                    if "frame_scores" not in algoSummaryJson and ignore_missing and (algo == "random" or algo == "automaticGTSummaries") :
                        print("Ignoring as score has not been computed for this")
                        continue
                    scores[0].append(round(algoSummaryJson["frame_scores"]["avgf1auto"], 5))
                    scores[1].append(round(algoSummaryJson["frame_scores"]["maxf1auto"], 5))
                    if pre_normalize:
                        scores[2].append(
                            round(algoSummaryJson["frame_scores"]["imp"]/norms[video_name][str(budget)]["importanceScore"], 5))
                        scores[3].append(round(algoSummaryJson["frame_scores"]["mega-cont"]/norms[video_name][str(budget)]["megaEventContinuityScore"], 5))
                        scores[4].append(
                            round(algoSummaryJson["frame_scores"]["div-time"]/norms[video_name][str(budget)]["diversityTimeScore"], 5))
                        scores[5].append(round(algoSummaryJson["frame_scores"]["div-scene"]/norms[video_name][str(budget)]["diversitySceneScore"], 5))
                        scores[6].append(
                            round(algoSummaryJson["frame_scores"]["div-concept"]/norms[video_name][str(budget)]["diversityConceptScore"], 5))
                        scores[7].append(
                            round(algoSummaryJson["frame_scores"]["div-sim"]/norms[video_name][str(budget)]["diversitySimScore"], 5))
                    else:
                        scores[2].append(
                            round(algoSummaryJson["frame_scores"]["imp"], 5))
                        scores[3].append(round(algoSummaryJson["frame_scores"]["mega-cont"], 5))
                        scores[4].append(
                            round(algoSummaryJson["frame_scores"]["div-time"], 5))
                        scores[5].append(round(algoSummaryJson["frame_scores"]["div-scene"], 5))
                        scores[6].append(
                            round(algoSummaryJson["frame_scores"]["div-concept"], 5))
                        scores[7].append(
                            round(algoSummaryJson["frame_scores"]["div-sim"], 5))
                    scores[8].append(round(algoSummaryJson["frame_scores"]["norm-vis-cont"], 5))
                    scores[9].append(round(algoSummaryJson["frame_scores"]["norm-uniform"], 5))
                avgs = [algo, video, budget, round(sum(scores[0]) / len(scores[0]), 4), round(sum(scores[1]) / len(scores[1]), 4), round(sum(scores[2]) / len(scores[2]), 4),
                        round(sum(scores[3]) / len(scores[3]), 4), round(sum(scores[4]) / len(scores[4]), 4), round(sum(scores[5]) / len(scores[5]), 4), round(sum(scores[6]) / len(scores[6]), 4), round(sum(scores[7]) / len(scores[7]), 4), round(sum(scores[8]) / len(scores[8]), 4), round(sum(scores[9]) / len(scores[9]), 4)]
                master_csv_results.append(avgs)

# Write results to csv file
if pre_normalize:
    normalized_master_csv_result = master_csv_results
    out = domain + "_frame_normalized_master.csv"
else:
    out = domain + "_frame_master.csv"
with open(out, "wb") as f:
    writer = csv.writer(f)
    for result in master_csv_results:
        writer.writerow(result)
    f.flush()

if not pre_normalize:
    #normalize this csv
    soccer_videos = ["soccer_1", "soccer_2", "soccer_3", "soccer_5", "soccer_7", "soccer_8", "soccer_9", "soccer_10", "soccer_11", "soccer_12", "soccer_17", "soccer_18"]
    friends_videos = ["friends_1", "friends_2", "friends_3", "friends_4", "friends_5", "friends_6", "friends_7", "friends_9", "friends_12", "friends_16", "friends_18", "friends_19"]
    surveillance_videos = ["surveillance_1", "surveillance_2", "surveillance_3", "surveillance_4", "surveillance_5", "surveillance_6", "surveillance_7", "surveillance_8", "surveillance_9", "surveillance_10", "surveillance_11", "surveillance_12"]
    techtalk_videos = ["techtalk_1", "techtalk_2", "techtalk_3", "techtalk_4", "techtalk_5", "techtalk_6", "techtalk_7", "techtalk_8", "techtalk_9", "techtalk_10", "techtalk_11"]
    birthday_videos = ["birthday_1", "birthday_2", "birthday_3", "birthday_4", "birthday_5", "birthday_6", "birthday_7", "birthday_8", "birthday_9", "birthday_10"]
    wedding_videos = ["wedding_1", "wedding_2", "wedding_3", "wedding_4", "wedding_5", "wedding_6", "wedding_7", "wedding_8", "wedding_9", "wedding_10"]

    tobe_normalized = ["importanceScore", "megaEventContinuityScore", "diversityTimeScore",
                "diversitySceneScore", "diversityConceptScore", "diversitySimScore"]

    maxvals = {}

    df = pd.read_csv(out)
    if domain == "soccer":
        videos = soccer_videos
    elif domain == "friends":
        videos = friends_videos
    elif domain == "surveillance":
        videos = surveillance_videos
    elif domain == "techtalk":
        videos = techtalk_videos
    elif domain == "birthday":
        videos = birthday_videos
    elif domain == "wedding":
        videos = wedding_videos
    else:
        print("Invalid domain")
        sys.exit()
    
    budgets = [60, 90, 120, 150, 180]

    for video in videos:
        if video not in maxvals:
            maxvals[video] = {}

        for budget in budgets:
            if str(budget) not in maxvals[video]:
                maxvals[video][str(budget)] = {}
            for criteria in tobe_normalized:
                maxval = df[(df['video'] == video) & (
                    df['budget'] == budget)][criteria].max()
                if math.isnan(maxval):
                    print("Some videos are absent. Cant proceed with normalization. Re-run with pre normalization flag turned on")
                    sys.exit()
                if domain == "friends":
                    video_key = video + ".avi"
                else:
                    video_key = video + ".mp4" 
                if norms[video_key][str(budget)][criteria] > maxval:
                    maxval = norms[video_key][str(budget)][criteria]
                df.loc[(df['video'] == video) & (
                        df['budget'] == budget), [criteria]] /= maxval
                print("Video: ", video, " Budget: ", budget)
                print("Maximum value: ", maxval, " for criteria: ", criteria)
                maxvals[video][str(budget)][criteria] = maxval
        
    with open(domain + "_frame_algo_norms.json", 'w') as fp:
        json.dump(maxvals, fp)

    for criteria in tobe_normalized:
        df = df.round({criteria: 4})
    out = domain + "_frame_normalized_master.csv"
    df.to_csv(out)


# read csv file as a list of lists
with open(domain + "_frame_normalized_master.csv", 'r') as read_obj:
    csv_reader = reader(read_obj)
    list_of_rows = list(csv_reader)

for algo in algos:
    master_without_header = []
    for i in range(len(list_of_rows)):
        row = list_of_rows[i]
        #print(row)
        #sys.exit()
        if row[1] == algo:
            temp = map(lambda x:float(x) if not x.isalpha() and "_" not in x and "-" not in x else x, row)
            master_without_header.append(temp)
    #print(master_without_header[0])
    #print(master_without_header[1])
    transposed = map(list, zip(*master_without_header))
    transposed = transposed[4:]
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
    

# master_csv_results.pop(0)
# master_without_header = master_csv_results
# #print(master_without_header)
# transposed = map(list, zip(*master_without_header))
# #print(transposed)
# transposed = transposed[3:]
# #print(transposed)
# minRow = [algo+"-min", "xxx", "xxx"]
# meanRow = [algo+"-mean", "xxx", "xxx"]
# maxRow = [algo+"-max", "xxx", "xxx"]
# for i in range(len(transposed)):
#     min_i = min(transposed[i])
#     mean_i = round(sum(transposed[i])/len(transposed[i]),4)
#     max_i = max(transposed[i])
#     if i == 3 or i == 8:
#         min_i = round(math.sqrt(min_i), 4)
#         mean_i = round(math.sqrt(mean_i), 4)
#         max_i = round(math.sqrt(max_i), 4)
#     minRow.append(min_i)
#     meanRow.append(mean_i)
#     maxRow.append(max_i)
# grand_master_csv_results.append(minRow)
# grand_master_csv_results.append(meanRow)
# grand_master_csv_results.append(maxRow)

# df = pd.read_csv(domain + "_normalized_master.csv")
# for algo in algos:
#     algodf = df[df['configuration'] == algo] 
#     minRow = [algo+"-min", "xxx", "xxx"]
#     meanRow = [algo+"-mean", "xxx", "xxx"]
#     maxRow = [algo+"-max", "xxx", "xxx"]
#     for column in to_compute_min_mean_max:
#         if column == "megaEventContinuityScore" or column == "normalized_vis_cont":
#             minRow.append(round(math.sqrt(algodf[column].min()), 4))
#             meanRow.append(round(math.sqrt(algodf[column].mean()), 4))
#             maxRow.append(round(math.sqrt(algodf[column].max()), 4))
#         else:
#             minRow.append(round(algodf[column].min(), 4))
#             meanRow.append(round(algodf[column].mean(), 4))
#             maxRow.append(round(algodf[column].max(), 4))
#     grand_master_csv_results.append(minRow)
#     grand_master_csv_results.append(meanRow)
#     grand_master_csv_results.append(maxRow)


# Write results to csv file
with open(domain + "_final_frame_normalized_master.csv", "wb") as f:
    writer = csv.writer(f)
    for result in grand_master_csv_results:
        writer.writerow(result)  
    



   
    



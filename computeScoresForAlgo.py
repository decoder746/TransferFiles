import sys
import os
import random
import commands
import csv
import json
import numpy as np
import math
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--path', type=str, help="Master data path")
parser.add_argument('--exe-path', type=str, help="Path to folder containing the eval executable")
parser.add_argument('--domain', type=str, help="Domain")
parser.add_argument('--algos', nargs="*", type=str, help="Comma separated list of algos")
parser.add_argument('--mode', type=str, help="frame or snippet")
parser.add_argument('--vkpath',type=str)
parser.add_argument('--mypath',type=str)
# path = sys.argv[1]
# exe_path = sys.argv[2]
# domain = sys.argv[3]
# algo = sys.argv[4]
args = parser.parse_args()

domainPath = os.path.join(args.path, args.domain)
budgets = [60, 90, 120, 150, 180]

for algo in args.algos:
    print("Computing scores for : ", algo)
    for budget in budgets:
        algoSummariesPath = os.path.join(domainPath, str(budget), algo)
        #Either we directly have summaries in this path, or we have video folders
        files = os.listdir(algoSummariesPath)
        temp = os.path.join(algoSummariesPath, files[0])
        if os.path.isfile(temp):
            summaries = files
            for summary in summaries:
                print("Processing: ", summary)
                video = summary.split(algo)[0][:-1]
                algo_summary_path = os.path.join(algoSummariesPath, summary)
                with open(algo_summary_path, "r") as f:
                    algoSummaryJson = json.load(f)
                if args.mode == "frame":
                    frame_scores = {}
                    #frameEvalCommand = os.path.join(args.exe_path, "GenerateAllEvalNumbers") + "  -summaryJsonOfAVideo " + algo_summary_path + "  -pathToAllHumanSummariesOfThisVideo " + os.path.join(
                        # args.path, args.domain + "/allAutomaticGTSummaries/" + video) + " -keywordJSONFile " + os.path.join(args.path, args.domain + "/" + args.domain + ".json") + " -annotatedJSONFile " + os.path.join(args.path, args.domain + "/" + video + ".json") + " -domain " + args.domain + " -verbose false"
                    frameEvalCommand = os.path.join(args.exe_path, "GenerateFrameEvalNumbers") + "  -summaryJsonOfAVideo " + algo_summary_path + "  -pathToAllHumanSummariesOfThisVideo " + os.path.join(
                    args.mypath, args.domain + "/allAutomaticGTSummaries/" + video) + " -keywordJSONFile " + os.path.join(args.vkpath, args.domain + "/" + args.domain + ".json") + " -annotatedJSONFile " + os.path.join(args.vkpath, args.domain + "/" + video + ".json") + " -domain " + args.domain + " -verbose false"
                    print("Algo summary frame eval: ", frameEvalCommand)
                    result = commands.getoutput(frameEvalCommand)
                    print("Result[1-8]: ", result)
                    results = result.split(" ")
                    results = [float(i) for i in results]
                    frame_scores["avgf1auto"] = results[0]
                    frame_scores["maxf1auto"] = results[1]
                    frame_scores["imp"] = results[2]
                    if not(args.domain == "techtalk"):
                        frame_scores["mega-cont"] = results[3]
                    else:
                        frame_scores["mega-cont"] = 99999
                    frame_scores["div-time"] = results[4]
                    if args.domain == "friends":
                        frame_scores["div-scene"] = results[5]
                    else:
                        frame_scores["div-scene"] = 99999
                    frame_scores["div-concept"] = results[6]
                    frame_scores["div-sim"] = results[7]

                    visContUniformEvalCommand = os.path.join(
                        args.exe_path, "GenerateVisContUniformNumbers") + " -summaryJsonOfAVideo " + algo_summary_path + " -verbose false"
                    print("Algo ContEval: ", visContUniformEvalCommand)
                    visContUniform = commands.getoutput(visContUniformEvalCommand)
                    print("Result[9-10]: ", visContUniform)
                    visContUniformVals = visContUniform.split(" ")
                    visContUniformVals = [float(i) for i in visContUniformVals]
                    frame_scores["norm-vis-cont"] = visContUniformVals[0]
                    frame_scores["norm-uniform"] = visContUniformVals[1]
                
                    algoSummaryJson["frame_scores"] = frame_scores
                    with open(algo_summary_path, 'w') as outfile:
                        json.dump(algoSummaryJson, outfile)
                else:
                    snippet_scores = {}
                    snippetEvalCommand = os.path.join(args.exe_path, "GenerateAllEvalNumbers") + "  -summaryJsonOfAVideo " + algo_summary_path + "  -pathToAllHumanSummariesOfThisVideo " + os.path.join(
                        args.mypath, args.domain + "/allAutomaticGTSummaries/" + video) + " -keywordJSONFile " + os.path.join(args.vkpath, args.domain + "/" + args.domain + ".json") + " -annotatedJSONFile " + os.path.join(args.vkpath, args.domain + "/" + video + ".json") + " -domain " + args.domain + " -verbose false"
                    print("Algo summary snippet eval: ", snippetEvalCommand)
                    result = commands.getoutput(snippetEvalCommand)
                    print("Result[1-8]: ", result)
                    results = result.split(" ")
                    results = [float(i) for i in results]
                    snippet_scores["avgf1auto"] = results[0]
                    snippet_scores["maxf1auto"] = results[1]
                    snippet_scores["imp"] = results[2]
                    if not(args.domain == "techtalk"):
                        snippet_scores["mega-cont"] = results[3]
                    else:
                        snippet_scores["mega-cont"] = 99999
                    snippet_scores["div-time"] = results[4]
                    if args.domain == "friends":
                        snippet_scores["div-scene"] = results[5]
                    else:
                        snippet_scores["div-scene"] = 99999
                    snippet_scores["div-concept"] = results[6]
                    snippet_scores["div-sim"] = results[7]

                    visContUniformEvalCommand = os.path.join(
                        args.exe_path, "GenerateVisContUniformNumbers") + " -summaryJsonOfAVideo " + algo_summary_path + " -verbose false"
                    print("Algo ContEval: ", visContUniformEvalCommand)
                    visContUniform = commands.getoutput(visContUniformEvalCommand)
                    print("Result[9-10]: ", visContUniform)
                    visContUniformVals = visContUniform.split(" ")
                    visContUniformVals = [float(i) for i in visContUniformVals]
                    snippet_scores["norm-vis-cont"] = visContUniformVals[0]
                    snippet_scores["norm-uniform"] = visContUniformVals[1]
                
                    algoSummaryJson["snippet_scores"] = snippet_scores
                    with open(algo_summary_path, 'w') as outfile:
                        json.dump(algoSummaryJson, outfile)
        else:
            videos = files
            for video in videos:
                summariesPath = os.path.join(algoSummariesPath, video)
                summaries = os.listdir(summariesPath)
                for summary in summaries:
                    print("Processing: ", summary)
                    algo_summary_path = os.path.join(summariesPath, summary)
                    with open(algo_summary_path, "r") as f:
                        algoSummaryJson = json.load(f)
                    if args.mode == "frame":
                        frame_scores = {}
                        frameEvalCommand = os.path.join(args.exe_path, "GenerateFrameEvalNumbers") + "  -summaryJsonOfAVideo " + algo_summary_path + "  -pathToAllHumanSummariesOfThisVideo " + os.path.join(
                        args.mypath, args.domain + "/allAutomaticGTSummaries/" + video) + " -keywordJSONFile " + os.path.join(args.vkpath, args.domain + "/" + args.domain + ".json") + " -annotatedJSONFile " + os.path.join(args.vkpath, args.domain + "/" + video + ".json") + " -domain " + args.domain + " -verbose false"
                        print("Algo summary frame eval: ", frameEvalCommand)
                        result = commands.getoutput(frameEvalCommand)
                        print("Result[1-8]: ", result)
                        results = result.split(" ")
                        results = [float(i) for i in results]
                        frame_scores["avgf1auto"] = results[0]
                        frame_scores["maxf1auto"] = results[1]
                        frame_scores["imp"] = results[2]
                        if not(args.domain == "techtalk"):
                            frame_scores["mega-cont"] = results[3]
                        else:
                            frame_scores["mega-cont"] = 99999
                        frame_scores["div-time"] = results[4]
                        if args.domain == "friends":
                            frame_scores["div-scene"] = results[5]
                        else:
                            frame_scores["div-scene"] = 99999
                        frame_scores["div-concept"] = results[6]
                        frame_scores["div-sim"] = results[7]

                        visContUniformEvalCommand = os.path.join(
                            args.exe_path, "GenerateVisContUniformNumbers") + " -summaryJsonOfAVideo " + algo_summary_path + " -verbose false"
                        print("Algo ContEval: ", visContUniformEvalCommand)
                        visContUniform = commands.getoutput(visContUniformEvalCommand)
                        print("Result[9-10]: ", visContUniform)
                        visContUniformVals = visContUniform.split(" ")
                        visContUniformVals = [float(i) for i in visContUniformVals]
                        frame_scores["norm-vis-cont"] = visContUniformVals[0]
                        frame_scores["norm-uniform"] = visContUniformVals[1]
                    
                        algoSummaryJson["frame_scores"] = frame_scores
                        with open(algo_summary_path, 'w') as outfile:
                            json.dump(algoSummaryJson, outfile)
                    else:
                        snippet_scores = {}
                        snippetEvalCommand = os.path.join(args.exe_path, "GenerateAllEvalNumbers") + "  -summaryJsonOfAVideo " + algo_summary_path + "  -pathToAllHumanSummariesOfThisVideo " + os.path.join(
                            args.mypath, args.domain + "/allAutomaticGTSummaries/" + video) + " -keywordJSONFile " + os.path.join(args.vkpath, args.domain + "/" + args.domain + ".json") + " -annotatedJSONFile " + os.path.join(args.vkpath, args.domain + "/" + video + ".json") + " -domain " + args.domain + " -verbose false"
                        print("Algo summary snippet eval: ", snippetEvalCommand)
                        result = commands.getoutput(snippetEvalCommand)
                        print("Result[1-8]: ", result)
                        results = result.split(" ")
                        results = [float(i) for i in results]
                        snippet_scores["avgf1auto"] = results[0]
                        snippet_scores["maxf1auto"] = results[1]
                        snippet_scores["imp"] = results[2]
                        if not(args.domain == "techtalk"):
                            snippet_scores["mega-cont"] = results[3]
                        else:
                            snippet_scores["mega-cont"] = 99999
                        snippet_scores["div-time"] = results[4]
                        if args.domain == "friends":
                            snippet_scores["div-scene"] = results[5]
                        else:
                            snippet_scores["div-scene"] = 99999
                        snippet_scores["div-concept"] = results[6]
                        snippet_scores["div-sim"] = results[7]
                        
                        visContUniformEvalCommand = os.path.join(
                            args.exe_path, "GenerateVisContUniformNumbers") + " -summaryJsonOfAVideo " + algo_summary_path + " -verbose false"
                        print("Algo ContEval: ", visContUniformEvalCommand)
                        visContUniform = commands.getoutput(visContUniformEvalCommand)
                        print("Result[9-10]: ", visContUniform)
                        visContUniformVals = visContUniform.split(" ")
                        visContUniformVals = [float(i) for i in visContUniformVals]
                        snippet_scores["norm-vis-cont"] = visContUniformVals[0]
                        snippet_scores["norm-uniform"] = visContUniformVals[1]
                        
                        algoSummaryJson["snippet_scores"] = snippet_scores
                        with open(algo_summary_path, 'w') as outfile:
                            json.dump(algoSummaryJson, outfile)


    

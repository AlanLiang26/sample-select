import random
import math
import sys
import argparse
import csv

MAX_SAMPLING_TIMES_COUNT = 3000
MAX_LOADED_COUNT = 35000

class Query(object):
    def __init__(self,query,frequency,total_frequency):
        self.query = query
        self.frequency = frequency
        self.begin_frequency = total_frequency
        self.end_frequency = (total_frequency + frequency)

def loadData(queries_file_name):
    queries_file = open(queries_file_name,'r')
    queries = []
    line = queries_file.readline()
    count = 0
    data_count = 0
    total_frequency = 0.0
    while line:
        data_count += 1
        if not data_count%17 == 0:
            line = queries_file.readline()
            continue
        info = line.rstrip('\n').rstrip(' ').lstrip(' ').split(' ')
        #print(info,count)
        length = len(info)
        if length < 2:
            line = queries_file.readline()
            continue
        query = info[1]
        #frequency = math.log(float(info[11]))
        frequency = float(info[0])
        #print(query,frequency)
        count += 1
        queries.append(Query(query,frequency,total_frequency))
        total_frequency += frequency
        line = queries_file.readline()
    queries_file.close()
    return queries,count,total_frequency

def loadCSVData(query_file_name):
    count = 0
    queries = []
    total_frequency = 0.0
    with open(query_file_name, 'r') as f:
        reader = csv.DictReader(x.replace('\0', '') for x in f)
        #reader = csv.DictReader(f)
        for line in reader:
            count += 1
            query = line["query"]
            #frequency = math.log(float(line["uniqueSearch"]))
            frequency = float(line["uniqueSearch"])
            queries.append(Query(query,frequency,total_frequency))
            total_frequency += frequency
            if count >= MAX_LOADED_COUNT:
                break

    return queries,count,total_frequency

def loadFilterData(filter_file_name):
    filter_file = open(filter_file_name,'r')
    queries = {}
    line = filter_file.readline()
    count = 0
    while line:
        count += 1
        info = line.split(",")
        query = info[0]
        queries[query] = 1
        line = filter_file.readline()
    filter_file.close()
    return queries

def tompsonSampling(queries,count,total_frequency,sampling_count,filter_queries):
    sampled_queries = {}
    for i in range(0,MAX_SAMPLING_TIMES_COUNT):
        random_frequency = random.uniform(0.000, total_frequency)
        for j in range(0,count):
            if random_frequency > queries[j].begin_frequency and random_frequency < queries[j].end_frequency:
                if len(sampled_queries) < sampling_count and (not queries[j].query in filter_queries) and (len(queries[j].query) > 5):
                    sampled_queries[queries[j].query] = queries[j].frequency
                if len(sampled_queries) >= sampling_count:
                    break
    return sampled_queries

def reSamplingOldSet(filter_queries,repick_count):
    queries = {}
    old_queries = []
    for key in filter_queries.keys():
        old_queries.append(key)
    while len(queries) < repick_count:
        queries[random.choice(old_queries)] = 1
    return queries


def outPut(sampled_queries,output_file_name):
    queries_file = open(output_file_name,'w')
    sampled_queries= sorted(sampled_queries.items(), key=lambda d:d[1], reverse = True)
    for query in sampled_queries:
        queries_file.write(query[0] + "\n")
        #queries_file.write(query[0]+ "\t" + str(query[1]) + "\n")
    queries_file.close()

if __name__ == "__main__":
    if 3 != sys.version_info.major:
        sys.exit('This tool requires Python 3; exiting!')
    parser = argparse.ArgumentParser(description="query sampling tool,get DCG set and training set")
    parser.add_argument("queries_file")
    #parser.add_argument("filter_file")

    parser.add_argument("samplings_out_file")
    #parser.add_argument("repicked_out_file")

    parser.add_argument("--sampling_count", default=400, type=int, help="")
    #parser.add_argument("--repick_count", default=550, type=int, help="")
    args = parser.parse_args()

    sampling_count = args.sampling_count
    #repick_count = args.repick_count

    #filter_file = args.filter_file
    queries_file = args.queries_file

    samplings_out_file = args.samplings_out_file
    #repicked_out_file = args.repicked_out_file

    #queries,count,total_frequency = loadCSVData(queries_file)
    queries,count,total_frequency = loadData(queries_file)
    print ("Queries Count is %d,Overall Volume is %.1f"%(count,total_frequency))

    #filter_queries = loadFilterData(filter_file)
    #repicked_queries = reSamplingOldSet(filter_queries,repick_count)
    #print("Count of Random Sampling Queries from Old DCG Set is %d"%(len(repicked_queries)))
    filter_queries = {}
    sampled_queries = tompsonSampling(queries,count,total_frequency,sampling_count,filter_queries)
    print("Count Tompson Sampling Queries from User Queries is %d"%(len(sampled_queries)))

    #outPut(repicked_queries,repicked_out_file)
    outPut(sampled_queries,samplings_out_file)

import random
# -*- coding: UTF-8 -*-
#!/usr/bin/python

MAX_SAMPLING_TIMES_COUNT = 3000

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
        # if not data_count%17 == 0:
        #     line = queries_file.readline()
        #     continue
        info = line.split(',')
        #print(info,count)
        length = len(info)
        if length < 2:
            line = queries_file.readline()
            continue
        query = info[0]
        #frequency = math.log(float(info[11]))
        frequency = float(info[1])
        #print(query,frequency)
        count += 1
        queries.append(Query(query,frequency,total_frequency))
        total_frequency += frequency
        line = queries_file.readline()
    queries_file.close()
    return queries,count,total_frequency

def tompsonSampling(queries,count,total_frequency,sampling_count):
    sampled_queries = {}
    for i in range(0,MAX_SAMPLING_TIMES_COUNT):
        if len(sampled_queries) >= sampling_count:
            break
        random_frequency = random.uniform(0.000, total_frequency)
        for j in range(0,count):
            if random_frequency > queries[j].begin_frequency and random_frequency < queries[j].end_frequency:
                if sampled_queries.has_key(queries[j].query):
                    break
                sampled_queries[queries[j].query] = queries[j].frequency
                break
    return sampled_queries

def outPut(sampled_queries,output_file_name):
    queries_file = open(output_file_name,'w')
    # sampled_queries= sorted(sampled_queries.items(), key=lambda d:d[1], reverse = True)
    for query in sampled_queries:
        queries_file.write(query + "\n")
        #queries_file.write(query[0]+ "\t" + str(query[1]) + "\n")
    queries_file.close()

if __name__ == "__main__":
    sampling_count = 300.0
    queries_file = "query_file.txt"
    samplings_out_file ="sampling.txt"
    queries,count,total_frequency = loadData(queries_file)
    print ("Queries Count is %d,Overall Volume is %.1f"%(count,total_frequency))
    sampled_queries = tompsonSampling(queries,count,total_frequency,sampling_count)
    print("Count Tompson Sampling Queries from User Queries is %d"%(len(sampled_queries)))
    outPut(sampled_queries,samplings_out_file)
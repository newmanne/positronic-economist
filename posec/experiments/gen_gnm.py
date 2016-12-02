import json
import redis
import argparse
import random
import os
import glob

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--qname', type=str, help="redis queue", default="gnm")
    parser.add_argument('--host', type=str, help="redis host", default="paxos")
    parser.add_argument('--port', type=int, help="redis port", default=8888)
    args = parser.parse_args()
    r = redis.StrictRedis(host=args.host, port=args.port)

    r.delete(args.qname)
    r.delete(args.qname+'_PROCESSING')

    jobs = []
    for bagg in glob.glob('/ubc/cs/research/arrow/newmanne/positronic-economist/baggs/*/*.bagg'):
        
        if 'approval' not in bagg.lower():
            continue
        if not ('bad' in bagg.lower() and 'final' in bagg.lower()):
            continue


        parts = os.path.basename(bagg).split('.')[0].split('_')
        digits = map(lambda x: x.isdigit(), parts)
        n = int(parts[digits.index(True)])

        for seed in range(1,11):
            print bagg
            jobs.append({'file': bagg, 'seed': seed})    

    random.shuffle(jobs)

    for job in jobs:
        r.rpush(args.qname, json.dumps(job))

    print r.llen(args.qname)

import json
import redis
import argparse
import random

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--qname', type=str, help="redis queue", default="posec")
    parser.add_argument('--host', type=str, help="redis host", default="paxos")
    parser.add_argument('--port', type=int, help="redis port", default=8888)
    args = parser.parse_args()
    r = redis.StrictRedis(host=args.host, port=args.port)

    r.delete(args.qname)
    r.delete(args.qname+'_PROCESSING')

    jobs = []

    #
    # GAME GENERATION
    #

    # for game in ['GSP', 'GFP']:
    #     for n in reversed(range(2,11,2)):
    #         for seed in range(1,11):
    #             job = {'game': game, 'n': n, 'seed': seed, 'bbsi_level': 1}
    #             jobs.append(job)

    # for game in ['GSP_bad', 'GFP_bad']:
    #     for n in range(2,11,2):
    #        for seed in range(1,11):
    #             job = {'game': game, 'n': n, 'seed': seed, 'bbsi_level': 1}
    #             jobs.append(job)

    # for n in range(2,10):
    #    for seed in range(1,11):
    #        job = {'game': 'vote', 'n': n, 'seed': seed, 'bbsi_level': 1}
    #        jobs.append(job)

    # for n in range(2,11):
    #    for seed in range(1,11):
    #        job = {'game': 'vote_bad', 'n': n, 'seed': seed, 'bbsi_level': 1}
    #        jobs.append(job)

    #
    # SOLVERS
    #
    # for alg in ['IBR', 'FP']:
    #     for game in ['GSP', 'GFP', 'TWO_APPROVAL']:
    #         for n in [10]:
    #             for seed in range(1,11):
    #                 for alg_seed in range(1,11):
    #                     output = './%s/%s_n=%d_seed=%d_algseed=%d.txt' % (alg, game, n, seed, alg_seed)
    #                     agg_file = '/ubc/cs/research/arrow/newmanne/positronic-economist/baggs/%s/%s.bagg' % (game, '_'.join([game.lower(), str(n), str(seed), '1', 'FINAL']))
    #                     job = {'alg': alg, 'agg_file': agg_file, 'alg_seed': alg_seed, 'output': output, 'cutoff': 3600}
    #                     jobs.append(job)

    for alg in ['IBR']:
        for game in ['TWO_APPROVAL', 'GFP']:
            for n in range(2,10):
                for seed in range(1,11):
                    for alg_seed in range(1,11):
                        output = './%s/%s_n=%d_seed=%d_algseed=%d.txt' % (alg, game, n, seed, alg_seed)
                        agg_file = '/ubc/cs/research/arrow/newmanne/positronic-economist/baggs/%s/%s.bagg' % (game, '_'.join([game.lower(), str(n), str(seed), '1', 'FINAL']))
                        job = {'alg': alg, 'agg_file': agg_file, 'alg_seed': alg_seed, 'output': output, 'cutoff': 3600}
                        jobs.append(job)

    # random.shuffle(jobs)

    for job in jobs:
        r.lpush(args.qname, json.dumps(job))
    print r.llen(args.qname)

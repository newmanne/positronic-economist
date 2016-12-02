import os
import redis
import argparse
import logging
import json
import subprocess

def run_shell_command(command):
    subprocess.check_call(command, shell=True)

def test():
    pass

OUTDIR = "output"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--qname', type=str, help="redis queue", default="gnm")
    parser.add_argument('--host', type=str, help="redis host", default="paxos")
    parser.add_argument('--port', type=int, help="redis port", default=8888)
    args = parser.parse_args()

    if not (args.qname and args.host and args.port):
        test()
    else:
        r = redis.StrictRedis(host=args.host, port=args.port)
        q = args.qname

        logging.basicConfig(format='%(asctime)-15s [%(levelname)s] %(message)s', level=logging.INFO)
        logging.getLogger().addHandler(logging.StreamHandler())

        while True:
            remaining_jobs = r.llen(q)
            logging.info("There are %d jobs remaining" % (remaining_jobs))
            instance = r.rpoplpush(q, q + '_PROCESSING')
            if instance is None:
                break
            job = json.loads(instance)
            logging.info("Running job %s" % job)

            if not os.path.exists(OUTDIR):
                os.makedirs(OUTDIR)

            print os.path.basename(job['file'])

            output = os.path.join(OUTDIR, os.path.basename(job['file']).split('.')[0] + '_' + str(job['seed']) + '.output')
            try:
                run_shell_command("(/ubc/cs/research/arrow/satfc/runsolver/runsolver -C 3600 /ubc/cs/research/arrow/satfc/AGGSolver/gnm_agg -f %s %s 1) &> %s" % (job['file'], job['seed'], output))
            except Exception:
                pass
            r.lrem(q + '_PROCESSING', 1, instance)
        print "ALL DONE!"

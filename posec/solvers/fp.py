import logging
import os
import random

import numpy as np

from posec.solvers.ibr_bagg import random_idx_max
from posec.pyagg import AGG_File
import time

logger = logging.getLogger(__name__)

def uniform_mixed_strategy(agg):
    strategies = []
    for size in agg.aSizes:
        strategy = [1. / size] * size
        strategies.append(strategy)
    return strategies

def normalize(v):
    norm=np.linalg.norm(v, ord=1)
    return v/norm

def normalize_model(model):
    return map(normalize, model)

def FP(agg, seed=None, output=None, cutoff=3600):
    start = time.time()

    random.seed(seed)

    file = output if output is not None else os.devnull

    with open(file, 'w') as f:
        f.write('max_regret,weighted_max_regret,cputime\n')

        def log_strategy(s, regrets=None):
            max_regret = max(map(max, regrets)) if regrets is not None else agg.max_regret(s)
            elapsed = time.time()-start
            weighted_max_regret = max_regret / agg.max_payoff
            f.write(','.join((str(max_regret), str(max_regret/agg.max_payoff), str(elapsed)))+'\n')
            logger.info("Weighted max regret overall is %s. Time elapsed %.2f" % (weighted_max_regret, elapsed))

        model = uniform_mixed_strategy(agg)
        strategy = model
        iteration = 0
        while not agg.isNE(strategy) and time.time() - start < cutoff:
            # Get everyone's current regret given the model's count frequencies as empirical mixed strategy
            regrets = agg.regret(strategy, asLL=True)
            log_strategy(strategy, regrets=regrets)

            # Calculate each player's best response, update that count by 1. Break ties randomly
            for i in range(len(agg.N)):
                best_response = random_idx_max(regrets[i])
                model[i][best_response] += 1

            strategy = normalize_model(model)

            iteration += 1

        log_strategy(strategy)
        # Either cutoff or NE
        if agg.isNE(strategy):
            logger.info("NE FOUND at iteration %d after %.2f" % (iteration, time.time() - start))
            logger.info(strategy)
        else:
            logger.info("Cutoff reached")

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)-15s [%(levelname)s] %(message)s', level=logging.INFO, filename='posec.log')
    logging.getLogger().addHandler(logging.StreamHandler())
    for n in range(1,11):
        path = '/ubc/cs/research/arrow/newmanne/positronic-economist/baggs/TWO_APPROVAL/'
        agg = AGG_File(path + 'two_approval_10_' + str(n) + '_1_FINAL.bagg')
        FP(agg)
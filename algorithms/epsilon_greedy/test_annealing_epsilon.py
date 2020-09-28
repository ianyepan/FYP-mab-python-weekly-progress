execfile("imports.py")

import random

random.seed(1)
means = [0.1, 0.1, 0.1, 0.1, 0.9]
n_arms = len(means)
random.shuffle(means)
arms = map(lambda mu: BernoulliArm(mu), means)
print("Best arm is " + str(argmax(means)))

my_algo = AnnealingEpsilonGreedy([], [])
my_algo.initialize(n_arms)
results = test_algorithm(my_algo, arms, 5000, 250)

with open("algorithms/epsilon_greedy/annealing_results.tsv", "w") as f:
  for i in range(len(results[0])):
    f.write("\t".join([str(results[j][i]) for j in range(len(results))]) + "\n")

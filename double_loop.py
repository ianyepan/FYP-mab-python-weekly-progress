#!/usr/bin/env python3
import random
import matplotlib.pyplot as plt
from arms.bernoulli import BernoulliArm
from arms.normal import NormalArm
from algorithms.epsilon_greedy.standard_epsilon import EpsilonGreedy
from algorithms.epsilon_greedy.annealing_epsilon import AnnealingEpsilonGreedy
from algorithms.softmax.standard_softmax import Softmax
from algorithms.softmax.annealing_softmax import AnnealingSoftmax
from algorithms.ucb.ucb1 import UCB1
from algorithms.ucb.ucb_bayesian import UCB_Bayesian
from algorithms.exp3.exp3 import Exp3
import numpy as np

from matplotlib import rcParams
rcParams['font.family'] = ['Roboto']
for w in ["font.weight", "axes.labelweight", "axes.titleweight", "figure.titleweight"]:
  rcParams[w] = 'regular'


def argmax(arr):
  return arr.index(max(arr))


def change_distribution():
  """Change the underlying reward distributions each arm follows."""
  arm1 = NormalArm(1.0, 2)
  arm2 = NormalArm(0.6, 2)
  arm3 = NormalArm(0.7, 2)
  arm4 = NormalArm(0.4, 2)
  arm5 = NormalArm(0.3, 2)
  arm6 = NormalArm(0.2, 2)
  arm7 = NormalArm(0.1, 2)
  arm8 = NormalArm(0.5, 2)
  arm9 = NormalArm(0.5, 2)
  arm10 = NormalArm(0.5, 2)
  return [arm1, arm2, arm3, arm4, arm5, arm6, arm7, arm8, arm9, arm10]


def plot_graph(timesteps, arms, algorithms, algorithm_rewards, algorithm_cum_rewards, algorithm_arm_selections, max_mu,
               max_cum_reward, change_of_distribution):
  """Plot a 3-row k-column graph with rolling average, cumulative reward and arm selection scatter plot."""
  num_of_algo = len(algorithms)

  plt.figure(figsize=(15, 10))
  for i, algo in enumerate(algorithms):
    plt.subplot(3, num_of_algo, i + 1)
    plt.plot(algorithm_rewards[i], label='Average rewards', color='palevioletred', alpha=0.8)
    if change_of_distribution:
      plt.axvline(x=timesteps/2, color='salmon', alpha=.5)
    plt.xlabel('Time-step t', fontsize=12)
    plt.ylabel(f'Avg. reward for {algo.get_name()}', fontsize=12)
    plt.title(f"{algo.get_name()}\nRolling Average Reward", fontsize=13)
    plt.axis([0, timesteps, 0, max_mu + 0.1])

    plt.subplot(3, num_of_algo, i + 1 + num_of_algo)
    plt.plot(algorithm_cum_rewards[i], label='Cumulative reward', color='orange', alpha=0.8)
    if change_of_distribution:
      plt.axvline(x=timesteps/2, color='salmon', alpha=.5)
    plt.xlabel('Time-step t', fontsize=12)
    plt.ylabel(f'Cum. reward for {algo.get_name()}', fontsize=12)
    plt.title(f"Cumulative Reward", fontsize=13)
    plt.axis([0, timesteps, 0, max_cum_reward])

    plt.subplot(3, num_of_algo, i + 1 + 2*num_of_algo)
    plt.scatter(range(timesteps - 1), algorithm_arm_selections[i], s=.1, color='salmon', alpha=.5)
    plt.axis([0, timesteps, 0, len(arms) + 1])
    if change_of_distribution:
      plt.axvline(x=timesteps/2, color='salmon', alpha=.5)
    plt.xlabel('Time-step t', fontsize=12)
    plt.ylabel(f'{algo.get_name()}\'s arm selection', fontsize=12)
    plt.title("Arm selection scatter plot", fontsize=13)

  plt.tight_layout(pad=2.0)
  # plt.savefig('./figures/graph_demo.png')
  plt.show()


def plot_cum_rewards(algorithms, algorithm_cum_rewards, timesteps, max_cum_reward):
  """Cumulative rewards of k algorithms in 1 line graph."""
  plt.figure()
  for i in range(len(algorithms)):
    plt.plot(algorithm_cum_rewards[i], label='Cumulative reward', alpha=0.8)
  plt.legend([algo.get_name() for algo in algorithms])
  plt.xlabel('Time-step t', fontsize=12)
  plt.ylabel(f'Cum. reward comparisons', fontsize=12)
  plt.title(f"Cumulative Reward", fontsize=13)
  plt.axis([0, timesteps, 0, max_cum_reward])
  # plt.savefig('./figures/cum_rewards.png')
  plt.show()


def main():
  arm1 = NormalArm(0.2, 1)
  arm2 = NormalArm(0.3, 1)
  arm3 = NormalArm(0.4, 1)
  arm4 = NormalArm(0.5, 1)
  arm5 = NormalArm(0.6, 1)
  arm6 = NormalArm(0.7, 1)
  arm7 = NormalArm(0.6, 1)
  arm8 = NormalArm(0.5, 1)
  arm9 = NormalArm(0.4, 1)
  arm10 = NormalArm(0.1, 1)
  arms = [arm1, arm2, arm3, arm4, arm5, arm6, arm7, arm8, arm9, arm10]
  max_mu = max([arm.mu for arm in arms])
  n_arms = len(arms)
  print(f'Optimal arm: #{argmax([arm.mu for arm in arms]) + 1}')
  change_of_distribution = False

  algo_epsilon = EpsilonGreedy(0.05, n_arms)
  algo_anneal_epsilon = AnnealingEpsilonGreedy(n_arms)
  algo_ucb1 = UCB1(n_arms)
  algo_ucb_bayesian = UCB_Bayesian(1.96, n_arms)  # 95% confident
  algo_softmax = Softmax(.2, n_arms)
  algo_anneal_softmax = AnnealingSoftmax(n_arms)
  algo_exp3 = Exp3(.2, n_arms)

  algorithms = [algo_softmax, algo_anneal_softmax, algo_exp3]
  algorithm_rewards = []  # 2D list[algo][t] (array of running avg. rewards for each algo at time-step t)
  algorithm_cum_rewards = []  # 2D list[algo][t] (array of cumulative rewards for each algo at time-step t)
  algorithm_arm_selections = []  # 2D list[algo][t] (array of arm selections for each algo at time-step t)

  # semi-global variables
  timesteps = 1000  # number of time-steps (T)
  total_iteration = 20  #outer-loop
  reward_round_iteration = np.zeros((timesteps), dtype=int)

  for algo in algorithms:
    avg_rewards, cum_rewards, arm_selections = [0], [0], []

    for i in range(total_iteration):
      for t in range(1, timesteps):
        chosen_arm = algo.select_arm()
        arm_selections.append(chosen_arm + 1)  # convert 0-based index to 1-based
        reward = arms[chosen_arm].draw_reward()
        reward_round_iteration[t] += reward  # This persists over total_iterations
        new_avg = (avg_rewards[-1]*(t - 1) + reward)/t  # new running avg.
        avg_rewards.append(new_avg)
        cum_rewards.append(new_avg*t)
        algo.update(chosen_arm, reward)
      algorithm_rewards.append(avg_rewards)
      algorithm_cum_rewards.append(cum_rewards)
      algorithm_arm_selections.append(arm_selections)

      # Resetting variable
      arm_selections = []

    # Compute average rewards for each iteration
    average_reward_in_each_round = np.zeros(timesteps, dtype=float)

    # Calculate the values for one good 1000 rounds
    # Squash 200X1000 -> 1X1000
    for t in range(timesteps):
      average_reward_in_each_round[t] = float(reward_round_iteration[t])/float(total_iteration)

    cumulative_optimal_reward = 0.0
    cumulative_reward = 0.0
    x_axis = np.zeros(timesteps, dtype=int)
    regrets = np.zeros(timesteps, dtype=float)  # regret for each round

    for t in range(timesteps):
      x_axis[t] = t
      cumulative_optimal_reward += max_mu
      cumulative_reward += average_reward_in_each_round[t]
      regrets[t] = cumulative_optimal_reward - cumulative_reward

    # print('After ', regret is: ', cumulative_optimal_reward - cumulative_reward)
    print(f"The average regret for {algo.get_name()} is {cumulative_optimal_reward - cumulative_reward}")

  max_cum_reward = max([algorithm_cum_rewards[i][-1] for i in range(len(algorithms))])
  for i in range(len(algorithms)):
    print(f"{algorithms[i].get_name()}: {algorithm_cum_rewards[i][-1]:.2f}")

  plot_graph(timesteps, arms, algorithms, algorithm_rewards, algorithm_cum_rewards, algorithm_arm_selections, max_mu,
             max_cum_reward, change_of_distribution)
  plot_cum_rewards(algorithms, algorithm_cum_rewards, timesteps, max_cum_reward)


if __name__ == "__main__":
  main()
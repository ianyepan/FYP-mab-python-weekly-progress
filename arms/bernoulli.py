import random


class BernoulliArm():
  def __init__(self, mu):
    self.mu = mu

  def draw_reward(self):
    return 0.0 if random.random() > self.mu else 1.0

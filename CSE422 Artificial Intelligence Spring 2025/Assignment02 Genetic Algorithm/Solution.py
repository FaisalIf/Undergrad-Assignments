import random

def get_fitness(item):
   return item[1]

class Strategy:
   def __init__(self, stop_loss, take_profit, trade_size):
      self.stop_loss = stop_loss
      self.take_profit = take_profit
      self.trade_size = trade_size

   def get_genes(self):
      return [self.stop_loss, self.take_profit, self.trade_size]

   def process_trade(self, current_capital, price_change):
      trade_amount = current_capital * (self.trade_size / 100.0)
      if price_change <= -self.stop_loss:
         effective_change = -self.stop_loss
      elif price_change >= self.take_profit:
         effective_change = self.take_profit
      else:
         effective_change = price_change
      return current_capital + trade_amount * (effective_change / 100.0)

   def compute_fitness(self, price_history, initial_capital=1000):
      capital = initial_capital
      for change in price_history:
         capital = self.process_trade(capital, change)
      return round(capital - initial_capital, 2)

   def apply_mutation(self, mutation_rate=0.05):
      if random.random() < mutation_rate:
         self.stop_loss = round(max(1.0, min(99.0, self.stop_loss + random.uniform(-1, 1))), 2)
      if random.random() < mutation_rate:
         self.take_profit = round(max(1.0, min(99.0, self.take_profit + random.uniform(-1, 1))), 2)
      if random.random() < mutation_rate:
         self.trade_size = round(max(1.0, min(99.0, self.trade_size + random.uniform(-1, 1))), 2)
      return self

   def clone(self):
      return Strategy(self.stop_loss, self.take_profit, self.trade_size)

   def to_dict(self):
      return {"stop_loss": self.stop_loss, "take_profit": self.take_profit, "trade_size": self.trade_size}

class GAOptimizer:
   def __init__(self, initial_population, price_history, generations=10, mutation_rate=0.05):
      self.price_history = price_history
      self.generations = generations
      self.mutation_rate = mutation_rate
      self.population = self.initialize_population(initial_population)

   def initialize_population(self, population_data):
      population_list = []
      for individual in population_data:
         population_list.append(Strategy(**individual))
      return population_list

   def evaluate_population(self, starting_capital=1000):
      evaluated = []
      for strategy in self.population:
         fitness_value = strategy.compute_fitness(self.price_history, starting_capital)
         evaluated.append((strategy, fitness_value))
      return evaluated

   def select_elites(self, evaluated_population, elite_count=2):
      evaluated_population.sort(key=get_fitness, reverse=True)
      elites = []
      for idx in range(elite_count):
         elites.append(evaluated_population[idx][0].clone())
      return elites

   def select_random_parents(self):
      parent1 = random.choice(self.population).clone()
      parent2 = random.choice(self.population).clone()
      return parent1, parent2

   def single_point_crossover(self, parent1, parent2):
      genes1 = parent1.get_genes()
      genes2 = parent2.get_genes()
      split_index = random.choice([0, 1])
      child1_genes = genes1[:split_index + 1] + genes2[split_index + 1:]
      child2_genes = genes2[:split_index + 1] + genes1[split_index + 1:]
      return Strategy(*child1_genes), Strategy(*child2_genes)

   def two_point_crossover(self, parent1, parent2):
      genes1 = parent1.get_genes()
      genes2 = parent2.get_genes()
      point1, point2 = sorted(random.sample(range(len(genes1)), 2))
      child1_genes = genes1[:point1] + genes2[point1:point2] + genes1[point2:]
      child2_genes = genes2[:point1] + genes1[point1:point2] + genes2[point2:]
      return Strategy(*child1_genes), Strategy(*child2_genes)

   def create_offspring(self):
      parent_a, parent_b = self.select_random_parents()
      offspring1, offspring2 = self.single_point_crossover(parent_a, parent_b)
      offspring1.apply_mutation(self.mutation_rate)
      offspring2.apply_mutation(self.mutation_rate)
      return offspring1, offspring2

   def evolve_population(self, starting_capital=1000):
      for generation in range(self.generations):
         evaluated = self.evaluate_population(starting_capital)
         elites = self.select_elites(evaluated, elite_count=2)
         child1, child2 = self.create_offspring()
         self.population = elites + [child1, child2]

   def run(self, starting_capital=1000):
      self.evolve_population(starting_capital)
      evaluated = self.evaluate_population(starting_capital)
      best_strategy, best_profit = max(evaluated, key=get_fitness)
      return best_strategy.to_dict(), best_profit

   def perform_two_point_crossover(self):
      parent1, parent2 = random.sample(self.population, 2)
      child1, child2 = self.two_point_crossover(parent1, parent2)
      return child1, child2

class GAIO:
   def __init__(self):
      self.initial_population = self.generate_initial_population()
      self.historical_prices = [-1.2, 3.4, -0.8, 2.1, -2.5, 1.7, -0.3, 5.8, -1.1, 3.5]
      self.generations = 10
      self.mutation_rate = 0.05
      self.starting_capital = 1000

   def generate_initial_population(self):
      population = []
      for i in range(4):
         individual = {
            "stop_loss": random.randint(1, 99),
            "take_profit": random.randint(1, 99),
            "trade_size": random.randint(1, 99)
         }
         population.append(individual)
      return population

   def run_ga(self):
      optimizer = GAOptimizer(self.initial_population, self.historical_prices, self.generations, self.mutation_rate)
      best_strategy, final_profit = optimizer.run(self.starting_capital)
      offspring_a, offspring_b = optimizer.perform_two_point_crossover()
      self.print_results(best_strategy, final_profit, offspring_a, offspring_b)

   def print_results(self, best_strategy, final_profit, offspring_a, offspring_b):
      print("Best Strategy:", best_strategy)
      print("Final Profit:", final_profit)
      print("Offspring from two-point crossover:")
      print("Offspring A:", offspring_a.to_dict())
      print("Offspring B:", offspring_b.to_dict())

trade = GAIO()
trade.run_ga()
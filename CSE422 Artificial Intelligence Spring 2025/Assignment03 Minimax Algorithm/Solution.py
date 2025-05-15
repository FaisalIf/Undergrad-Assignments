import math
import random

def generate_moves(n, current=None):
    if current is None:
        current = []
    if len(current) == n:
        yield tuple(current)
    else:
        for move in [0, 1]:
            yield from generate_moves(n, current + [move])

class GameUtils:
    def calc_strength(self, base_value):
        return math.log2(base_value + 1) + base_value / 10.0

    def compute_base_utility(self, max_base, min_base):
        return self.calc_strength(max_base) - self.calc_strength(min_base)

    def build_game_tree(self, base_utility, depth_limit=5):
        tree = {}
        for moves in generate_moves(depth_limit):
            adjust = random.uniform(0.1, 1.0)
            tree[moves] = base_utility + adjust if random.choice([True, False]) else base_utility - adjust
        return tree

class StandardMax:
    def get_value(self, tree, depth, alpha, beta, path, depth_limit=5):
        if self.is_terminal(depth, depth_limit):
            return self.terminal_value(tree, path)
        return self.evaluate_max(tree, depth, alpha, beta, path, depth_limit)
    
    def is_terminal(self, depth, depth_limit):
        return depth == depth_limit
    
    def terminal_value(self, tree, path):
        return tree[path]
    
    def evaluate_max(self, tree, depth, alpha, beta, path, depth_limit):
        best = -float('inf')
        for action in [0, 1]:
            new_path = self.extend_path(path, action)
            value = StandardMin().get_value(tree, depth + 1, alpha, beta, new_path, depth_limit)
            best = max(best, value)
            if best >= beta:
                break
            alpha = max(alpha, best)
        return best

    def extend_path(self, path, action):
        return path + (action,)

class StandardMin:
    def get_value(self, tree, depth, alpha, beta, path, depth_limit=5):
        if self.is_terminal(depth, depth_limit):
            return self.terminal_value(tree, path)
        return self.evaluate_min(tree, depth, alpha, beta, path, depth_limit)
    
    def is_terminal(self, depth, depth_limit):
        return depth == depth_limit
    
    def terminal_value(self, tree, path):
        return tree[path]
    
    def evaluate_min(self, tree, depth, alpha, beta, path, depth_limit):
        best = float('inf')
        for action in [0, 1]:
            new_path = self.extend_path(path, action)
            value = StandardMax().get_value(tree, depth + 1, alpha, beta, new_path, depth_limit)
            best = min(best, value)
            if best <= alpha:
                break
            beta = min(beta, best)
        return best
         
    def extend_path(self, path, action):
        return path + (action,)

class MindControlMax:
    def get_value(self, tree, depth, alpha, beta, path, depth_limit=5):
        if self.is_terminal(depth, depth_limit):
            return self.terminal_value(tree, path)
        return self.evaluate_mind_control(tree, depth, alpha, beta, path, depth_limit)
    
    def is_terminal(self, depth, depth_limit):
        return depth == depth_limit
    
    def terminal_value(self, tree, path):
        return tree[path]
    
    def evaluate_mind_control(self, tree, depth, alpha, beta, path, depth_limit):
        best = -float('inf')
        for action in [0, 1]:
            new_path = self.extend_path(path, action)
            value = self.get_value(tree, depth + 1, alpha, beta, new_path, depth_limit)
            best = max(best, value)
            if best >= beta:
                break
            alpha = max(alpha, best)
        return best
    
    def extend_path(self, path, action):
        return path + (action,)

class ChessMasters:
    def __init__(self, starter, base_carlsen, base_caruana):
        self.initial_starter = starter
        self.carlsen_strength = base_carlsen
        self.caruana_strength = base_caruana
        self.game_starters = [starter, 1 - starter, starter, 1 - starter]
        self.results = {'Carlsen': 0, 'Caruana': 0, 'Draw': 0}
        self.game_utils = GameUtils()

    def setup_players(self, game_index):
        current_starter = self.game_starters[game_index]
        if current_starter == 0:
            return self.carlsen_strength, self.caruana_strength, "Magnus Carlsen", "Fabiano Caruana", current_starter
        else:
            return self.caruana_strength, self.carlsen_strength, "Fabiano Caruana", "Magnus Carlsen", current_starter

    def get_minimax_value(self, max_base, min_base):
        base_util = self.game_utils.compute_base_utility(max_base, min_base)
        tree = self.game_utils.build_game_tree(base_util)
        value = StandardMax().get_value(tree, 0, -float('inf'), float('inf'), ())
        return round(value, 2)

    def update_results(self, minimax_val, current_starter, max_name, min_name):
        if minimax_val > 0:
            if current_starter == 0:
                self.results['Carlsen'] += 1
            else:
                self.results['Caruana'] += 1
            return max_name, "(Max)"
        elif minimax_val < 0:
            if current_starter == 0:
                self.results['Caruana'] += 1
            else:
                self.results['Carlsen'] += 1
            return min_name, "(Min)"
        else:
            self.results['Draw'] += 1
            return "Draw", ""

    def play_single_game(self, game_index):
        max_base, min_base, max_name, min_name, current_starter = self.setup_players(game_index)
        minimax_val = self.get_minimax_value(max_base, min_base)
        winner, label = self.update_results(minimax_val, current_starter, max_name, min_name)
        print(f"Game {game_index + 1} Winner: {winner} {label} (Utility value: {minimax_val:.2f})")

    def play_all_games(self):
        print("Problem 1: Chess Masters")
        for i in range(4):
            self.play_single_game(i)
        print("\nOverall Results:")
        print(f"Magnus Carlsen Wins: {self.results['Carlsen']}")
        print(f"Fabiano Caruana Wins: {self.results['Caruana']}")
        print(f"Draws: {self.results['Draw']}")
        if self.results['Carlsen'] > self.results['Caruana']:
            print("Overall Winner: Magnus Carlsen")
        elif self.results['Caruana'] > self.results['Carlsen']:
            print("Overall Winner: Fabiano Caruana")
        else:
            print("Overall Winner: Draw")

class ChessNoobsWithMagic:
    def __init__(self, starter, cost, base_light, base_L):
        self.starter = starter
        self.cost = cost
        self.light_strength = base_light
        self.L_strength = base_L
        self.game_utils = GameUtils()

    def setup_players(self):
        if self.starter == 0:
            return self.light_strength, self.L_strength, "Light"
        else:
            return self.L_strength, self.light_strength, "L"

    def compute_values(self, max_base, min_base):
        base_util = self.game_utils.compute_base_utility(max_base, min_base)
        tree = self.game_utils.build_game_tree(base_util)
        standard = round(StandardMax().get_value(tree, 0, -float('inf'), float('inf'), ()), 2)
        mind_control = round(MindControlMax().get_value(tree, 0, -float('inf'), float('inf'), ()), 2)
        return standard, mind_control, round(mind_control - self.cost, 2)

    def print_recommendation(self, standard, mind_after, max_name):
        if standard > 0:
            print(f"{max_name} should NOT use Mind Control as the position is already winning.")
        else:
            if mind_after > 0:
                print(f"{max_name} should use Mind Control.")
            else:
                if mind_after > standard:
                    print(f"{max_name} should NOT use Mind Control as it backfires.")
                else:
                    print(f"{max_name} should NOT use Mind Control as the position is losing either way.")

    def play_game(self):
        print("\nProblem 2: Chess Noobs with Magic")
        max_base, min_base, max_name = self.setup_players()
        standard, mind_control, mind_after = self.compute_values(max_base, min_base)
        print(f"\nMinimax value without Mind Control: {standard:.2f}")
        print(f"Minimax value with Mind Control: {mind_control:.2f}")
        print(f"Minimax value with Mind Control after incurring the cost: {mind_after:.2f}")
        self.print_recommendation(standard, mind_after, max_name)

class ChessRunner:
    def run_chess_masters(self):
        print("\nProblem 1: Chess Masters")
        starter = int(input("Enter starting player for game 1 (0 for Carlsen, 1 for Caruana): "))
        carlsen_base = float(input("Enter base strength for Carlsen: "))
        caruana_base = float(input("Enter base strength for Caruana: "))
        game = ChessMasters(starter, carlsen_base, caruana_base)
        game.play_all_games()

    def run_chess_noobs_magic(self):
        print("\nProblem 2: Chess Noobs with Magic")
        starter = int(input("Enter who goes first (0 for Light, 1 for L): "))
        cost = float(input("Enter the cost of using Mind Control: "))
        light_base = float(input("Enter base strength for Light: "))
        L_base = float(input("Enter base strength for L: "))
        game = ChessNoobsWithMagic(starter, cost, light_base, L_base)
        game.play_game()

runner = ChessRunner()

# problem 1
runner.run_chess_masters()
# problem 2
runner.run_chess_noobs_magic()
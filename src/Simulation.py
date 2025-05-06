from Facility_Location_Game import FLG_environment
from Tools import Tools
from Best_Response_Dynamics import BRD

import copy
import numpy as np
import matplotlib.pyplot as plt

class Simulation():

    def __init__(self, n_nodes, n_potential_facilities, n_brd_players, max_iterations, n_simulations, seed):

        self.n_nodes = n_nodes
        self.n_potential_facilities = n_potential_facilities
        self.n_brd_players = n_brd_players
        self.max_iterations = max_iterations
        self.seed = seed
        self.n_simulations = n_simulations
        self.main_rng = np.random.default_rng(seed=self.seed)

        self.setup_simulation()


    def setup_simulation(self):

        # Generate the FLG environment
        self.FLG_env = FLG_environment(self.n_nodes, self.n_potential_facilities, seed=self.seed)
        assert all(isinstance(node, int) for node in self.FLG_env.graph.nodes()) # Check that nodes were correctly generated (Just in case)

        # Calculate all distances between nodes using Dijkstra's algorithm for computational efficiency
        self.distances = Tools().calculate_distance_matrix(self.FLG_env.graph)

        # Setup the BRD players
        self.BRD_setup = BRD(self.n_brd_players, self.distances, self.FLG_env, seed=self.seed)


    def run_FLG_BRD_simulation(self):

        # Best Response Dynamics process
        players_find_best_response = [True] * self.n_brd_players

        iterations = 0
        potential_function_development = [] # Track how the potential function changes over time        
        players_development_over_time = [] # Track players' assignments over time
        while any(players_find_best_response) and iterations < self.max_iterations:

            # Actual process
            turn_of_player = self.main_rng.choice(tuple(range(self.n_brd_players))) # Randomly select a player to find their best response
            updated = self.BRD_setup.find_best_response(turn_of_player)
            if updated:
                players_find_best_response = [True] * self.n_brd_players  # Force recheck all players
            else:
                players_find_best_response[turn_of_player] = False

            # Simulation development study
            iterations += 1
            potential_function_current_value = self.BRD_setup.calculate_potential_function()
            potential_function_development.append(potential_function_current_value)

            snapshot = {pid: copy.deepcopy(data) for pid, data in self.BRD_setup.players.items()}
            players_development_over_time.append(snapshot)

        # When the while loop ends it means that all player were not capable of finding a best response so the Nash Equilibrium is reached

        return iterations, potential_function_development, players_development_over_time
    

    def show_simulation_results(self, iterations, potential_function_development, players_development_over_time, plot_results=False):

        # Show the results of the simulation
        print(f"Simulation completed in {iterations} iterations")

        print("Final players' positions:")
        for player_id, player_data in players_development_over_time[-1].items():
            print(f"Player {player_id}: Facility Position: {player_data['facility_position']}, Utility: {player_data['Utility']}")

        print(f"Final Potential Function value: {potential_function_development[-1]}")

        if plot_results:

            # Plotting simulation development
            plt.figure(figsize=(10, 12))

            # Plot development of the Potential Function Over Time
            plt.subplot(3, 1, 1)  # 3 rows, 1 column, position 1
            plt.plot(potential_function_development, marker='o')
            plt.title("Potential Function Over Time")
            plt.xlabel("Iteration")
            plt.ylabel("Potential Function Value")
            plt.grid(True)

            # Data for the other two plots
            player_facility_positions = {pid: [] for pid in range(self.n_brd_players)}
            player_utilities = {pid: [] for pid in range(self.n_brd_players)}

            for snapshot in players_development_over_time:
                for pid, data in snapshot.items():
                    player_facility_positions[pid].append(data['facility_position'])
                    player_utilities[pid].append(data['Utility'])

            # Plot development of the Facility Positions Over Time
            plt.subplot(3, 1, 2)  # Position 2
            for pid, positions in player_facility_positions.items():
                plt.plot(positions, label=f'Player {pid}', marker='o')
            plt.title("Facility Positions Over Time")
            plt.xlabel("Iteration")
            plt.ylabel("Facility ID")
            plt.legend()
            plt.grid(True)

            # Plot development of the Utility Over Time
            plt.subplot(3, 1, 3)  # Position 3
            for pid, utils in player_utilities.items():
                plt.plot(utils, label=f'Player {pid}', marker='x')
            plt.title("Utility Over Time")
            plt.xlabel("Iteration")
            plt.ylabel("Utility")
            plt.legend()
            plt.grid(True)


            plt.tight_layout()
            plt.show()
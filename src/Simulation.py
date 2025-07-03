from Facility_Location_Game import FLG_environment
from tools.algorithm_tools import Tools
from Best_Response_Dynamics import BRD

import copy
import numpy as np
import matplotlib.pyplot as plt
import statistics as stats

class Simulation():

    def __init__(self, n_nodes, n_potential_facilities, n_brd_players, max_iterations, n_simulations, seed):

        self.n_nodes = n_nodes
        self.n_potential_facilities = n_potential_facilities
        self.n_brd_players = n_brd_players
        self.max_iterations = max_iterations
        self.seed = seed
        self.main_rng = np.random.default_rng(seed=self.seed)

        self.setup_simulation()


    def setup_simulation(self):

        """
        Initializes the whole simulation environment
        """

        # Generate the FLG environment
        self.FLG_env = FLG_environment(self.n_nodes, self.n_potential_facilities, seed=self.seed)
        assert all(isinstance(node, int) for node in self.FLG_env.graph.nodes()) # Check that nodes were correctly generated (Just in case)

        # Calculate all distances between nodes using Dijkstra's algorithm for computational efficiency
        self.distances = Tools().calculate_distance_matrix(self.FLG_env.graph)

        # Setup the BRD players
        self.BRD_setup = BRD(self.n_brd_players, self.distances, self.FLG_env, seed=self.seed)


    def run_FLG_BRD_simulation(self):

        """
        Handle the simulation process

        Returns:
            iterations (int): Shows how many iterations the simulation took
            potential_function_development (list): How the potential function changes for each iteration  
            players_development_over_time (list): Players' facility assignments for each iteration
        """

        # Best Response Dynamics process
        players_find_best_response = [True] * self.n_brd_players

        # Variables for simulation study
        iterations = 0
        potential_function_development = [] # Track how the potential function changes over time        
        players_development_over_time = [] # Track players' assignments over time
        while any(players_find_best_response) and iterations < self.max_iterations:

            # Actual process
            player_in_turn = self.main_rng.choice(tuple(range(self.n_brd_players))) # Randomly select a player to find their best response
            updated = self.BRD_setup.find_best_response(player_in_turn)
            if updated:
                players_find_best_response = [True] * self.n_brd_players  # Force recheck all players
            else:
                players_find_best_response[player_in_turn] = False

            # Simulation development study
            iterations += 1
            potential_function_current_value = self.BRD_setup.calculate_potential_function()
            potential_function_development.append(potential_function_current_value)

            snapshot = {pid: copy.deepcopy(data) for pid, data in self.BRD_setup.players.items()}
            players_development_over_time.append(snapshot)

        # When the while loop ends it means that all player were not capable of finding a best response so the Nash Equilibrium is reached

        return iterations, potential_function_development, players_development_over_time

    
    def run_simulations(self, n_simulations):

        """
        Handle multiple simulations
        """
        
        # Variables for simulation study
        avg_iterations = 0
        potential_function_developments_per_iteration = []
        players_developments_per_iteration = []

        for i in range(n_simulations):

            print(f"Running simulation {i+1}/{n_simulations}...")
            iterations, potential_function_development, players_development_over_time = self.run_FLG_BRD_simulation()

            avg_iterations += iterations
            potential_function_developments_per_iteration.append(potential_function_development)
            players_developments_per_iteration.append(players_development_over_time)

        avg_iterations /= n_simulations

        return avg_iterations, potential_function_developments_per_iteration, players_developments_per_iteration
    

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
            

    def show_multiple_simulations_results(self, avg_iterations, potential_function_developments_per_iteration, players_development_per_iteration):

        # Show the results of the simulation
        print(f"The simulations took {avg_iterations} iterations on average to be completed")

        print(f"The average final potential function value was: {stats.mean([pf[-1] for pf in potential_function_developments_per_iteration])}")


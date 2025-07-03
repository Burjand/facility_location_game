import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.Simulation import Simulation
import tools.general_tools as general_tool

if __name__ == "__main__":

    CONFIGURATION = general_tool.extract_json_data("config.json5")

    # CONFIGURATION
    capacitated_facilities = CONFIGURATION['capacitated_facilities'] # (bool) True if you want capacitated facilities

    # HYPERPARAMETERS
    # Basics
    n_nodes = CONFIGURATION['n_nodes']    # Number of nodes in the graph
    n_potential_facilities = CONFIGURATION['n_potential_facilities'] # Number of potential facilities
    n_brd_players = CONFIGURATION['n_brd_players'] # Number of players in the BRD process
    max_iterations = CONFIGURATION['max_iterations'] # Max number of iterations before stopping an episode
    seed = CONFIGURATION['seed']
    n_simulations = CONFIGURATION['n_simulations'] # Number of simulations to run
    convergence_threshold = CONFIGURATION['convergence_threshold'] # Threshold used to determine convergence of the potential function (Not used in this version of the code)
    demand_distribution = tuple(CONFIGURATION['demand_distribution']) # The distribution of the graph's demand (node weights)
    cost_distribution = tuple(CONFIGURATION['weight_distribution']) # The distribution of the graph's costs (edge weights)

    # SIMULATION
    # Setup simulation
    simulation = Simulation(n_nodes, n_potential_facilities, n_brd_players, max_iterations, seed, demand_distribution, cost_distribution)
    
    # Run simulations
    if n_simulations == 1:
        iterations, potential_function_development, players_development_over_time = simulation.run_FLG_BRD_simulation()
        simulation.show_simulation_results(iterations, potential_function_development, players_development_over_time, True)

    else:

        assert (isinstance(n_simulations, int) and n_simulations > 1)
        avg_iterations, potential_function_developments_per_iteration, players_development_per_iteration = simulation.run_simulations(n_simulations)
        simulation.show_multiple_simulations_results(avg_iterations, potential_function_developments_per_iteration, players_development_per_iteration)
        





    


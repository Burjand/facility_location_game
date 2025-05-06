from Simulation import Simulation

if __name__ == "__main__":

    # HYPERPARAMETERS
    n_nodes = 100    # Number of nodes in the graph
    n_potential_facilities = 80 # Number of potential facilities
    n_brd_players = 10 # Number of players in the BRD process
    max_iterations = 1000 # Max number of iterations before stopping an episode
    #convergence_threshold = 1e-5 # Threshold used to determine convergence of the potential function (Not used in this version of the code)
    seed = 66
    n_simulations = 10 # Number of simulations to run

    # SIMULATION
    # Setup simulation
    simulation = Simulation(n_nodes, n_potential_facilities, n_brd_players, max_iterations, n_simulations, seed)
    # Run simulations
    if n_simulations == 1:
        iterations, potential_function_development, players_development_over_time = simulation.run_FLG_BRD_simulation()
        simulation.show_simulation_results(iterations, potential_function_development, players_development_over_time, True)

    else:

        assert (isinstance(n_simulations, int) and n_simulations > 1)
        avg_iterations, potential_function_developments_per_iteration, players_development_per_iteration = simulation.run_simulations(n_simulations)
        simulation.show_multiple_simulation_results(avg_iterations, potential_function_developments_per_iteration, players_development_per_iteration)
        





    


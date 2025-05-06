import numpy as np
import matplotlib.pyplot as plt
import copy

from Facility_Location_Game import FLG_environment
from Tools import Tools
from Best_Response_Dynamics import BRD

if __name__ == "__main__":

    # Hyperparameters
    n_nodes = 100    # Number of nodes in the graph
    n_potential_facilities = 80 # Number of potential facilities
    n_brd_players = 10 # Number of players in the BRD process
    max_iterations = 1000
    convergence_threshold = 1e-5
    seed = 66
    main_rng = np.random.default_rng(seed=seed)

    # Generate the FLG environment
    FLG_env = FLG_environment(n_nodes, n_potential_facilities, seed=seed)
    assert all(isinstance(node, int) for node in FLG_env.graph.nodes())

    # Calculate all distances between nodes using Dijkstra's algorithm for computational efficiency
    distances = Tools().calculate_distance_matrix(FLG_env.graph)

    # Setup the BRD players
    BRD_setup = BRD(n_brd_players, distances, FLG_env, seed=seed)

    # Best Response Dynamics process
    players_find_best_response = [True] * n_brd_players

    iteration = 0
    potential_function_development = [] # Track how the potential function changes over time        
    player_assignments_over_time = [] # Track players' assignments over time
    while any(players_find_best_response) and iteration < max_iterations:       

        # Actual process
        turn_of_player = main_rng.choice(tuple(range(n_brd_players))) # Randomly select a player to find their best response
        updated = BRD_setup.find_best_response(turn_of_player)
        if updated:
            players_find_best_response = [True] * n_brd_players  # Force recheck all players
        else:
            players_find_best_response[turn_of_player] = False

        # Simulation development study
        iteration += 1
        potential_function_current_value = BRD_setup.calculate_potential_function()
        potential_function_development.append(potential_function_current_value)
        print(potential_function_current_value)

        snapshot = {pid: copy.deepcopy(data) for pid, data in BRD_setup.players.items()}
        player_assignments_over_time.append(snapshot)

    # When the while loop ends it means that all player were not capable of finding a best response so the Nash Equilibrium is reached
    print(f"Nash Equilibrium found at iteration {iteration}!!!!!!")
    print("Final players' positions:")
    for player_id, player_data in BRD_setup.players.items():
        print(f"Player {player_id}: Facility Position: {player_data['facility_position']}, Utility: {player_data['Utility']}")
    print("Final Potential Function value:")
    print(BRD_setup.calculate_potential_function())


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
    player_facility_positions = {pid: [] for pid in range(n_brd_players)}
    player_utilities = {pid: [] for pid in range(n_brd_players)}

    for snapshot in player_assignments_over_time:
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



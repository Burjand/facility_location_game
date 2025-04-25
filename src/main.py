import numpy as np
import matplotlib.pyplot as plt


from Facility_Location_Game import FLG_environment
from Tools import Tools
from Best_Response_Dynamics import BRD

if __name__ == "__main__":
    # Hyperparameters
    n_nodes = 10
    n_potential_facilities = 10
    n_brd_players = 3

    # Generate the FLG environment
    FLG_env_gen = FLG_environment(n_nodes, n_potential_facilities)
    flg_env = FLG_env_gen.FLG_env

    # Calculate all distances between nodes using Dijkstra's algorithm for computational efficiency
    distances = Tools().calculate_distance_matrix(flg_env.graph)

    # Setup the BRD players
    BRD_setup = BRD(n_brd_players, distances, flg_env)

    # Best Response Dynamics process
    players_find_best_response = [True] * n_brd_players

    iteration = 0
    potential_function_development = []
    player_assignments_over_time = []
    while any(players_find_best_response):        

        # Actual rocess
        turn_of_player = np.random.choice(tuple(range(n_brd_players)))
        players_find_best_response[turn_of_player] = BRD_setup.find_best_response(turn_of_player)

        # Simulation development study
        iteration += 1
        potential_function_current_value = BRD_setup.calculate_potential_function()
        potential_function_development.append(potential_function_current_value)
        print(potential_function_current_value)

        snapshot = {pid: data for pid, data in BRD_setup.players.items()}
        player_assignments_over_time.append(snapshot)
        

    # When the while loop ends it means that all player were not capable of finding a best response so the Nash Equilibrium is reached
    print("Nash Equilibrium found!!!!!!")
    print("Final players' positions:")
    for player_id, player_data in BRD_setup.players.items():
        print(f"Player {player_id}: Facility Position: {player_data['facility_position']}, Utility: {player_data['Utility']}")
    print("Final Potential Function value:")
    print(BRD_setup.calculate_potential_function())


    # Plotting simulation development
    # Plot development of the potential function over time
    plt.figure(figsize=(10, 5))
    plt.plot(potential_function_development, marker='o')
    plt.title("Potential Function Over Time")
    plt.xlabel("Iteration")
    plt.ylabel("Potential Function Value")
    plt.grid(True)
    plt.show()

    player_facility_positions = {pid: [] for pid in range(n_brd_players)}
    player_utilities = {pid: [] for pid in range(n_brd_players)}

    for snapshot in player_assignments_over_time:
        for pid, data in snapshot.items():
            player_facility_positions[pid].append(data['facility_position'])
            player_utilities[pid].append(data['Utility'])

    # Plot facility assignments over time
    plt.figure(figsize=(10, 4))
    for pid, positions in player_facility_positions.items():
        plt.plot(positions, label=f'Player {pid}', marker='o')
    plt.title("Facility Positions Over Time")
    plt.xlabel("Iteration")
    plt.ylabel("Facility ID")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot utility over time
    plt.figure(figsize=(10, 4))
    for pid, utils in player_utilities.items():
        plt.plot(utils, label=f'Player {pid}', marker='x')
    plt.title("Utility Over Time")
    plt.xlabel("Iteration")
    plt.ylabel("Utility")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()



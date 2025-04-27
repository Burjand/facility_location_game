import numpy as np

class BRD():

    def __init__(self, n_players, distances, FLG_env, seed=42):

        self.n_players = n_players
        self.distances = distances
        self.nodes_demand = FLG_env.node_demand
        self.potential_facilities = FLG_env.potential_facilities_mask
        self.seed = seed
        self.rng = np.random.default_rng(seed=self.seed)

        self.check_players_amount()
        self.players = self.create_players()

    
    def check_players_amount(self):

        if self.n_players > sum(self.potential_facilities):
            raise ValueError("More players than available facilities.")


    def create_players(self):

        print("Nodes demands: " + str(self.nodes_demand))
        
        # Create a dictionary of options where is possible to put a facility, the value is initialized to 0 to indicate that in that potential facility there is no player assigned
        # and the key is the index of the potential facility
        self.facility_options = {
            i: 0 for i, is_potential in enumerate(self.potential_facilities) 
            if is_potential == 1
        }

        # Create players and assign them to random facilities
        players = {}
        for i in range(self.n_players):
            selected_random_facility = self.rng.choice(tuple(k for k, v in self.facility_options.items() if v == 0))            
            players[i] = {'facility_position': selected_random_facility, 'Utility': None}
            self.facility_options[selected_random_facility] = 1  # Mark the facility as occupied by a player

        # Update the utilities of all players
        for player_id, player in players.items():
            taken_facilities = [facility for facility, taken in self.facility_options.items() if taken == 1]
            player['Utility'] = self.calculate_facility_utility(player['facility_position'], taken_facilities)

        print("Players created with their initial positions and utilities:" + str(players)) 

        return players


    def find_best_response(self, player_id):
        current_facility = self.players[player_id]['facility_position']
        best_option = current_facility
        best_utility = self.players[player_id]['Utility']

        # Temporarily free the current facility
        self.facility_options[current_facility] = 0

        # Evaluate all possible options (including staying at current)
        for option in self.facility_options:
            if self.facility_options[option] == 1:
                continue  # Skip facilities occupied by others

            # Compute utility if player moves to `option`
            taken_facilities = [
                f for f, taken in self.facility_options.items() 
                if taken == 1 or f == option  # Include the new facility
            ]
            utility = self.calculate_facility_utility(option, taken_facilities)

            if utility > best_utility:
                best_utility = utility
                best_option = option

        # Restore the current facility’s state
        self.facility_options[current_facility] = 1

        # Update if a better option was found
        if best_option != current_facility:
            self.facility_options[current_facility] = 0
            self.facility_options[best_option] = 1
            self.players[player_id]['facility_position'] = best_option
            self.players[player_id]['Utility'] = best_utility
            return True
        return False


    def calculate_facility_utility(self, target_facility, taken_facilities):

        # Utilities reward both demand capture and cost minimization
        nearest_nodes = self.calculate_nearest_nodes(taken_facilities)
        captured_clients = nearest_nodes.get(target_facility, [])
        
        # Calculate the total demand of captured clients (including the facility's own node)
        sum_demands = sum(self.nodes_demand[c] for c in captured_clients)
        
        # Calculate the total cost (demand * distance) for all captured clients
        sum_costs = sum(self.nodes_demand[c] * self.distances[c][target_facility] for c in captured_clients)
        
        # Utility is the total demand minus total cost
        utility = sum_demands - sum_costs
        
        return utility


    def calculate_nearest_nodes(self, taken_facilities):
        # Calculate the nearest nodes to all facilities already taken

        # Create a dictionary where the keys are the taken facilities and the values will hold the nearest nodes to each facility
        facilities_nearest_nodes = {facility: [] for facility in taken_facilities}

        for node in self.distances:

            if node in taken_facilities:
                facilities_nearest_nodes[node].append(node)
                continue

            node_distances = self.distances[node] # Access to the disrances of the analyzed node to all other nodes

            min_distance = min(node_distances[facility] for facility in taken_facilities) # Calculate the minimum distance from the analyzed node to all taken facilities

            closest_facilities = [
                facility for facility in taken_facilities if node_distances[facility] == min_distance # Select all nodes that are at the minimum distance from the analyzed node
            ]
            
            # Apply tie-breaking rule (random assignment)            
            chosen_facility = self.rng.choice(closest_facilities) if len(closest_facilities) > 1 else closest_facilities[0]
            
            facilities_nearest_nodes[chosen_facility].append(node)

        return facilities_nearest_nodes


    def calculate_potential_function(self):

        taken_facilities = [facility for facility, taken in self.facility_options.items() if taken == 1]
        facilities_nearest_nodes = self.calculate_nearest_nodes(taken_facilities)

        system_wide_efficiency = 0

        for node in self.nodes_demand.keys():
            nearest_facility = next((k for k, v in facilities_nearest_nodes.items() if node in v), None)
            system_wide_efficiency += self.nodes_demand[node] * self.distances[node][nearest_facility]

        return system_wide_efficiency







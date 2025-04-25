import numpy as np

class BRD():

    def __init__(self, n_players, distances, flg_env, seed=42):

        self.n_players = n_players
        self.distances = distances
        self.nodes_demand = flg_env.node_demand
        self.potential_facilities = flg_env.potential_facilities_mask
        self.seed = seed

        self.players = self.create_players()


    def create_players(self):
        
        # Create a dictionary of options where is possible to put a facility, the value is initialized to 0 to indicate that in that potential facility there is no player assigned
        # and the key is the index of the potential facility
        self.facility_options = {}
        for i in range(len(self.potential_facilities)):
            if self.potential_facilities[i] == 1:
                self.facility_options[i] = 0

        # Create players and assign them to random facilities
        players = {}
        for i in range(self.n_players):
            selected_random_facility = np.random.choice(tuple(k for k, v in self.facility_options.items() if v == 0))            
            players[i] = {'facility_position': selected_random_facility, 'Utility': None}
            self.facility_options[selected_random_facility] = 1  # Mark the facility as occupied by a player

        # Update the utilities of all players
        for player_id, player in players.items():
            taken_facilities = [facility for facility, taken in self.facility_options.items() if taken == 1 and facility != player['facility_position']]
            player['Utility'] = self.calculate_facility_utility(player['facility_position'], taken_facilities)

        return players


    def find_best_response(self, player):

        new_facility_options = [facility for facility,taken in self.facility_options.items() if taken == 0 or facility == self.players[player]['facility_position']]
        new_utility = self.players[player]['Utility']
        best_option = self.players[player]['facility_position']

        for option in new_facility_options:
            taken_facilities = [facility for facility, taken in self.facility_options.items() if taken == 1 and facility != self.players[player]['facility_position']]
            temp_utility = self.calculate_facility_utility(option, taken_facilities)

            if temp_utility > new_utility:
                new_utility = temp_utility
                best_option = option

        if best_option != self.players[player]['facility_position']:
            # Update the facility options
            self.facility_options[self.players[player]['facility_position']] = 0
            self.facility_options[best_option] = 1  # Mark the new facility as occupied by the player
            self.players[player]['facility_position'] = best_option # Update the player's facility position
            self.players[player]['Utility'] = new_utility # Update the player's utility
            return True

        else:

            # No change in facility position, return False
            return False


    def calculate_facility_utility(self, target_facility, taken_facilities):
        # Calculate the utility of a facility given the facilities already taken
        facilities_nearest_nodes = self.calculate_nearest_nodes(taken_facilities + [target_facility])
        
        utility = 0
        for node in facilities_nearest_nodes[target_facility]:
            utility -= self.nodes_demand[node] * self.distances[node][target_facility]

        return utility


    def calculate_nearest_nodes(self, taken_facilities):
        # Calculate the nearest nodes to all facilities already taken

        # Create a dictionary where the keys are the taken facilities and the values will hold the nearest nodes to each facility
        facilities_nearest_nodes = {facility: [] for facility in taken_facilities}

        for node in self.distances.keys():

            node_distances = self.distances[node]

            min_distance = min(node_distances[facility] for facility in taken_facilities)

            closest_facilities = [
                facility for facility in taken_facilities 
                if node_distances[facility] == min_distance
            ]
            
            # Apply tie-breaking rule (random assignment)
            np.random.seed(self.seed)
            chosen_facility = np.random.choice(closest_facilities) if len(closest_facilities) > 1 else closest_facilities[0]
            
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







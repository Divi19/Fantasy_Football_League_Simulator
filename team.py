from __future__ import annotations
from data_structures.referential_array import ArrayR
from constants import GameResult, PlayerPosition, PlayerStats, TeamStats
from player import Player
from typing import Collection, Union, TypeVar
from data_structures.hash_table_separate_chaining import HashTableSeparateChaining
from data_structures.linked_queue import LinkedQueue
from data_structures.linked_list import LinkedList
from constants import Constants

T = TypeVar("T")


class Team:
    unique_number = 1
    def __init__(self, team_name: str, players: ArrayR[Player]) -> None:
        """
        Constructor for the Team class

        Args:
            team_name (str): The name of the team
            players (ArrayR[Player]): The players of the team

        Returns:
            None

        Complexity:
        In the best-case complexity, it occurs when the for loop, that loops through the TeamStats statitics, calls the insert() method of the
        hash table with seperate chaining. The insert() method then calls the _setitem_() method which calls the hash() method with complexity
        of O(K) where K is the size of the key. The for loop in the _setitem_() method only goes through once in which a position is found on the
        first loop meaning that there is no collisions, so, the complexity of the loop is O(1) and the append() method also has a complexity of O(1),
        hence, the best case complexity for _setitem_() is O(K). Therefore, the best case complexity of the insert() method is also O(K), so the for
        loop that goes through the TeamStats statitics has a complexity of O(N) where N is the number of statistics in the TeamStats enum, and it calls
        the insert() method. As a result, we have a complexity of O(K * N).

        In the worst-case complexity, it occurs when the for loop, that loops through the TeamStats statitics, calls the insert() method of the
        hash table with seperate chaining. The insert() method then calls the _setitem_() method which calls the hash() method with complexity
        of O(K) where K is the size of the key. The for loop in the _setitem_() method goes through almost all the elements in the linked list
        meaning it goes through L number of elements due to many conflicts, so, the complexity of the loop is O(L) and the append() method also has a 
        complexity of O(1), hence, the worst case complexity for _setitem_() is O(K + L). Therefore, the worst case complexity of the insert() method is also 
        O(K + L), so the for loop that goes through the TeamStats statitics has a complexity of O(N) where N is the number of statistics in the TeamStats enum, 
        and it calls the insert() method. As a result, we have a complexity of O(N * (K + L)).

            Best Case Complexity: O(K * N) where K is the size of the key and N is the number of statistics in the TeamStats enum
            Worst Case Complexity: O(N * (K + L)) where K is the size of the key, N is the number of statistics in the TeamStats enum
            and L is the number of elements in the linked list at a specific hash table position
        """
        self.number = Team.unique_number
        self.name = team_name
        self.statistics = HashTableSeparateChaining()

        for statistic in TeamStats:
            self.statistics.insert(statistic.value, 0)

        self.statistics[TeamStats.LAST_FIVE_RESULTS.value] = LinkedQueue()

        self.players = HashTableSeparateChaining()

        for player in players:
            self.add_player(player)

        Team.unique_number += 1

    def reset_stats(self) -> None:
        """
        Resets all the statistics of the team to the values they were during init.

        Complexity: See init.
            Best Case Complexity: O(K * N) where K is the size of the key and N is the number of statistics in the TeamStats enum
            Worst Case Complexity: O(N * (K + L)) where K is the size of the key, N is the number of statistics in the TeamStats enum
            and L is the number of elements in the linked list at a specific hash table position
        """
        for statistic in TeamStats:
            self.statistics.insert(statistic.value, 0)
        self.statistics[TeamStats.LAST_FIVE_RESULTS.value] = LinkedQueue()


    def add_player(self, player: Player) -> None:
        """
        Adds a player to the team.

        Args:
            player (Player): The player to add

        Returns:
            None

        Complexity:
        In the best-case complexity, it occurs when the the insert() method calls the _setitem_() method which calls the hash() method with complexity
        of O(K) where K is the size of the key. The for loop in the _setitem_() method only goes through once in which a position is found on the
        first loop meaning that there is no collisions, so, the complexity of the loop is O(1) and the append() method also has a complexity of O(1),
        hence, the best case complexity for _setitem_() is O(K). Therefore, the best case complexity of the insert() method is also O(K), hence the best case
        complexity for add_player() method is O(K)

        In the worst-case complexity, it occurs when the insert() method calls the _setitem_() method which calls the hash() method with complexity
        of O(K) where K is the size of the key. The for loop in the _setitem_() method goes through almost all the elements in the linked list
        meaning it goes through L number of elements due to many conflicts, so, the complexity of the loop is O(L) and the append() method also has a 
        complexity of O(1), hence, the worst case complexity for _setitem_() is O(K + L). Therefore, the worst case complexity of the insert() method is also 
        O(K + L), hence the worst case complexity for add_player() is O(K + L)

            Best Case Complexity: O(K) where K is the size of the key
            Worst Case Complexity: O(K + L) where K is the size of the key and L is the number of elements in the linked list at a specific hash table position
        """
        if player.get_position().value not in self.players:
            linked_list = LinkedList()
            linked_list.insert(0, player)
            self.players.insert(player.get_position().value, linked_list)
        else:
            access_key = self.players[player.get_position().value]
            access_key.insert(len(access_key), player)

    def remove_player(self, player: Player) -> None:
        """
        Removes a player from the team.

        Args:
            player (Player): The player to remove

        Returns:
            None

        Complexity:
        In the best-case complexity, it occurs when the _getitem_() method of the hash table with seperate chaining is called, which in the best case calls 
        the hash() method which has a complexity of O(K) where K is the size of the key and in this case the for loop for getting the key only runs one iteration
        in which it finds the key after the first loop and there are no collisions, so, the complexity of the loop is O(1), hence, the best case complexity for _getitem_()
        is O(K). The other method used is index() for the linked list and in the best case the item index is found immediately and the start of the linked list, so, it is O(1) 
        and the other method used is delete_at_index() and if the item is again in the first position, it is O(1), therefore, the best case complexity of this method is O(K).

        In the worst-case complexity, it occurs when the _getitem_() method of the hash table with seperate chaining is called, which in the worst case calls the hash() method 
        which has a complexity of O(K) where K is the size of the key and in this case the for loop for getting the key goes through almost all the elements in the linked list 
        meaning it goes through L number of elements due to many conflicts, so, the complexity of the loop is O(K + L), hence, the worst case complexity for _getitem_() is O(K + L).
        For the other methods, both index() and delete_at_index() have a worst case of O(L) where L is the number of elements inside the linked list, and it occurs when the item to find
        is at nearly the end of the linked list, so, L items needs to be traversed through, therefore, the final worst case complexity is O(K + L).

            Best Case Complexity: O(K) where K is the size of the key
            Worst Case Complexity: O(K + L) where K is the size of the key and L is the number of elements inside the linked list
        """
        if player.get_position().value in self.players:
            linked_list_access = self.players[player.get_position().value]
            index_of_player = linked_list_access.index(player)
            linked_list_access.delete_at_index(index_of_player)

    def get_number(self) -> int:
        """
        Returns the number of the team.

        Complexity:
            Analysis not required.
        """
        return self.number

    def get_name(self) -> str:
        """
        Returns the name of the team.

        Complexity:
            Analysis not required.
        """
        return self.name

    def get_players(self, position: Union[PlayerPosition, None] = None) -> Union[Collection[Player], None]:
        """
        Returns the players of the team that play in the specified position.
        If position is None, it should return ALL players in the team.
        You may assume the position will always be valid.
        Args:
            position (Union[PlayerPosition, None]): The position of the players to return

        Returns:
            Collection[Player]: The players that play in the specified position
            held in a valid data structure provided to you within
            the data_structures folder this includes the ArrayR
            which was previously prohibited.

            None: When no players match the criteria / team has no players

        Complexity:
        In the best-case complexity, it occurs when the values() method of the hash table with seperate chaining is called which has
        a complexity of O(N) where N is the number of items currently being stored in the hash table and the for loop only runs one time
        because the first linked list provided by the values() method is not empty/its length is not equal to zero, hence the complexity
        of the for loop takes only the complexity of the values() method which is O(N). The position is not equal to None, so, the nested for loops
        do not run, and the conditional that returns a None type is fulfiled which occurs when the length of the particular linked list for the position
        is equal to zero, indicating then there are no elements inside the linked list and the complexity of this _len_() is O(1). Therefore, the final
        best case complexity if O(N).

        In the worst-case complexity, it occurs when the position is None which cause a nested loop to run in which all the statistics of PlayerPosition
        enum is gone through and each linked list value from each enum key is iterated through, hence we have a complexity of O(M) for the outer loop and 
        O(L) for the inner loop which combines to form a final worst case complexity of O(M * L) where M is the number of statistics in the PlayerPostion 
        enum and L is number of items inside the linked list.

            Best Case Complexity: O(N) where N is the number of items currently being stored in the hash table
            Worst Case Complexity: O(M * L) where M is the number of statistics in the PlayerPostion enum and L is number of items inside the linked list
        """
        all_empty = all(len(lst) == 0 for lst in self.players.values())

        if all_empty:
            return None
        
        if position is None:
            linked_list = LinkedList()
            for lists in PlayerPosition:
                if lists.value in self.players and self.players[lists.value]:
                    for player in self.players[lists.value]:
                        linked_list.append(player)
            return linked_list

        if len(self.players[position.value]) == 0:
            return None

        return self.players[position.value]

    def get_statistics(self):
        """
        Get the statistics of the team

        Returns:
            statistics: The teams' statistics

        Complexity:
        Both the best and worst case complexity is O(1) since we are only using a simple return statament

            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return self.statistics

    def get_last_five_results(self) -> Union[Collection[GameResult], None]:
        """
        Returns the last five results of the team.
        If the team has played less than five games,
        return all the result of all the games played so far.

        For example:
        If a team has only played 4 games and they have:
        Won the first, lost the second and third, and drawn the last,
        the array should be an array of size 4
        [GameResult.WIN, GameResult.LOSS, GameResult.LOSS, GameResult.DRAW]

        **Important Note:**
        If this method is called before the team has played any games,
        return None the reason for this is explained in the specefication.

        Returns:
            Collection[GameResult]: The last five results of the team
            or
            None if the team has not played any games.

        Complexity:
        In the best-case complexity, it occurs when the _getitem_() method of the hash table with seperate chaining is called, which in the best case calls 
        the hash() method which has a complexity of O(K) where K is the size of the key and in this case the for loop for getting the key only runs one iteration
        in which it finds the key after the first loop and there are no collisions, so, the complexity of the loop is O(1), hence, the best case complexity for _getitem_()
        is O(K).

        In the worst-case complexity, it occurs when the _getitem_() method of the hash table with seperate chaining is called, which in the worst case calls the hash() method 
        which has a complexity of O(K) where K is the size of the key and in this case the for loop for getting the key goes through almost all the elements in the hash table 
        meaning it goes through N number of elements due to many conflicts, so, the complexity of the loop is O(K + N), hence, the worst case complexity for _getitem_() is O(K + N).

            Best Case Complexity: O(K) where K is the size of the key
            Worst Case Complexity: O(K + N) where K is the size of the key and N is the number of keys currently being stored in the hash table
        """
        if self.statistics[TeamStats.GAMES_PLAYED.value] == 0:
            return None
        return self.statistics[TeamStats.LAST_FIVE_RESULTS.value]

    def get_top_x_players(self, player_stat: PlayerStats, num_players: int) -> list[tuple[int, str, Player]]:
        """
        Note: This method is only required for FIT1054 students only!

        Args:
            player_stat (PlayerStats): The player statistic to use to order the top players
            num_players (int): The number of players to return from this team

        Return:
            list[tuple[int, str, Player]]: The top x players from this team
        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        raise NotImplementedError

    def __setitem__(self, statistic: TeamStats, value: int) -> None:
        """
        Updates the team's statistics.

        Args:
            statistic (TeamStats): The statistic to update
            value (int): The new value of the statistic

        Complexity: See game_outcomes
            Best Case Complexity: O(K) where K is the size of the key
            Worst Case Complexity: O(K + L) where K is the size of the key and L is the number of elements in the linked list at a specific hash table position
        """
        original_value = self.statistics[statistic.value]
        self.statistics[statistic.value] = value
        new_value = self.statistics[statistic.value]
        difference = new_value - original_value
        last_five_results = self.get_last_five_results()

        if last_five_results is None:
            last_five_results = LinkedQueue()

        self.game_outcomes(statistic, last_five_results, difference)

        if statistic.value == "Goals For" or statistic.value == "Goals Against":
            self.statistics[TeamStats.GOALS_DIFFERENCE.value] = int(self.statistics[TeamStats.GOALS_FOR.value]) - int(self.statistics[TeamStats.GOALS_AGAINST.value])
            
        for i in range(len(last_five_results)):
            if len(last_five_results) >= Constants.NUMBER_OF_RESULTS:
                last_five_results.serve()

        self.statistics[TeamStats.LAST_FIVE_RESULTS.value] = last_five_results

    def game_outcomes(self, statistic, last_five_results, difference):
        """
        Checks on the outcomes of the games and changes the necessary other values.

        Args:
            statistic (TeamStats): The statistic to update
            last_five_results: The last five results of the team
            difference (int): The difference between the original value and the new value

        Complexity:
        In the best-case complexity, it occurs when the _setitem_() method is called for hash table with seperate chaining which calls the hash() method with complexity
        of O(K) where K is the size of the key. The for loop in the _setitem_() method only goes through once in which a position is found on the
        first loop meaning that there is no collisions, so, the complexity of the loop is O(1) hence, the best case complexity for _setitem_() is O(K). 

        In the worst-case complexity, it occurs when the _setitem_() method is called for hash table with seperate chaining which calls the hash() method with complexity
        of O(K) where K is the size of the key. The for loop in the _setitem_() method goes through almost all the elements in the linked list
        meaning it goes through L number of elements due to many conflicts, so, the complexity of the loop is O(L), hence, the worst case complexity for _setitem_() is O(K + L).

            Best Case Complexity: O(K) where K is the size of the key
            Worst Case Complexity: O(K + L) where K is the size of the key and L is the number of elements in the linked list at a specific hash table position
        """
        if statistic.value == "Wins" or statistic.value == "Draws" or statistic.value == "Losses":
            self.statistics[TeamStats.GAMES_PLAYED.value] = int(self.statistics[TeamStats.GAMES_PLAYED.value]) + difference
            if statistic.value == "Wins":
                self.statistics[TeamStats.POINTS.value] += (difference * GameResult.WIN.value)
                last_five_results.append(GameResult.WIN)
            if statistic.value == "Draws":
                self.statistics[TeamStats.POINTS.value] += (difference * GameResult.DRAW.value)
                last_five_results.append(GameResult.DRAW)
            if statistic.value == "Losses":
                self.statistics[TeamStats.POINTS.value] += (difference * GameResult.LOSS.value)
                last_five_results.append(GameResult.LOSS)


    def __getitem__(self, statistic: TeamStats) -> int:
        """
        Returns the value of the specified statistic.

        Args:
            statistic (TeamStats): The statistic to return

        Returns:
            int: The value of the specified statistic

        Raises:
            ValueError: If the statistic is invalid

        Complexity:
        In the best-case complexity, it occurs when the _getitem_() method of the hash table with seperate chaining is called, which in the best case calls 
        the hash() method which has a complexity of O(K) where K is the size of the key and in this case the for loop for getting the key only runs one iteration
        in which it finds the key after the first loop and there are no collisions, so, the complexity of the loop is O(1), hence, the best case complexity for _getitem_()
        is O(K).

        In the worst-case complexity, it occurs when the _getitem_() method of the hash table with seperate chaining is called, which in the worst case calls the hash() method 
        which has a complexity of O(K) where K is the size of the key and in this case the for loop for getting the key goes through almost all the elements in the hash table 
        meaning it goes through N number of elements due to many conflicts, so, the complexity of the loop is O(K + N), hence, the worst case complexity for _getitem_() is O(K + L).

            Best Case Complexity: O(K) where K is the size of the key
            Worst Case Complexity: O(K + N) where K is the size of the key and N is the number of keys currently being stored in the hash table
        """
        return self.statistics[statistic.value]

    def __len__(self) -> int:
        """
        Returns the number of players in the team.

        Complexity:
        Both the best and worst case complexity is O(N) where N is the number of keys currently being stored in the hash table because
        a for loop goes through N number of keys in the hash table and calls the _len_() method on the linked lists that are the values
        of the key and this has complexity of O(1), so, the final complexity is O(N).

            Best Case Complexity: O(N) where N is the number of keys currently being stored in the hash table
            Worst Case Complexity: O(N) where N is the number of keys currently being stored in the hash table
        """
        num_of_players = 0
        for key in self.players:
            linked_list = key
            num_of_players += len(linked_list)
        return num_of_players

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the team object.

        Complexity:
            Analysis not required.
        """
        return f"{self.get_name()} vs {self.get_statistics()}"

    def __repr__(self) -> str:
        """Returns a string representation of the Team object.
        Useful for debugging or when the Team is held in another data structure."""
        return str(self)

    def __lt__(self, other):
        if self.statistics[TeamStats.POINTS.value] != other.statistics[TeamStats.POINTS.value]:
            return self.statistics[TeamStats.POINTS.value] > other.statistics[TeamStats.POINTS.value]
        if self.statistics[TeamStats.GOALS_DIFFERENCE.value] != other.statistics[TeamStats.GOALS_DIFFERENCE.value]:
            return self.statistics[TeamStats.GOALS_DIFFERENCE.value] > other.statistics[TeamStats.GOALS_DIFFERENCE.value]
        if self.statistics[TeamStats.GOALS_FOR.value] != other.statistics[TeamStats.GOALS_FOR.value]:
            return self.statistics[TeamStats.GOALS_FOR.value] > other.statistics[TeamStats.GOALS_FOR.value]
        return self.name < other.name

    def __eq__(self, other):
        return (self.statistics[TeamStats.POINTS.value] == other.statistics[TeamStats.POINTS.value] and self.statistics[TeamStats.GOALS_DIFFERENCE.value] == other.statistics[TeamStats.GOALS_DIFFERENCE.value] and self.statistics[TeamStats.GOALS_FOR.value] == other.statistics[TeamStats.GOALS_FOR.value] and self.name == other.name)

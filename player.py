from __future__ import annotations
from constants import PlayerPosition, PlayerStats
from data_structures.hash_table_separate_chaining import HashTableSeparateChaining
from hashy_perfection_table import HashyPerfectionTable


class Player:

    def __init__(self, name: str, position: PlayerPosition, age: int) -> None:
        """
        Constructor for the Player class

        Args:
            value (str): The value of the player
            position (PlayerPosition): The position of the player
            age (int): The age of the player

        Returns:
            None

        Complexity:
        Both the best and worst-case complexity is O(1) since we are using our HashyPerfectionTable ADT which provides
        a perfect hash function, so, the hash() method in our perfect hash table which is used in the _setitem_() method,
        has a complexity of O(1), so, _setitem_ also has complexity of O(1). The number of PlayerStats in this perfect hash table
        is a constant value, hence the for loop iterates over a constant value and calls the _setitem_() method which is O(1), therefore,
        the final complexity for both best and worst case is O(1).

            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)

        """
        self.name = name
        self.position = position
        self.age = age
        self.statistics = HashyPerfectionTable()

        for statistic in PlayerStats:
            self.statistics[statistic.value] = 0

    def reset_stats(self) -> None:
        """
        Reset the stats of the player

        Returns:
            None

        Complexity:
        Both the best and worst-case complexity is O(1) since we are using our HashyPerfectionTable ADT which provides
        a perfect hash function, so, the hash() method in our perfect hash table which is used in the _setitem_() method,
        has a complexity of O(1), so, _setitem_ also has complexity of O(1). The number of PlayerStats in this perfect hash table
        is a constant value, hence the for loop iterates over a constant value and calls the _setitem_() method which is O(1), therefore,
        the final complexity for both best and worst case is O(1).

            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)

        """
        for statistic in PlayerStats:
            self.statistics[statistic.value] = 0

    def get_name(self) -> str:
        """
        Get the value of the player

        Returns:
            str: The value of the player

        Complexity:
        It uses a simple return statment, so, both best and worst case complexity is O(1).

            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return self.name

    def get_position(self) -> PlayerPosition:
        """
        Get the position of the player

        Returns:
            PlayerPosition: The position of the player

        Complexity:
        It uses a simple return statment, so, both best and worst case complexity is O(1).

            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return self.position

    def get_statistics(self):
        """
        Get the statistics of the player

        Returns:
            statistics: The players' statistics

        Complexity:
        It uses a simple return statment, so, both best and worst case complexity is O(1).

            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return self.statistics

    def __setitem__(self, statistic: PlayerStats, value: int) -> None:
        """
        Set the value of the player's stat based on the key that is passed.

        Args:
            statistic (PlayerStat): The key of the stat
            value (int): The value of the stat

        Returns:
            None

        Complexity:
        It uses a simple return statment and the _setitem_ method in the perfect hash table has a complexity of O(1), so, 
        both best and worst case complexity is O(1).

            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        self.statistics[statistic.value] = value

    def __getitem__(self, statistic: PlayerStats) -> int:
        """
        Get the value of the player's stat based on the key that is passed.

        Args:
            statistic (PlayerStat): The key of the stat

        Returns:
            int: The value of the stat

        Complexity:
        It uses a simple return statment and the _getitem_ method in the perfect hash table has a complexity of O(1), so,
        both best and worst case complexity is O(1).

            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return self.statistics[statistic.value]

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the player object.

        Complexity:
            Analysis not required.
        """
        return f"Player(value= {self.name}, stats= {self.statistics})"

    def __repr__(self) -> str:
        """Returns a string representation of the Player object.
        Useful for debugging or when the Player is held in another data structure."""
        return str(self)

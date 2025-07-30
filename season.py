from __future__ import annotations
from data_structures.bset import BSet
from data_structures.referential_array import ArrayR
from dataclasses import dataclass
from team import Team
from typing import Generator, Union
from data_structures.array_sorted_list import ArraySortedList
from constants import Constants
from data_structures.linked_queue import LinkedQueue
from data_structures.linked_list import LinkedList
from game_simulator import GameSimulator
from constants import PlayerStats, TeamStats


@dataclass
class Game:
    """
    Simple container for a game between two teams.
    Both teams must be team objects, there cannot be a game without two teams.

    Note: Python will automatically generate the init for you.
    Use Game(home_team: Team, away_team: Team) to use this class.
    See: https://docs.python.org/3/library/dataclasses.html
    """
    home_team: Team = None
    away_team: Team = None
    result = None

    def update_players(self, home_players, away_players, names, stat):
        """
        Updates the statistics of the players.

        Args:
            home_players: The players of the home team.
            away_players: The players of the away team.
            names: A list of names of the players to be updated.
            stat: The statistic to be updated.

        Complexity:
        In the best-case complexity, it occurs when there are no names in the names list or it is initialized to
        a None type in which case the whole if block is skipped and no loops are done, thus, it has a constant best case 
        time complexity of O(1).

        In the worst-case complexity, it occurs when there are names in the names variable and it is not a None type, and the player is in
        the away team. Therefore, it would have to go through the outer loop for N number of players in the list and both the inner loops for A number
        of home players and B number of away players, thus, leading to a complexity of O(A + B) for the inner loop. It goes through both inner loops since it still has
        to check the home players list to see if the player is inside there which it will not detect, so it goes through A number of players and hence, goes to the away player 
        loop which it will detect but it has to go through nearly all the B number of away players in the list to find the player to update. The final complexity combines both 
        the outer loop which gives the final worst case complexity as O(N * (A + B)).

            Best Case Complexity: O(1)
            Worst Case Complexity: O(N * (A + B)) where N is the number of players in the list in which we need to update the statitics on,
            A is the number of players in the home team and B is the number of players in the away team
        """
        if names is not None:
            for name in names:
                for player in home_players:
                    if name == player.get_name():
                        stats = player.get_statistics()
                        stats[stat] += 1
                        break
                for player in away_players:
                    if name == player.get_name():
                        stats = player.get_statistics()
                        stats[stat] += 1

    def update_game(self):
        """
        Updates the statistics of both the players and the team

        Args:
            None

        Complexity:
        In the best-case complexity, it occurs when the get_players() method is called and since the paramter is None, it causes a nested loop to run in which 
        all the statistics of PlayerPosition enum is gone through and each linked list value from each enum key is iterated through, hence we have a complexity 
        of O(M) for the outer loop and O(L) for the inner loop which combines to form a final best case complexity of O(M * L) where M is the number of statistics 
        in the PlayerPostion enum and L is number of items inside the linked list. The update_players() method has a best case of O(1) when there are no names in the 
        names list or it is initialized to a None type in which case the whole if block is skipped and no loops are done, thus, it has a constant best case 
        time complexity of O(1). Therefore the final best complexity only takes into account the get_players() method, so, it has a complexity of O(M * L).

        In the worst-case complexity, it occurs when the get_player() method is called and since the parameter is None, it causes a nested loop to run in which 
        all the statistics of PlayerPosition enum is gone through and each linked list value from each enum key is iterated through, hence we have a complexity 
        of O(M) for the outer loop and O(L) for the inner loop which combines to form a worst case complexity of O(M * L) where M is the number of statistics 
        in the PlayerPostion enum and L is number of items inside the linked list. Also, the update_players() method is called which has a worst case of O(N * (A + B))
        which occurs when there are names in the names variable and it is not a None type, and the player is in the away team. Therefore, the final worst case complexity
        combines both of these to form a complexity of O((M * L) + (N * (A + B))).
        

            Best Case complexity: O(M * L) where M is the number of statistics in the PlayerPostion enum and L is number of items inside the linked list
            Worst Case Complexity: O((M * L) + (N * (A + B))) where M is the number of statistics in the PlayerPostion enum, L is number of items inside the linked list,
            N is the number of players in the list in which we need to update the statitics on, A is the number of players in the home team and B is the number of players in 
            the away team
        """ 
        self.result = GameSimulator.simulate(self.home_team, self.away_team)
        home_players = self.home_team.get_players()
        away_players = self.away_team.get_players()
        update_scores = self.result['Goal Scorers']
        update_assists = self.result['Goal Assists']
        update_interceptions = self.result['Interceptions']
        update_tackles = self.result['Tackles']

        self.update_players(home_players, away_players, update_scores, PlayerStats.GOALS.value)
        self.update_players(home_players, away_players, update_assists, PlayerStats.ASSISTS.value)
        self.update_players(home_players, away_players, update_interceptions, PlayerStats.INTERCEPTIONS.value)
        self.update_players(home_players, away_players, update_tackles, PlayerStats.TACKLES.value)

        for player in home_players:
            stats = player.get_statistics()
            stats[PlayerStats.GAMES_PLAYED.value] += 1

        for player in away_players:
            stats = player.get_statistics()
            stats[PlayerStats.GAMES_PLAYED.value] += 1

        home_goals = self.result['Home Goals']
        away_goals = self.result['Away Goals']

        self.home_team[TeamStats.GOALS_FOR] += home_goals
        self.home_team[TeamStats.GOALS_AGAINST] += away_goals

        self.away_team[TeamStats.GOALS_FOR] += away_goals
        self.away_team[TeamStats.GOALS_AGAINST] += home_goals

        if home_goals > away_goals:
            self.home_team[TeamStats.WINS] += 1
            self.away_team[TeamStats.LOSSES] += 1
        elif home_goals < away_goals:
            self.away_team[TeamStats.WINS] += 1
            self.home_team[TeamStats.LOSSES] += 1
        else:
            self.home_team[TeamStats.DRAWS] += 1
            self.away_team[TeamStats.DRAWS] += 1

    def __str__(self) -> str:
        return f"{self.home_team.get_name()} vs {self.away_team.get_name()}"

class WeekOfGames:
    """
    Simple container for a week of games.

    A fixture must have at least one game.
    """

    def __init__(self, week: int, games: ArrayR[Game]) -> None:
        """
        Container for a week of games.

        Args:
            week (int): The week number.
            games (ArrayR[Game]): The games for this week.
        """
        self.games: ArrayR[Game] = games
        self.week: int = week

    def get_games(self) -> ArrayR:
        """
        Returns the games in a given week.

        Returns:
            ArrayR: The games in a given week.

        Complexity:
        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """
        return self.games

    def get_week(self) -> int:
        """
        Returns the week number.

        Returns:
            int: The week number.

        Complexity:
        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """
        return self.week

    def __iter__(self):
        """
        Complexity:
        Both the best and worst case complexity is O(1) since a simple return statement is used.

        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Complexity:
        Both the best and worst case complexity is O(1) since a simple return statement is used and the _setitem_() for referential
        array is O(1).

        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """
        games = self.games[self._index]
        self._index += 1
        return games
    
    def __str__(self) -> str:
        return f"Week {self.week}: " + ", ".join(str(game) for game in self.games)


class Season:

    def __init__(self, teams: ArrayR[Team]) -> None:
        """
        Initializes the season with a schedule.

        Args:
            teams (ArrayR[Team]): The teams played in this season.

        Complexity:
        In both the best and worst case, the complexity is O(N^2) since in both instances, the _generate_schedule() method is
        called which is O(N^2) in both cases. In the best case, the add method adds the teams at the end of the list meaning no
        shuffling needs to take place, hence it has O(1) complexity and combined with the for loop, it would have O(N) complexity
        where again N is the number teams in the season and the for loop that goes through the week of games has the append() method with
        complexity of O(1) and combined with the for loop, it has a complexity of O(M) where M is the number of weeks in a season. Therefore,
        our complexity is O((N^2) + N + M) which can just be simplified to O(N^2).

            Best Case Complexity: O(N^2) where N is the number of teams in the season.
            Worst Case Complexity: O(N^2) where N is the number of teams in the season.
        """
        self.teams = teams
        sorted_list = ArraySortedList(Constants.MAX_NUM_TEAMS)
        linked_list = LinkedList()
        for team in teams:
            sorted_list.add(team)

        schedules = self._generate_schedule()
        for schedule in schedules:
            linked_list.append(schedule)
        
        self.leaderboard = sorted_list
        self.schedule = linked_list

    def _generate_schedule(self) -> ArrayR[ArrayR[Game]]:
        """
        Generates a schedule by generating all possible games between the teams.

        Return:
            ArrayR[ArrayR[Game]]: The schedule of the season.
                The outer array is the weeks in the season.
                The inner array is the games for that given week.

        Complexity:
            Best Case Complexity: O(N^2) where N is the number of teams in the season.
            Worst Case Complexity: O(N^2) where N is the number of teams in the season.
        """
        num_teams: int = len(self.teams)
        weekly_games: list[ArrayR[Game]] = []
        flipped_weeks: list[ArrayR[Game]] = []
        games: list[Game] = []

        # Generate all possible matchups (team1 vs team2, team2 vs team1, etc.)
        for i in range(num_teams):
            for j in range(i + 1, num_teams):
                games.append(Game(self.teams[i], self.teams[j]))

        # Allocate games into each week ensuring no team plays more than once in a week
        week: int = 0
        while games:
            current_week: list[Game] = []
            flipped_week: list[Game] = []
            used_teams: BSet = BSet()

            week_game_no: int = 0
            for game in games[:]:  # Iterate over a copy of the list
                if game.home_team.get_number() not in used_teams and game.away_team.get_number() not in used_teams:
                    current_week.append(game)
                    used_teams.add(game.home_team.get_number())
                    used_teams.add(game.away_team.get_number())

                    flipped_week.append(Game(game.away_team, game.home_team))
                    games.remove(game)
                    week_game_no += 1

            weekly_games.append(ArrayR.from_list(current_week))
            flipped_weeks.append(ArrayR.from_list(flipped_week))
            week += 1

        return ArrayR.from_list(weekly_games + flipped_weeks)

    def simulate_season(self) -> None:
        """
        Simulates the season.

        Complexity:
        In the best-case complexity, there is two nested loops with complexity of O(W) and O(G) for the outer loop and inner loop respectively. Inside
        the inner loop, we call the update_players() method which has best case O(M * L) when the get_players() method is called and since the paramter is None, 
        it causes a nested loop to run in which all the statistics of PlayerPosition enum is gone through and each linked list value from each enum key is iterated through, 
        hence we have a complexity of O(M) for the outer loop and O(L) for the inner loop which combines to form a best case complexity of O(M * L) where M is the number 
        of statistics in the PlayerPostion enum and L is number of items inside the linked list. Therefore, combining them, we end up with a best case complexity
        of O(W * G * (M * L)).

        In the worst-case complexity, there is two nested loops with complexity of O(W) and O(G) for the outer loop and inner loop respectively. Inside
        the inner loop, we call the update_players() method which has worst case O((M * L) + (N * (A + B))) when the get_players() method is called and since the paramter is None, 
        it causes a nested loop to run in which all the statistics of PlayerPosition enum is gone through and each linked list value from each enum key is iterated through, 
        hence we have a complexity of O(M) for the outer loop and O(L) for the inner loop which combines to form a final best case complexity of O(M * L) where M is the number 
        of statistics in the PlayerPostion enum and L is number of items inside the linked list.Also, the update_players() method is called which has a worst case of O(N * (A + B))
        which occurs when there are names in the names variable and it is not a None type, and the player is in the away team. Therefore, the worst case complexity
        combines both of these to form a complexity of O((M * L) + (N * (A + B))). Therefore, combining them, we end up with a worst case complexity
        of O(W * G * ((M * L) + (N * (A + B)))

            Best Case Complexity: O(W * G * (M * L)) where W is the number of weeks of games, G is the number of games played in a given week,
            M is the number of statistics in the PlayerPostion enum and L is number of items inside the linked list.
            Worst Case Complexity: O(W * G * ((M * L) + (N * (A + B))) where W is the number of weeks of games, G is the number of games played in a given week,
            M is the number of statistics in the PlayerPostion enum, L is number of items inside the linked list, N is the number of players in the list in which we need 
            to update the statitics on, A is the number of players in the home team and B is the number of players in the away team.
        """
        for game_week in self.schedule:          
            for game in game_week:
                game.update_game()

    def delay_week_of_games(self, orig_week: int, new_week: Union[int, None] = None) -> None:
        """
        Delay a week of games from one week to another.

        Args:
            orig_week (int): The original week to move the games from.
            new_week (Union[int, None]): The new week to move the games to. If this is None, it moves the games to the end of the season.

        Complexity:
        In the best-case complexity, it occurs when the new_week parameter is set to None, so, it goes through the conditional where it calls the
        index() method for the linked list, and in the best case, the index is in the first position of the linked list, so, it is O(1). The delete_at_index()
        method is then called and since the item was found to be in the first position, it does not need to traverse through the other elements to delete the
        index, hence, it is O(1). Finally, the append() method for linked list is O(1) complexity and therefore, the final best case complexity is just O(1).

        In the worst-case complexity, it occurs when the new_week parameter is not set to None and has a value, so, the index() methods for both the original and
        the new week is called and in the worst case, both the elements are almost at the end of the linked list, so, the complexity for both the index() methods is O(N) 
        where N is the number of items in the linked list. The delete_at_index() methos also has to traverse nearly to the end of the list to delete the index, so, it is
        also O(N) and lastly, the insert method has to traverse to the end of the linked list to insert the element into the new position hence, it is also O(N). Therefore,
        the final worst case complexity is O(N).

            Best Case Complexity: O(1)
            Worst Case Complexity: O(N) where N is the number of items in the linked list
        """
        if new_week is None:
            first_week_index = self.schedule.index(self.schedule[orig_week - 1])
            week1 = self.schedule.delete_at_index(first_week_index)
            self.schedule.append(week1)            
            return None
        
        first_week_index = self.schedule.index(self.schedule[orig_week - 1])
        second_week_index = self.schedule.index(self.schedule[new_week - 1])

        week = self.schedule.delete_at_index(first_week_index)
        self.schedule.insert(second_week_index, week)
        
    def get_next_game(self) -> Union[Generator[Game], None]:
        """
        Gets the next game in the season.

        Returns:
            Game: The next game in the season.
            or None if there are no more games left.

        Complexity:
        Both the best and worst case complexity is O(1)  because the is_empty() method check is O(1) and the _getitem_() method for
        the linked list is O(1) since only the first element of the linked list is returned.

            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        if self.schedule.is_empty():
            return None
        current_game = self.schedule[0]
        return current_game

    def get_leaderboard(self) -> ArrayR[ArrayR[Union[int, str]]]:
        """
        Generates the final season leaderboard.

        Returns:
            ArrayR(ArrayR[ArrayR[Union[int, str]]]):
                Outer array represents each team in the leaderboard
                Inner array consists of 10 elements:
                    - Team name (str)
                    - Games Played (int)
                    - Points (int)
                    - Wins (int)
                    - Draws (int)
                    - Losses (int)
                    - Goals For (int)
                    - Goals Against (int)
                    - Goal Difference (int)
                    - Previous Five Results (ArrayR(str)) where result should be WIN LOSS OR DRAW

        Complexity:
        In the best-case complexity, it occurs when the for loop that adds the teams into self.leaderboard are all added at the ends of the list each time, so, no 
        shuffling of elements occur, so, only the _index_to_add() method causes its complexity to be O(logN) and when combined with the loop it has a complexity of
        O(NlogN). For the for loop that loops through the teams in self.leaderboard and adds it to the referential array, it has a complexity of O(N) where N inumber of 
        teams participating in the season and the creation of ArrayR has a complexity of O(M) where M is the number of statistics of the TeamStats enum, so, it combines
        to form a complexity of O(N * M). Therefore, the final best case complexity is O((N * M) + NlogN) which can be simplifed to just O(N * M).

        In the worst-case complexity, it occurs when the for loop that adds the teams into self.leaderboard are all added at the beginning of the list each time, so, there 
        shuffling of N elements occuring, so, it has a complexity of O(N) where N is the number of teams participating in the season. After combining with its for loop we have 
        a complexity of O(N^2). For the for loop that loops through the teams in self.leaderboard and adds it to the referential array, it has a complexity of O(N) where N inumber of 
        teams participating in the season and the creation of ArrayR has a complexity of O(M) where M is the number of statistics of the TeamStats enum, so, it combines
        to form a complexity of O(N * M). Therefore, the final best case complexity is O((N * M) + N^2) which can be simplifed to just O(N^2).

            Best Case Complexity: O(N * M) where N is the number of teams participating in the season and M is the number of statistics of the TeamStats enum
            Worst Case Complexity: O(N^2) where N is the number of teams participating in the season
        """
        ref_list = ArrayR(len(self.leaderboard))
        index_counter = 0
        self.leaderboard.reset()
        for team in self.teams:
            self.leaderboard.add(team)
        for teams in self.leaderboard:
            stat = teams.get_statistics()
            collection = ArrayR(len(TeamStats) + 1)
            collection[0] = teams.get_name()
            collection[1] = stat[TeamStats.GAMES_PLAYED.value]
            collection[2] = stat[TeamStats.POINTS.value]
            collection[3] = stat[TeamStats.WINS.value]
            collection[4] = stat[TeamStats.DRAWS.value]
            collection[5] = stat[TeamStats.LOSSES.value]
            collection[6] = stat[TeamStats.GOALS_FOR.value]
            collection[7] = stat[TeamStats.GOALS_AGAINST.value]
            collection[8] = stat[TeamStats.GOALS_DIFFERENCE.value]
            collection[9] = stat[TeamStats.LAST_FIVE_RESULTS.value]

            ref_list[index_counter] = collection
            index_counter += 1
        return ref_list

    def get_teams(self) -> ArrayR[Team]:
        """
        Returns:
            PlayerPosition (ArrayR(Team)): The teams participating in the season.

        Complexity:
        Both the best and worst case complexity is O(1) since we are just using a simple return statement.

            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return self.teams

    def __len__(self) -> int:
        """
        Returns the number of teams in the season.

        Complexity:
        Both the best and worst case complexity is O(1) since the len() method is O(1) and a simple return statement
        is used.

            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return len(self.teams)

    def __str__(self) -> str:
        output = []
        for game_week in self.schedule:
            for game in game_week:                
                home_team = game.home_team.get_players()
                away_team = game.away_team.get_players()
                home_team_name = game.home_team.get_name()
                away_team_name = game.away_team.get_name()
                home_goals = game.result['Home Goals'] 
                away_goals = game.result['Away Goals']
                
                goal_scorers = game.result['Goal Scorers'] if 'Goal Scorers' in game.result else "None"
                goal_assists = game.result['Goal Assists'] if 'Goal Assists' in game.result else "None"
                tackles = game.result['Tackles'] if 'Tackles' in game.result else "None"
                interceptions = game.result['Interceptions'] if 'Interceptions' in game.result else "None"
                
                game_str = (
                    f"{home_team_name} {home_goals} - {away_goals} {away_team_name}\n"
                    f"Goal Scorers: {goal_scorers}\n"
                    f"Goal Assists: {goal_assists}\n"
                    f"Tackles: {tackles}\n"
                    f"Interceptions: {interceptions}\n")
                
                output.append(game_str.strip()) 
            
        return "\n\n".join(output)

    def __repr__(self) -> str:
        """Returns a string representation of the Season object.
        Useful for debugging or when the Season is held in another data structure."""
        return f"Season(teams={self.teams}, schedule={self.schedule})"

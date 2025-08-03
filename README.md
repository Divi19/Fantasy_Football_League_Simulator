#Fantasy Football League Simulator

Welcome to the **Fantasy Football League Simulator**, which is a simulation-based system designed to model an entire fantasy football season. This project demonstrates the use of **advanced data structures and algorithms** to:
- Manage teams
- Simulate matches
- Update statistics
- Generate awards
- Organize a full schedule of games
- Reschedule postponed games

##Features
- **Player and Team Modeling:** Each player has a position and associated stats and each team consists of a fixed lineup of players.
- **Statistics Management:** Stats are updated automatically after each match, tracking points, goals, wins, and more through custom data structures such as hash tables.
- **Season Scheduling:** Randomized match scheduling ensures every team plays each other fairly across the season.
- **Awards System:** At season's end, the system awards the top players and teams based on performance.
- **Match Rescheduling:** In the event of severe weather or unforeseen circumstances, the system can postpone the affected match or matches to a later date without disrupting the existing schedule.
- **Custom Data Structures:**
  - Linked Lists and Queues for dynamic data management
  - Hash Tables with multiple implementation techniques such as Linear Probing, Double Hashing and Separate Chaining
  - Recursion-based schedule randomization
  - Array Sorted Lists incorporating Binary Search
  - Sets with bit vector implementation
- **Simulation Engine:** Matches are simulated with randomized scores, stat updates, and outcomes.

##Project Structure
|- main.py #Entry point for simulation
|- player.py #Player and PlayerStats logic
|- team.py #Team and player grouping logic
|- season.py #Full season manager and scheduler
|- game_simulator.py #Simulates games between the teams
|- constants.py #All the fixed values used in the program
|- random_gen.py #Random generator used for the match simulation
|- awards.py #Represents player and team rewards system
|- hashy_step_table.py #Hash table with Double Hashing
|- hashy_perfection_table.py #Hash table with perfect hash function for a small set of known keys
|- data structures/
| |- linked_list.py #Linked List implementation
| |- linked_queue.py #Linked Queue implementation
| |- hash_table.py #Hash table with Linear Probing
| |- hash_table_separate_chaining.py #Hash table with Separate Chaining
| |- array_sorted_list.py #Array sorted list using binary search
| |- bset.py #Sets using bit vector implementation

##Concepts Covered
- Abstract Data Types (ADTs)
- Linked Structures
- Hashing Techniques (Linear Probing, Separate Chaining, etc)
- Sorting and Searching
- Recursive Schedule Generation
- Dynamic Statistics Propagation
- Time Complexity Optimization

##How To Run
- Clone the repo by clicking the green 'Code' button, and then copy the HTTPS link of the repository
- Open Visual Studio Code, navigate to the source control section and click clone repository
- Paste the copied link into this box and hit enter
- Select the location where you want to store the folder/repository and click 'Open'
- The repository will be cloned, and you will now have access to the simulator

##Testing
- To use the test files, simply run this command in the terminal and just hit enter if you want to run all tests or you can specify the test number to run a specific one: python run_tests.py
- Each test file checks to see if parts of the program are functioning properly
- Print statements can be added to assist in debugging

#Learning Objectives
This project was built as part of a data structures and algorithms learning project. The goal is to reinforce concepts through a creative and engaging sport simulation environment that makes use of these data structures effectively.

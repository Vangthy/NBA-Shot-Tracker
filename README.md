# NBA-Shot-Tracker:
This project creates a shot chart of a player that the user inputs. It will also give stats such as how many years they have been in the league, assist per game, points per game, and more. It will also state their field goal percentage and three point percentage.

# Dependencies:
- [NumPy](https://numpy.org/) v1.21.0
- [Pandas](https://pandas.pydata.org/) v1.3.0
- [Matplotlib](https://matplotlib.org/) v3.4.3
- [NBA API](https://github.com/swar/nba_api)
  - [NBA API - players](https://github.com/swar/nba_api) v1.1.8
  - [NBA API - teams](https://github.com/swar/nba_api) v1.1.8
  - [NBA API - shotchartdetail](https://github.com/swar/nba_api) v1.1.8
  - [NBA API - playercareerstats](https://github.com/swar/nba_api) v1.1.8
 
# How to use:
1. Run the program
2. Input the player's name (It could just be their first or last name, and it will give you a list to pick from. Typing the players full name will just give you the player)
3. Input the season that you want from the player (ex. 1999-00). (Shots started being tracked in the 1996-97 season, so seasons before will print a empty shot chart. It will print their stats and the team they played for in the console)

# Installation
1. Download the project ZIP file.
2. Extract the contents.
3. Open a terminal or command prompt and navigate to the project directory.
4. Run the following command to install the required libraries:

```bash
python -m pip install -r requirements.txt
```

# Acknowledgment
I would like to acknowledge the following YouTube video for providing code snippets that were utilized in this project:

- [How to make NBA Shot Charts (PYTHON) | FlightReacts Inspired](https://www.youtube.com/watch?v=a3u-3gEYvxM)
  - Channel: Hobe

Certain parts of the code in this project were directly adapted from the examples provided in the mentioned video. Please check the video for detailed explanations and original code. It inspired me to create one and also how to use Python. I've never done data visualization in Python before, and it helped a lot with my understanding.

# Contributing
If you'd like to contribute to the project, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix: `git checkout -b feature-name`.
3. Make your changes and commit them: `git commit -m "Description of changes"`.
4. Push your branch to your fork: `git push origin feature-name`.
5. Open a pull request with a clear title and description.

Thank you for contributing!

# License
This project is licensed under the GNU General Public License v3.0- see the [LICENSE.md](https://github.com/Vangthy/NBA-Shot-Tracker/blob/main/LICENSE.md) file for details.

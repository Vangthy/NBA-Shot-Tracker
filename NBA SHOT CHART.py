# Author: Vangthy Lee
# Date: 3/12/2024
# Description: NBA Player Shot Charts and Statistics

# Importing necessary libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Arc
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playercareerstats


# Function to get player career statistics
def fetch_player_stats(player_id):
    """
        Retrieves career statistics for an NBA player based on their unique identifier.

        Parameters:
        - player_id (int): The unique identifier of the NBA player.

        Returns:
        pandas.DataFrame: A DataFrame containing career statistics for the specified player.
        """
    player_stats = playercareerstats.PlayerCareerStats(player_id=player_id).get_data_frames()[0]
    return player_stats


def obtain_team_name(team_id):
    """
        Retrieves the full name of an NBA team based on its ID.

        Parameters:
        - team_id (int): The unique identifier of the NBA team.

        Returns:
        str: The full name of the NBA team corresponding to the given team_id.
        """
    team_info = [team for team in teams.get_teams() if team['id'] == team_id][0]
    return team_info['full_name']



def get_player_shot_chart_detail(player_name, season_id):
    """
        Retrieves the shot chart details for a player in a specific season.

        Parameters:
        - player_name (str): The full name of the player.
        - season_id (str): The season year in the format YYYY-YY.

        Returns:
        Tuple containing the player's shot chart DataFrame and league average DataFrame.
    """
    # Get the player's name
    nba_players = players.get_players()
    player_dict = [player for player in nba_players if player['full_name'] == player_name][0]

    # Get player's career statistics
    career = playercareerstats.PlayerCareerStats(player_id=player_dict['id'])
    career_df = career.get_data_frames()[0]
    print(career_df)

    # Check if the player played in the specified season
    season_mask = career_df['SEASON_ID'].apply(lambda x: str(x)[:4] == season_id[:4])
    if not season_mask.any():
        print(f"Player {player_name} did not play in the {season_id} season.")
        return None, None

    # Get team ID for the specified season
    team_id = career_df[season_mask]['TEAM_ID'].iloc[0]
    team_name = obtain_team_name(team_id)  # Get the team name
    print(f"Team for the season {season_id} : {team_name} ({team_id})")

    # Get shot chart details using the NBA API
    try:
        shotchartlist = shotchartdetail.ShotChartDetail(team_id=int(team_id),
                                                        player_id=int(player_dict['id']),
                                                        season_type_all_star='Regular Season',
                                                        season_nullable=season_id,
                                                        context_measure_simple='FGA').get_data_frames()
    except KeyError:
        print("Error: Failed to retrieve shot chart details from the NBA API.")
        return None, None

    # Get player statistics
    player_stats = fetch_player_stats(player_dict['id'])

    # Extract relevant career statistics
    season_stats = player_stats[player_stats['SEASON_ID'] == season_id]
    games_played = season_stats['GP'].iloc[0]  # GP is the column for games played
    ppg = round(season_stats['PTS'].iloc[0] / games_played, 1)
    apg = round(season_stats['AST'].iloc[0] / games_played, 1)
    rpg = round(season_stats['REB'].iloc[0] / games_played, 1)

    print(f"PPG: {ppg}, APG: {apg}, RPG: {rpg}")

    return shotchartlist[0], shotchartlist[1]


def draw_basketball_court(ax=None, color="blue", lw=1, outer_lines=False, shotzone=False):
    """Returns an axes with a basketball court drawn onto to it.
        This function draws a court based on the x and y-axis values that the NBA
        stats API provides for the shot chart data.  For example the center of the
        hoop is located at the (0,0) coordinate.  Twenty-two feet from the left of
        the center of the hoop in is represented by the (-220,0) coordinates.
        So one foot equals +/-10 units on the x and y-axis.
        Parameters
        ----------
        ax : Ax es, optional
            The Axes object to plot the court onto.
        color : matplotlib color, optional
            The color of the court lines.
        lw : float, optional
            The linewidth the of the court lines.
        outer_lines : boolean, optional
            If `True` it draws the out of bound lines in same style as the rest of
            the court.
        Returns
        -------
        ax : Axes
            The Axes object with the court on it.
    """
    if ax is None:
        ax = plt.gca()

    # Basketball hoop
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Backboard
    backboard = Rectangle((-30, -12.5), 60, 0, linewidth=lw, color=color)

    # The paint
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
    # Create the inner box of the paint, widt=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False)

    # Free Throw Top Arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color, fill=False)

    # Free Throw Bottom Arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color, fill=False)

    # Restricted Zone
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)

    # Three Point Line
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw, color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0, linewidth=lw, color=color)

    # Display the legend with customized entries
    made_legend_marker = plt.Line2D([0], [0], marker='o', color='green', markersize=10, linestyle='None',
                                    fillstyle='none', markeredgewidth=2, markeredgecolor='green', label='Made Shots')
    missed_legend_marker = plt.Line2D([0], [0], marker='x', color='red', markersize=10, linestyle='None',
                                      markeredgewidth=2, label='Missed Shots')
    legend_handles = [made_legend_marker, missed_legend_marker]

    # Set the legend outside the plot area
    plt.legend(handles=legend_handles, bbox_to_anchor=(-.165, .10), loc='center left')

    # Draw shotzone Lines
    # Based on Advanced Zone Mode
    if (shotzone == True):
        inner_circle = Circle((0, 0), radius=80, linewidth=lw, color='black', fill=False)
        outer_circle = Circle((0, 0), radius=160, linewidth=lw, color='black', fill=False)
        corner_three_a_x = Rectangle((-250, 92.5), 30, 0, linewidth=lw, color=color)
        corner_three_b_x = Rectangle((220, 92.5), 30, 0, linewidth=lw, color=color)

        # 60 degrees
        inner_line_1 = Rectangle((40, 69.28), 80, 0, 60, linewidth=lw, color=color)
        # 120 degrees
        inner_line_2 = Rectangle((-40, 69.28), 80, 0, 120, linewidth=lw, color=color)

        # Assume x distance is also 40 for the endpoint
        inner_line_3 = Rectangle((53.20, 150.89), 290, 0, 70.53, linewidth=lw, color=color)
        inner_line_4 = Rectangle((-53.20, 150.89), 290, 0, 109.47, linewidth=lw, color=color)

        # Assume y distance is also 92.5 for the endpoint
        inner_line_5 = Rectangle((130.54, 92.5), 80, 0, 35.32, linewidth=lw, color=color)
        inner_line_6 = Rectangle((-130.54, 92.5), 80, 0, 144.68, linewidth=lw, color=color)
        # List of the court elements to be plotted onto the axes
        court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                          bottom_free_throw, restricted, corner_three_a,
                          corner_three_b, three_arc, center_outer_arc,
                          center_inner_arc, inner_circle, outer_circle,
                          corner_three_a_x, corner_three_b_x,
                          inner_line_1, inner_line_2, inner_line_3, inner_line_4, inner_line_5, inner_line_6]
    else:
        # List of the court elements to be plotted onto the axes
        court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                          bottom_free_throw, restricted, corner_three_a,
                          corner_three_b, three_arc, center_outer_arc,
                          center_inner_arc]
    if outer_lines:
        # Draw the half court line, baseline and side out bound lines
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                color=color, fill=False)
        court_elements.append(outer_lines)

        # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax


def plot_shot_chart(data, title="", color="b",
                    xlim=(-250, 250), ylim=(422.5, -47.5), line_color="blue",
                    court_color="white", court_lw=2, outer_lines=False,
                    flip_court=False, gridsize=None,
                    ax=None, despine=False, **kwargs):
    """
        Plots an NBA shot chart based on the provided data.

        Parameters:
        - data (pandas.DataFrame): DataFrame containing shot data, including columns 'EVENT_TYPE', 'LOC_X', and 'LOC_Y'.
        - title (str): Title for the plot.
        - color (str): Color for the shot markers.
        - xlim (tuple): X-axis limits for the plot.
        - ylim (tuple): Y-axis limits for the plot.
        - line_color (str): Color for the court lines.
        - court_color (str): Color for the court background.
        - court_lw (int): Line width for the court lines.
        - outer_lines (bool): Whether to draw outer lines on the court.
        - flip_court (bool): If True, flips the court horizontally.
        - gridsize (None or int): Grid size for the plot.
        - ax (matplotlib.axes.Axes, optional): Axes object to plot onto. If None, uses the current Axes.
        - despine (bool): If True, removes spines from the plot.
        - **kwargs: Additional keyword arguments to pass to scatter plot.

        Returns:
        matplotlib.axes.Axes: The Axes object containing the shot chart.
        """
    if ax is None:
        ax = plt.gca()

    if not flip_court:
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
    else:
        ax.set_xlim(xlim[::-1])
        ax.set_ylim(ylim[::-1])

    ax.tick_params(labelbottom="off", labelleft="off")
    ax.set_title(title, fontsize=18)

    # draws the court
    draw_basketball_court(ax, color=line_color, lw=court_lw, outer_lines=outer_lines)

    # separate color by make or miss
    x_missed = data[data['EVENT_TYPE'] == 'Missed Shot']['LOC_X']
    y_missed = data[data['EVENT_TYPE'] == 'Missed Shot']['LOC_Y']

    x_made = data[data['EVENT_TYPE'] == 'Made Shot']['LOC_X']
    y_made = data[data['EVENT_TYPE'] == 'Made Shot']['LOC_Y']

    # plot missed shots
    ax.scatter(x_missed, y_missed, c='r', marker="x", s=300, linewidths=3, **kwargs)
    # plot made shots
    ax.scatter(x_made, y_made, facecolors='none', edgecolors='g', marker="o", s=100, linewidths=3, **kwargs)

    # Set the spines to match the rest of court lines, makes outer_lines
    # somewhate unnecessary
    for spine in ax.spines:
        ax.spines[spine].set_lw(court_lw)
        ax.spines[spine].set_color(line_color)

    if despine:
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

    return ax


def calculate_fg_percentage(made_shots, total_shots):
    """
        Calculates the field goal percentage based on made and total shot attempts.

        Parameters:
        - made_shots (int): Number of shots made.
        - total_shots (int): Total number of shot attempts.

        Returns:
        float: The calculated field goal percentage.
    """
    # Check if the player attempted any shots during the specified season
    if total_shots > 0:
        # Calculate and return the field goal percentage
        return (made_shots / total_shots) * 100
    else:
        # If no shots were attempted, return 0 as the field goal percentage
        return 0


# Function to get player information by name
def find_player_by_name(player_name):
    """
        Finds an NBA player by their name and provides information about the player.

        Parameters:
        - player_name (str): The name of the player to search for.

        Returns:
        dict or None: A dictionary containing information about the selected player,
                     or None if no player is found.
    """
    # Retrieve the list of all NBA players
    nba_players = players.get_players()

    # Search for players with the input name
    matching_players = [player for player in nba_players if player_name.lower() in player['full_name'].lower()]

    # If no matching player is found, notify the user
    if not matching_players:
        print(f"No player found with the name '{player_name}'.")
        return None

    # If multiple players are found with similar names, let the user choose
    if len(matching_players) > 1:
        print("Multiple players found with similar names. Please choose one:")
        for i, player in enumerate(matching_players, start=1):
            print(f"{i}. {player['full_name']}")

        choice = int(input("Enter the corresponding number: "))
        selected_player = matching_players[choice - 1]
    else:
        # If only one player is found, select that player
        selected_player = matching_players[0]

    # Display the selected player's name
    print(f"\nSelected player: {selected_player['full_name']}")

    # Get player career statistics
    career = playercareerstats.PlayerCareerStats(player_id=selected_player['id'])
    career_df = career.get_data_frames()[0]

    # Display the years the player has played
    played_years = sorted(career_df['SEASON_ID'].unique(), reverse=True)
    print(f"\nYears the player has played: {', '.join(played_years)}")

    return selected_player


def main():
    """
        The main function for user interaction.

        This function prompts the user for input, retrieves information about the selected player,
        and displays a shot chart for the specified season along with field goal statistics.

        Returns:
        None
    """
    # Prompt the user for input
    user_input = input(
        "Enter the Name of the Player (Shot chart gets created in the 1996-97 season and onwards. Prior seasons will not have a shot chart): ")
    selected_player = find_player_by_name(user_input)
    if selected_player:
        # Get shot chart details for the selected player in a specific season
        # Prompt the user for the season year
        season_year = input("Enter the season year (Example: 1996-97): ")
        player_shotchart_df, league_avg = get_player_shot_chart_detail(selected_player['full_name'], season_year)

        # Check if player_shotchart_df is not None
        if player_shotchart_df is not None:
            # Set the title dynamically using the player's name
            title = f"{selected_player['full_name']}'s Shot Chart : " + season_year + " Season"

            # Set the figure size
            plt.rcParams['figure.figsize'] = (12, 11)

            # Plot the shot chart with the dynamic title
            plot_shot_chart(player_shotchart_df, title=title)

            # Field goal percentage
            fg_percentage = calculate_fg_percentage(player_shotchart_df['SHOT_MADE_FLAG'].sum(),
                                                    len(player_shotchart_df))

            # Count the total number of 3-point attempts
            three_point_attempted = len(player_shotchart_df[player_shotchart_df['SHOT_TYPE'] == '3PT Field Goal'])

            # Count the number of made 3-pointers
            three_point_made = player_shotchart_df[player_shotchart_df['SHOT_TYPE'] == '3PT Field Goal'][
                'SHOT_MADE_FLAG'].sum()

            # Calculate the 3-point field goal percentage
            three_point_fg_percentage = (
                                                three_point_made / three_point_attempted) * 100 if three_point_attempted > 0 else 0

            # Display field goal percentage
            plt.text(246, 455,
                     f'FG%: {fg_percentage:.2f}% ({player_shotchart_df["SHOT_MADE_FLAG"].sum()} - {len(player_shotchart_df)})',
                     ha='right', fontsize=14)

            # Display the 3-point field goal percentage
            plt.text(246, 470,
                     f'3 Point FG%: {three_point_fg_percentage:.2f}% ({three_point_made} - {three_point_attempted})',
                     ha='right', fontsize=14)

            # Show the plot
            plt.show()


if __name__ == "__main__":
    main()

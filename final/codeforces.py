import requests
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.ticker import FuncFormatter
import mplcursors  # Import mplcursors library
import os  # Import the os module

# Set the style for seaborn (optional)
sns.set(style='whitegrid')

# Username for the user you want to fetch data for
username = 'skqliiiao'

# Function to fetch user information from Codeforces API
def get_codeforces_user_info(username):
    url = f'https://codeforces.com/api/user.info?handles={username}'
    response = requests.get(url)
    data = response.json()
    return data

# Function to fetch user's solved problems from Codeforces API
def get_codeforces_solved_problems(username):
    url = f'https://codeforces.com/api/user.status?handle={username}&from=1&count=100000'
    response = requests.get(url)
    data = response.json()
    return data

# Function to fetch user's Codeforces rating history
def get_codeforces_rating_history(username):
    url = f'https://codeforces.com/api/user.rating?handle={username}'
    response = requests.get(url)
    data = response.json()
    return data

# Define a custom function to format y-axis labels
def format_func(value, tick_number):
    return f'{int(value):,}'

if __name__ == '__main__':
    # Get user information
    user_info = get_codeforces_user_info(username)

    if user_info['status'] != 'OK':
        print(f"Failed to fetch user information for {username}.")
    else:
        user_info = user_info['result'][0]
        # print(f"Codeforces Profile for {user_info['handle']}:")
        # print(f"Rating: {user_info.get('rating', 'Not available')}")
        # print(f"Max Rating: {user_info.get('maxRating', 'Not available')}")

        # Calculate the total solved problems count based on API data
        solved_problems_data = get_codeforces_solved_problems(username)

        if solved_problems_data['status'] != 'OK':
            print(f"Failed to fetch solved problems data for {username}.")
        else:
            solved_problems = set()  # To keep track of solved problems
            rating_count_map = {}  # To count problems by rating

            for problem in solved_problems_data['result']:
                if 'contestId' in problem and 'index' in problem['problem']:
                    problem_id = f"{problem['contestId']}{problem['problem']['index']}"
                    verdict = problem.get('verdict', '')

                    try:
                        # Handle "Unrated" ratings by assigning a value of 700
                        problem_rating_str = problem['problem']['rating'] if 'rating' in problem['problem'] else 'Unrated'
                        problem_rating = int(problem_rating_str) if problem_rating_str != 'Unrated' else 700

                        if verdict == 'OK':
                            problem_name = problem['problem']['name']

                            # Count the problem by rating
                            if problem_rating in rating_count_map:
                                rating_count_map[problem_rating] += 1
                            else:
                                rating_count_map[problem_rating] = 1

                            solved_problems.add(problem_id)
                    except ValueError:
                        # Handle cases where the rating is not a valid integer
                        pass

            total_solved_problems = len(solved_problems)
            print(f"Total Solved Problems: {total_solved_problems}")

            # Sort the rating_count_map by rating in non-decreasing order
            sorted_rating_count = sorted(rating_count_map.items(), key=lambda x: x[0])

            # Extract ratings and problem counts for the graph
            ratings, solved_counts = zip(*sorted_rating_count)

            # Convert ratings and solved_counts to lists
            ratings = list(ratings)
            solved_counts = list(solved_counts)

            # Replace 700 with "Unrated" for x-label
            ratings = ["Unrated" if rating == 700 else rating for rating in ratings]

            # Define a custom color dictionary (add more as needed)
            rating_colors = {
                800: 'lightgrey',
                900: 'lightgrey',
                1000: 'lightgrey',
                1100: 'lightgrey',
                1200: 'lightgreen',
                1300: 'lightgreen',
                1400: 'turquoise',
                1500: 'turquoise',
                1600: 'cornflowerblue',
                1700: 'cornflowerblue',
                1800: 'cornflowerblue',
                1900: 'orchid',
                2000: 'orchid',
                2100: 'yellow',
                2200: 'yellow',
                2300: 'gold',
                2400: 'coral',
                2500: 'coral',
                2600: 'indianred',
                2700: 'indianred',
                2800: 'indianred',
                2900: 'indianred',
                3000: 'maroon',
                3100: 'maroon',
                3200: 'maroon',
                3300: 'maroon',
                3400: 'maroon',
                3500: 'maroon',
            }

            # Create a beautiful bar graph with custom colors
            plt.figure(figsize=(10, 6))
            ax = sns.barplot(x=ratings, y=solved_counts, palette=[rating_colors.get(rating, 'gray') for rating in ratings])

            # Add labels and title
            plt.xlabel('Rating')
            plt.ylabel('Number of Problems Solved')
            plt.title('Number of Problems Solved by Rating')

            # Show the graph
            plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

            # Add count labels on bars
            for p, label in zip(ax.patches, solved_counts):
                ax.annotate(format_func(label, None), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center',
                            va='center', fontsize=10, color='black', xytext=(0, 5),
                            textcoords='offset points')

            # Add total problems solved as footer with a lower position
            total_solved_problems_text = f'Total Solved Problems: {total_solved_problems}'
            footer_position = -0.2  # Adjust this value to move the text lower
            plt.text(0.02, footer_position, total_solved_problems_text, transform=ax.transAxes, fontsize=12)


            # Format y-axis labels with commas
            ax.yaxis.set_major_formatter(FuncFormatter(format_func))

            #plt.show()
            # Show the graph
            plt.grid(True)
            plt.tight_layout()

            # Save the graph with a filename based on the date
            output_directory = "Problem_Solved"  # Change this to your desired directory path
            os.makedirs(output_directory, exist_ok=True)  # Create the directory if it doesn't exist
            timestamp = pd.Timestamp.now().strftime('%Y_%m_%d')
            graph_filename = f'{username}_problems_graph_{timestamp}.png'

            graph_filepath = os.path.join(output_directory, graph_filename)

            # Check if the file already exists, and if so, remove it
            if os.path.exists(graph_filepath):
                os.remove(graph_filepath)

            plt.savefig(graph_filepath)

            latest_dict = "Latest_Info"
            os.makedirs(latest_dict, exist_ok=True)
            graph_filename = 'solved_problems_graph.png'
            graph_filepath = os.path.join(latest_dict, graph_filename)

            if os.path.exists(graph_filepath):
                os.remove(graph_filepath)
            plt.savefig(graph_filepath)

            # Close the figure to free up resources (optional)
            plt.close()

        # Fetch user's Codeforces rating history
        rating_history_data = get_codeforces_rating_history(username)

        if rating_history_data['status'] != 'OK':
            print(f"Failed to fetch rating history data for {username}.")
        else:
            rating_history = rating_history_data['result']

            # Extract dates and ratings
            dates = [entry['ratingUpdateTimeSeconds'] for entry in rating_history]
            ratings = [entry['newRating'] for entry in rating_history]

            # Convert dates to datetime objects
            dates = [pd.to_datetime(date, unit='s') for date in dates]

            # Plot the rating history
            plt.figure(figsize=(12, 6))
            plt.plot(dates, ratings, label='Rating', marker='o', markersize=5, linestyle='-', color='blue')

            # Find the highest rating and the most recent rating
            highest_rating = max(ratings)
            current_rating = ratings[-1]

            # Highlight the highest rating with a red point
            plt.scatter(dates[ratings.index(highest_rating)], highest_rating, color='red', edgecolor='red',
                        label=f'Highest Rating: {highest_rating}')

            # Highlight the current rating with a yellow point
            plt.scatter(dates[-1], current_rating, color='yellow', edgecolor='yellow',
                        label=f'Current Rating: {current_rating}')

            # Add labels and title
            plt.xlabel('Date')
            plt.ylabel('Rating')
            plt.title('Codeforces Rating History')

            # Format y-axis labels with commas
            ax = plt.gca()
            ax.yaxis.set_major_formatter(FuncFormatter(format_func))

            # Show a legend
            plt.legend()

            # Show the graph
            mplcursors.cursor(hover=True)  # Enable hover text on the rating history plot
            plt.grid(True)
            plt.tight_layout()
            #plt.show()
            # Show the graph
            plt.grid(True)
            plt.tight_layout()

            # Save the graph with a filename based on the date
            output_directory = "Contest_Rating"  # Change this to your desired directory path
            os.makedirs(output_directory, exist_ok=True)  # Create the directory if it doesn't exist
            timestamp = pd.Timestamp.now().strftime('%Y_%m_%d')
            graph_filename = f'{username}_rating_graph_{timestamp}.png'

            graph_filepath = os.path.join(output_directory, graph_filename)

            # Check if the file already exists, and if so, remove it
            if os.path.exists(graph_filepath):
                os.remove(graph_filepath)


            plt.savefig(graph_filepath)

            latest_dict = "Latest_Info"
            os.makedirs(latest_dict, exist_ok=True)
            graph_filename = 'contest_rating_graph.png'
            graph_filepath = os.path.join(latest_dict, graph_filename)

            if os.path.exists(graph_filepath):
                os.remove(graph_filepath)
            plt.savefig(graph_filepath)

            # Close the figure to free up resources (optional)
            plt.close()

import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Please enter the city you want to search on the right. (chicago, new_york_city, washington): ").lower()
        if city.lower() not in ['chicago', 'new_york_city', 'washington']:
            print("Please enter a valid city.")
            continue
        else:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month_mapping = {
            'january': 1,
            'february': 2,
            'march': 3,
            'april': 4,
            'may': 5,
            'june': 6,
            'july': 7,
            'august': 8,
            'september': 9,
            'october': 10,
            'november': 11,
            'december': 12
        }

        month_input = input("Please enter the month you want to search. (all, January, February, March...December): ").lower()
        month_input_lower = month_input.lower()
        if month_input_lower in "all":
            month = month_input_lower
            break
        elif month_input_lower in month_mapping:
            month = month_mapping[month_input_lower]
            break
        else:
            print("Please enter a valid month.")
            continue

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Please enter the day of the week you want to search. (all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday): ").title()
        if day.lower() not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            print("Please enter a valid day of the week.")
            continue
        else:
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    while True:
        df = pd.read_csv(city + '.csv')
        #Columns unnamed = 0  drop
        df.drop(columns='Unnamed: 0', inplace=True)
        #Missing values
        df.fillna(method='ffill', inplace=True)

        df['Start Time'] = pd.to_datetime(df['Start Time'], format='%Y-%m-%d %H:%M:%S')
        # extract day from 'Start Time' column to create 'Day' column.
        df['Day'] = df['Start Time'].dt.day_name()

        if month != 'all':
            df = df[df['Start Time'].dt.month == int(month)] 

        # Filter by day
        if day != 'All':
            df = df[df['Day'] == day]

        if df.empty:
            print("No data corresponding to the month and day of the week, please re-enter.")
            city, month, day = get_filters()
            continue

        break

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    start_time = time.time()
        
    # TO DO: display the most common month
    most_common_month = df['Start Time'].dt.month_name().mode()[0]  
    print(f"the most month: {most_common_month}")


    # TO DO: display the most common day of week
    most_common_day = df['Start Time'].dt.day_name().mode()[0]  
    print(f"the most day of week: {most_common_day}")


    # TO DO: display the most common start hour
    most_common_hour = df['Start Time'].dt.hour.mode()[0]  
    print(f"the most start hour: {most_common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print(f"most commonly used start station: {most_common_start_station}")

    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print(f"most commonly used end station: {most_common_end_station}")

    # TO DO: display most frequent combination of start station and end station trip
    most_common_combination_per_row = df.apply(lambda row: (row['Start Station'], row['End Station']), axis=1).mode().iloc[0]
    print(f"most frequent combination of start station and end station trip: {most_common_combination_per_row}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    total_trip_duration_minutes = round(total_trip_duration / 60, 1)
    print(f"total travel time(minutes): {total_trip_duration_minutes} minutes")

    # TO DO: display mean travel time
    average_trip_duration = df['Trip Duration'].mean()
    print(f"mean travel time (seconds): {average_trip_duration}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type_counts = df['User Type'].value_counts()
    for user_type, count in user_type_counts.items():
        print(f"{user_type}: {count}")

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        Gender_counts = df['Gender'].value_counts()
        for Gender_type, count in Gender_counts.items():
            print(f"{Gender_type}: {count}")
    else:
        print("The 'Gender' column does not exist.")

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        df['Birth Year'] = pd.to_numeric(df['Birth Year'], errors='coerce')
        earliest_birth_year = df['Birth Year'].dropna().min()
        print(f"earliest year: {int(earliest_birth_year)}")


        latest_birth_year = df['Birth Year'].dropna().max()
        print(f"most recent year: {int(latest_birth_year)}")


        most_common_birth_year = df['Birth Year'].dropna().mode()[0]
        print(f"most year: {int(most_common_birth_year)}")
    else:
        print(" The 'Birth Year' column does not exist.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#5줄의 데이터를 보는 함수
def data_view(df):
    start_row = 0
    total_rows = len(df)
    
    while start_row < total_rows:
        view = input('\nDo you want to see more data? Enter yes or no.\n')
        
        if view.lower() == 'yes':
            print(df.iloc[start_row : start_row + 5])
            start_row += 5
        else:
            break

    print("No more data to display. Exiting...")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data_view(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

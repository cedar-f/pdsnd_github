import time
import pandas as pd
import numpy as np
from tabulate import tabulate

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

FILTERS = np.array(['months', 'weekdays', 'both', 'none'])

MONTH = np.array(['january', 'february', 'march', 'april', 'may', 'june'])

WEEKDAYS = np.array(['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'])

QUESTION_LIST = {
    'city': 'Which city(ies) do you want do select data? Use commas to list the names.'
    , 'filter': 'Would you like to filter data by month,day,both or not at all?'
    , 'month': 'Which month(s) do you want do filter data? Use commas to list the names.'
    , 'weekday': 'Which weekday(s) do you want do filter data? Use commas to list the names.'
}


def get_user_choice(prompt, valid_choice):
    """ check user answer is valid or not and return it"""

    valid_choice = np.array(valid_choice)

    prompt = prompt + '\n(valid answer: ' + ','.join(valid_choice) + ' )\n>'
    while True:
        choice = input(prompt)
        choice_arr = np.char.strip(np.array(choice.lower().split(',')))
        is_valid_choice = np.isin(choice_arr, valid_choice)
        invalid_choice = [str(choice_arr[index]) for index, value in enumerate(is_valid_choice) if not value]
        if len(invalid_choice) > 0:
            print(
                f'Something is not right. Please mind the formatting and be sure to enter a valid option\n Invalid answer {",".join(invalid_choice)}')
        else:
            return choice_arr


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (ndarray) city - name of the city to analyze
        (ndarray) month - name of the month to filter by, or "all" to apply no month filter
        (ndarray) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    months = np.array([])
    days = np.array([])

    print('Hello! Let\'s explore some US bikeshare data!')
    print('-' * 40)

    cities = get_user_choice(QUESTION_LIST['city'], list(CITY_DATA.keys()))
    print('-' * 30)
    filters = get_user_choice(QUESTION_LIST['filter'], FILTERS)
    print('-' * 30)

    if 'both' in filters:
        months = get_user_choice(QUESTION_LIST['month'], MONTH)
        print('-' * 30)
        days = get_user_choice(QUESTION_LIST['weekday'], WEEKDAYS)
    elif 'months' in filters:
        months = get_user_choice(QUESTION_LIST['month'], MONTH)
    elif 'weekdays' in filters:
        days = get_user_choice(QUESTION_LIST['weekday'], WEEKDAYS)

    print('-' * 40)
    return cities, months, days


def load_data(cities, months, days):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (ndarray) city - name of the city to analyze
        (ndarray) month - name of the month to filter by, or "all" to apply no month filter
        (ndarray) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print("\nThe program is loading the data for the filters of your choice.")
    start_time = time.time()

    df = pd.DataFrame([])

    for city in cities:
        file_name = CITY_DATA[city]
        print(file_name)
        if len(df) == 0:
            df = pd.read_csv(file_name)
            df.insert(1, 'City', city)
        else:
            sub_df = pd.read_csv(file_name)
            sub_df.insert(1, 'City', city)
            df = pd.concat([df, sub_df])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df.insert(4, 'Month', pd.to_datetime(df['Start Time']).dt.month_name())
    df.insert(5, 'Weekday', pd.to_datetime(df['Start Time']).dt.day_name())

    if len(months) > 0:
        df = df.query('Month.str.lower() in @months', engine='python')
    if len(days) > 0:
        df = df.query('Weekday.str.lower() in @days', engine='python')

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-' * 40)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['Month'].mode()[0]
    print('Most popular month: ' + most_common_month)

    # display the most common day of week
    most_common_weekday = df['Weekday'].mode()[0]
    print('Most popular weekday: ' + most_common_weekday)

    # display the most common start hour
    most_common_hours = df['Start Time'].dt.hour.mode()[0]
    print('Most popular hour: ' + str(most_common_hours))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('Most popular start station: ' + most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('Most popular end station: ' + most_common_end_station)

    # display most frequent combination of start station and end station trip
    most_common_station_set = ('[' + df['Start Station'] + '] - [' + df['End Station'] + ']').mode()[0]
    print('Most popular of combination between start/end station: ' + most_common_station_set)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = (df['End Time'] - df['Start Time']).sum()
    print('Total travel time: ' + str(total_travel_time))

    # display mean travel time
    mean_travel_time = (df['End Time'] - df['Start Time']).mean() / pd.Timedelta(minutes=1)
    print('Mean travel time: ' + str(mean_travel_time) + ' minute(s)')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    try:
        print('Counts of user types')
        count_of_user_types = df.groupby('User Type').size()
        for index, value in count_of_user_types.items():
            print(f"{index}: {value}")
    except:
        pass

    try:
        # Display counts of gender
        count_of_genders = df.groupby('Gender').size()
        print('\n\nCounts of genders')
        for index, value in count_of_genders.items():
            print(f"{index}: {value}")
    except:
        pass

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year = df['Birth Year'].min().astype(int)
        print('\n\nEarliest year: ' + str(earliest_year))
    except:
        pass
    try:
        most_recent_year = df['Birth Year'].max().astype(int)
        print('Most recent year: ' + str(most_recent_year))
    except:
        pass
    try:
        most_popular_year = df['Birth Year'].mode()[0].astype(int)
        print('Most popular year: ' + str(most_popular_year))
    except:
        pass

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def show_raw_data(df):
    while True:
        choice = input('Do you want to see raw data? (Press \'y\' for yes and \'n\' for no)\n>')
        if choice == 'y':
            total_row = df.shape[0]
            continue_show = 1
            begin_index = 0
            while continue_show == 1:
                print(f'row {begin_index + 1} - {begin_index + 5} of total {total_row} rows\n')
                print(tabulate(df.iloc[begin_index: begin_index + 5], headers='keys', tablefmt='psql'))
                begin_index = begin_index + 5
                choice_continue = input(
                    'Do you want to go to next page? (Press \'y\' to continue and \'n\' for exit)\n>')
                if choice_continue == 'y':
                    continue_show = 1
                elif choice_continue == 'n':
                    continue_show = 0
                    break
                else:
                    print('Invalid answer, please type again\n')
                    input("Press any key to continue...")
            break
        elif choice == 'n':
            break

        else:
            print('Invalid answer, please type again\n')
            input("Press any key to continue...")


def main():
    while True:
        # get filters from user
        cities, months, days = get_filters()

        # load data depend on filters
        df = load_data(cities, months, days)

        # show data loaded
        show_raw_data(df)
        time_stats(df)
        input("Press any key to continue...\n" + "-" * 30)
        station_stats(df)
        input("Press any key to continue...\n" + "-" * 30)
        trip_duration_stats(df)
        input("Press any key to continue...\n" + "-" * 30)
        user_stats(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

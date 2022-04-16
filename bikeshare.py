import time
import pandas as pd
import numpy as np
import pandasql

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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    C=["chicago", "new york city", "washington"]
    city=""
    while city not in C:
        city=input("Enter the name of the city: ").lower()
        
        
    # get user input for month (all, january, february, ... , june)
    M=["all","january", "february", "march", "april", "may", "june"]
    month=""
    while month not in M:
        month=input("Enter the name of the month to filter by or 'all': ")
        
        
    # get user input for day of week (all, monday, tuesday, ... sunday)
    D=["all","tuesday", "wednesday", "thursday", "friday", "saturday","sunday","monday" ]
    day=""
    while day not in D:
        day=input("Enter the name of the day of week to filter by or 'all': ")
        
        
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
    df =pd.read_csv(CITY_DATA[city])
    if month != "all":
        month=month.title()
    if day != "all":    
        day=day.title()
    df["Start Time"]=pd.to_datetime(df['Start Time'])
    df["month"]=df['Start Time'].dt.month_name()
    df["day"]=df['Start Time'].dt.day_name()
    df["hour"]=df['Start Time'].dt.hour
    df["frequent combination"] = df["Start Station"]+" --> "+df["End Station"]
    
    if month == "all" and day=="all":
        q="select * from df "
    elif month == "all" and day!="all" :
        q = "select * from df where day = '{}'".format(day)
    elif month != "all" and day=="all" :   
        q="select * from df where month = '{}'".format(month)
    else:
        q="select * from df where month = '{}' and day = '{}'".format(month,day)
        
    df=pandasql.sqldf(q)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    mcms = df["month"].mode()
    mcm = mcms[0]
    print("Most common month: {}".format(mcm))
    # display the most common day of week
    mcds = df["day"].mode()
    mcd = mcds[0]
    print("Most common day of week: {}".format(mcd))
    # display the most common start hour
    mchs = df["hour"].mode()
    mch = mchs[0]
    print("Most common start hour: {}".format(mch))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    csss=df["Start Station"].mode()
    css=csss[0]
    print("Most commonly used start station: {}".format(css))
    # display most commonly used end station
    cess=df["End Station"].mode()
    ces=cess[0]
    print("Most commonly used end station: {}".format(ces))

    # display most frequent combination of start station and end station trip
    cfts=df["frequent combination"].mode()
    cft=cfts[0]
    print("Most frequent combination of start station and end station trip: {}".format(cft))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    ttt=df["Trip Duration"].sum()
    print("total travel time: {} seconds".format(ttt))
    
    # display mean travel time
    mtt=df["Trip Duration"].mean()
    print("mean travel time: {} seconds".format(mtt))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    s=df["User Type"].value_counts()
    for i in s.index :
        print("The count of {} : {}".format(i,s[i]))

    try:
        # Display counts of gender
        g=df["Gender"].value_counts()
        for i in g.index :
            print("The count of {} : {}".format(i,g[i]))
    except KeyError:
        print("No Gender column found.")
    
    try:
        # Display earliest, most recent, and most common year of birth
        ys=df["Birth Year"].value_counts()
        ys_index=ys.index
        print("Earliest year of birth: {}".format(int(ys_index[-1])))
        print("Most recent year of birth: {}".format(int(ys_index.max())))
        print("Most common year of birth: {}".format(int(ys_index[0])))
    except KeyError:
        print("No Birth Year column found.")   

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
 
def displayRawData(df):
    start=0
    end = start+5
    a=input("Would you like to view 5 rows of individual trip data? (yes or no):")
    
    while end < len(df.index) and a.lower() =="yes":
        print(df.iloc[start:end])
        start = end
        if end+5 < len(df.index):
            end+=5
        else:
            end = len(df.index)
        
        a=input("Would you like to view 5 rows of individual trip data? (yes or no):")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        displayRawData(df)
        
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

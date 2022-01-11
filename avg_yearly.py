import pandas as pd



def rolling_mean_avg():
    """
    [ - Reads historical data on women representation in parliament
      - Calculates average value by 'year' and rolling mean (windon=5 by default) of 'women_perc' (numerical attribute) 
      - Saves output to csv file ]
    """
    # read data
    df = pd.read_csv('./data/women_in_parliament-historical_database-1945_to_2018_cleaned.csv')

    # calculate yearly average of all countries and rolling mean
    avg_yearly = pd.DataFrame(df.groupby(['year'])['women_perc'].mean())
    avg_yearly['women_perc'] = round(avg_yearly['women_perc'], 2)
    avg_yearly['RM5'] = avg_yearly['women_perc'].rolling(window=5).mean()
    avg_yearly['RM5'] = round(avg_yearly['RM5'], 2)
    
    avg_yearly['decade'] = avg_yearly.index//10*10
    avg_yearly['decade'] = avg_yearly['decade']%100

    avg_yearly['year_in_decade'] = avg_yearly.index%10
    print(avg_yearly.head(10))


    # save output
    avg_yearly.to_csv('./data/avg_yearly.csv')

if __name__ == "__main__":
    rolling_mean_avg()   
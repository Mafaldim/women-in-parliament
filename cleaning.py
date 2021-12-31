import pandas as pd
import numpy as np
import seaborn as sns


if __name__ == "__main__":
        
    # Read data
    df = pd.read_excel('./data/women_in_parliament-historical_database-1945_to_2018.xlsx')

    # Rename columns
    df.rename(columns={
        'Country':'country',
        'Region':'region',
        'Election / Renewal': 'election_renewal',
        'Year':'year',
        'Month':'month',
        'Chamber Type': 'chamber_type',
        'Chamber Total Seats': 'chamber_total_seats',
        'Total women': 'women_total',
        '% Of Women in Chamber': 'women_perc',
        'NOTES':'notes'
    }, inplace=True)

    # Transform to numeric columns listed as categorical ('women_total', 'women_perc')
    ## replace non-numerical values for 'women_total' attribute
    #non_numerical_values = [print(item) for i,item in enumerate(temp) if type(item)!= int] #print non-numerical values
    to_replace_dct = {
        '?': np.nan,
        'na':np.nan,
        'Not available':np.nan,
        'nan':np.nan,
        '7 5': 6,
        '14 16': 15,
        '24 22': 23,
        '11 10 ': 10,
        '12 13 10???': 12,
        '20 18 21???': 20,
        '25 29 19???': np.nan
    }
    df['women_total'].replace(to_replace=to_replace_dct, inplace=True)
    ## replace non-numerical values for 'women_perc' attribute
    #non_numerical_values = [print(item) for i,item in enumerate(temp) if type(item)== str] #print non-numerical values
    for i in range(len(df['women_perc'])):
        if type(df['women_perc'].iloc[i]) == str and df['women_perc'].iloc[i][-1] == '%':
            df['women_perc'].iloc[i] = float( df['women_perc'].iloc[i][:-1])*0.01
    df['women_perc'].replace(to_replace=to_replace_dct, inplace=True)
    ## transform type to float
    df['women_total'] = df['women_total'].astype(np.float16)
    df['women_perc'] = df['women_perc'].astype(np.float16)

    # Normalise categorical values for attributes: 'chamber_type','country', 'chamber_type', 'country', 'month'
    df['chamber_type'] = df['chamber_type'].apply(lambda x: x.strip(' ') )
    df['country'] = df['country'].apply(lambda x: x.strip(' ') )
    to_replace_dct = {
        'Lower': 'lower',
        'Upper': 'upper',
        'Single': 'single',
        'Single???': 'single',
        'Not available': np.nan,
        'Single Lower?': 'lower',
        'Special': 'temporary_assembly',
        'Temporary Assembly': 'temporary_assembly',
        'Constituent Assembly': 'single', # from notes; Uganda Unicameral Consistußent Assembly
        'Council': 'Single' # from notes; Nepal, Qatar, Saudi Arabia
    }
    df['chamber_type'].replace(to_replace=to_replace_dct, inplace=True)
    df['country'].replace('Iran (Islamic Republic Of)', 'Iran (Islamic Republic of)', inplace=True)
    to_replace_dct = {
        'january': 'January',
        'january ': 'January',
        'february': 'February',
        'march': 'March',
        'april': 'April',
        'april ': 'April',
        'may': 'May',
        'june': 'June',
        'july': 'July',
        'august': 'August',
        'september': 'September',
        'october': 'October',
        'October ': 'October',
        'november': 'November',
        'december': 'December',
        'May- June': 'June',
        'May- September':'September',
        'april- april': 'April',
        'april-december': 'December',
        'June-- August': 'August',
        'June- august': 'August',
        'June - December': 'December',
        'June-July': 'July',
        'March - February': 'February',
        'March - April': 'April',
        'March - June':'June',
        'Janvier': 'January',
        'July-September':'September', 
        'July-December': 'December',
        'MARCH': 'March',
        'June- November': 'November',
        'Janauary': 'January',
        'March-March': 'March', 
        'March- April': 'April',
        'March- December': 'December',
        'September - October': 'October', 
        'September- october': 'October', 
        'September- November': 'November',
        'March-December': 'December', 
        'September- September': 'September', 
        'September- December': 'December',
        'May- May': 'May', 
        'May-December': 'December', 
        'April -May': 'May', 
        'February- may': 'May',
        'February - october': 'October',
        'July- July': 'July',
        'October - May': 'May',
        'October- November': 'November', 
        'April-October': 'October',
        'January-February': 'February', 
        'January-june': 'June',
        'January-december': 'December', 
        'June- March': 'March',
        'June-June': 'June',
        'June-August': 'August',
        'June-September':'September', 
        'October -october': 'October', 
        'November- november': 'November',
        'November- december': 'December', 
        'April- May': 'May', 
        'April- July': 'July',
        'April- September': 'September', 
        'May- november': 'November', 
        'May - June': 'June', 
        ' March': 'March',
        'August-august': 'August', 
        'August- september': 'September', 
        'November - December': 'December',
        'April - June': 'June', 
        'March - March ': 'March', 
        'March- April ': 'April', 
        'June- July': 'July',
        'June- june': 'June', 
        'October -november': 'November', 
        'October - december': 'December',
        'July - August': 'August', 
        'september- August': 'August', 
        'september- September': 'September',
        'Dec 2014-Jan 2015': 'December', 
        'Jan Feb': 'February', 
        'April - May': 'May',
        'june-June': 'June',
        'June- December': 'December',
        'Febrruary': 'February',
        'june ': 'June',
        'July ': 'July'
        }
    df['month'].replace(to_replace=to_replace_dct, inplace=True)

    # Keep 2 decimal places - women percentage
    df['women_perc'] = round(df['women_perc'], 2)

    # Calculate decade
    df['decade'] = df['year']//10*10

    # Save to csv
    df.to_csv('./data/women_in_parliament-historical_database-1945_to_2018_cleaned.csv',index=False)


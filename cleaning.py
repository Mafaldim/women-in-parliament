import pandas as pd
import numpy as np
import seaborn as sns
import pycountry

import warnings
warnings.filterwarnings("ignore")

if __name__ == "__main__":
        
    # ####################################################
    # Clean/Prepare WOMEN-IN-PARLIAMENT historical data  #
    ######################################################

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
    df['country'].replace('Germany (Democratic Republic)', 'Germany', inplace=True)
    df['country'].replace('Germany (Federal Republic Of)', 'Germany', inplace=True)

    df['country'].replace('Yemen North (Yemen Arab Republic)', 'Yemen', inplace=True)
    df['country'].replace("Yemen South (People's Democratic Republic)", 'Yemen', inplace=True)

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

    # select chambers
    selected_chambers = ['lower','single','single lower','temporary assembly']
    df = df[df['chamber_type'].isin(selected_chambers)]

    # Keep 2 decimal places - women percentage
    df['women_perc'] = round(df['women_perc'], 2)

    # Calculate decade
    df['decade'] = df['year']//10*10

    # Save to csv
    df.to_csv('./data/women_in_parliament-historical_database-1945_to_2018_cleaned.csv',index=False)

    # calculate yearly average of all countries and rolling mean
    avg_yearly = pd.DataFrame(df.groupby(['year'])['women_perc'].mean())
    avg_yearly['women_perc'] = round(avg_yearly['women_perc'], 2)
    avg_yearly['RM5'] = avg_yearly['women_perc'].rolling(window=5).mean()
    avg_yearly['RM5'] = round(avg_yearly['RM5'], 2)
    
    avg_yearly['decade'] = avg_yearly.index//10*10
    avg_yearly['decade'] = avg_yearly['decade']%100

    avg_yearly['year_in_decade'] = avg_yearly.index%10
    
    # save output
    avg_yearly.to_csv('./data/avg_yearly.csv')

    # ####################################################
    # Clean/Prepare POPULATION data                      #
    ######################################################

    # read population data
    df_pop = pd.read_excel('./data/WPP2019_POP_F01_1_TOTAL_POPULATION_BOTH_SEXES.xlsx',usecols=[2,7,17,27,37,47,57,67,75])
    df_pop = df_pop.iloc[15:]
    df_pop.columns = df_pop.iloc[0]
    df_pop = df_pop.iloc[1:]
    # reshape data by decade
    df_pop = df_pop.rename(columns={'Region, subregion, country or area *':'decade'})
    df_pop_ = df_pop.T.reset_index()
    df_pop_.columns = df_pop_.iloc[0]
    df_pop_ = df_pop_.iloc[1:]
    df_pop_ = df_pop_.set_index('decade')
    # save to file
    df_pop_.to_csv('./data/population_by_decade.csv')

    # calculate average percentage participation by decade - country level
    df_avg_dc = pd.DataFrame(df.groupby(['country', 'decade'])['women_perc'].mean().reset_index())
    # save to file
    df_avg_dc.to_csv('./data/women_perc_byDecade_countryLevel.csv', index=False)

    # get the list of countries for which we have an avg decade women representation percentage
    countries = list(df_avg_dc['country'].unique())


    # iterate through countries get their population
    for i in range(len(countries)):
        if i == 0:
            country = countries[i]
            df_pop_c_d = pd.DataFrame(df_pop_[country].reset_index())
            df_pop_c_d = df_pop_c_d.rename(columns={country:'pop'})
            df_pop_c_d['country'] = country
        else:
            country = countries[i]
            try:
                temp = pd.DataFrame(df_pop_[country].reset_index())
                temp = temp.rename(columns={country:'pop'})
                temp['country'] = country
                df_pop_c_d = pd.concat([temp,df_pop_c_d])
            except:
                pass
    df_pop_c_d['decade'] = df_pop_c_d['decade'].astype('int64')

    # merge population to participation by decade, country data
    df_pop_participation = df_avg_dc.merge(df_pop_c_d, on=['country','decade'])
    df_pop_participation.dropna(inplace=True)
    df_pop_participation['pop'] = df_pop_participation['pop'].astype('float')

    df_pop_participation = df_pop_participation.sort_values(by='decade')
    df_pop_participation['women_perc'] = round(df_pop_participation['women_perc'],2)
    df_pop_participation.to_csv('./data/participation_by_decade_country_pop.csv')


    ##################################################################################
    # Participation Ranks 2021 - Regions                                             #
    ##################################################################################

    # read data
    df_historic = pd.read_csv('./data/women_in_parliament-historical_database-1945_to_2018_cleaned.csv')
    df_regions = df_historic[['country','region']]
    df_regions = df_regions.drop_duplicates()

    df_2021 = pd.read_csv('./data/women_percent_as_of2021_cleaned.csv')
    df_2021.rename(columns={'Country':'country'},inplace=True)

    df_regions.set_index(['country'], inplace=True)
    df_2021.set_index(['country'], inplace=True)

    df_2021_regions = df_2021.join(df_regions).reset_index()

    to_replace = dict({'Azerbaijan':'ASIA',
    'Bangladesh':'ASIA',
    'Bahrain':'MENA',
    'Bahamas': 'AME',
    'Bolivia (Plurinational State of)':'AME',
    'Central African Republic':'SUB-SAHARAN',
    'Chad':'SUB-SAHARAN',
    'Chile':'AME',
    'China':'ASIA',
    'Congo':'SUB-SAHARAN',
    "Côte d'Ivoire":'SUB-SAHARAN',
    'Qatar':'MENA',
    'North Macedonia': 'EUR',
    'Venezuela (Bolivarian Republic of)':'AME' })

    for i in range(len(df_2021_regions)):
        country  = df_2021_regions['country'].iloc[i]
        if country in to_replace.keys():
            df_2021_regions['region'].iloc[i] = to_replace[country]

    df_2021_regions.to_csv('./data/women_percent_as_of2021_with_regions.csv')

    ################
    # Fix ISO codes #
    #################

    def get_iso3(country_name):
        try:
            iso3 = pycountry.countries.get(name=country_name).alpha_3
        except:
            iso3 = 'not_found'
        
        return iso3

    # read data of Women's representation in parliament as of 2021
    df21 = pd.read_csv('./data/women_percent_as_of2021.csv',skiprows=5)
    # get country ISO code
    df21['iso3'] = df21['Country'].apply(get_iso3)

    # fix missing country codes
    missing_codes = df21[df21['iso3'].str.contains('not_found')]['Country'].unique()

    bol_index = df21[df21['Country'].str.contains('Bolivia')].index[0]
    df21.iloc[bol_index]['iso3']='BOL'

    mda_index = df21[df21['Country'].str.contains('Moldova')].index[0]
    df21.iloc[mda_index]['iso3']='MDA'

    tza_index = df21[df21['Country'].str.contains('Tanzania')].index[0]
    df21.iloc[tza_index]['iso3']='TZA'

    usa_index = df21[df21['Country'].str.contains('States of America')].index[0]
    df21.iloc[usa_index]['iso3']='USA'

    kor_index = df21[df21['Country'].str.contains('Republic of Korea')].index[0]
    df21.iloc[kor_index]['iso3']='KOR'

    prk_index = df21[df21['Country'].str.contains("Democratic People's Republic of Korea")].index[0]
    df21.iloc[prk_index]['iso3']='PRK'

    cod_index = df21[df21['Country'].str.contains("Democratic Republic of the Congo")].index[0]
    df21.iloc[cod_index]['iso3']='COD'

    bgm_index = df21[df21['Country']=="Gambia (The)"].index[0]
    df21.iloc[bgm_index]['iso3']='GBM'

    irn_index = df21[df21['Country']=="Iran (Islamic Republic of)"].index[0]
    df21.iloc[irn_index]['iso3']='IRN'

    fsm_index = df21[df21['Country']=="Micronesia (Federated States of)"].index[0]
    df21.iloc[fsm_index]['iso3']='FSM'

    ven_index = df21[df21['Country']=="Venezuela (Bolivarian Republic of)"].index[0]
    df21.iloc[ven_index]['iso3']='VEN'

    ch_index = df21[df21['Country']=="Czech Republic"].index[0]
    df21.iloc[ch_index]['iso3']='CZE'

    df21 = df21.loc[:186]
    df21['%W'] = df21['%W'].iloc[:186].astype('float')

    df21['%W_str'] = df21['%W'].apply(lambda x:str(x)+'%')

    df21.to_csv('./data/women_percent_as_of2021_cleaned.csv',index=False)


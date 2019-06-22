# --------------
import pandas as pd
import datetime

# Read the data using pandas module.
ipl_dataset = pd.read_csv(path, delimiter=',')
# Find the list of unique cities where matches were played
unique_cities = pd.unique(ipl_dataset['city'])
print(unique_cities)
# Find the columns which contains null values if any ?
columns_null = ipl_dataset.isnull().sum()[ipl_dataset.isnull().sum()>0].index
print(columns_null)
# List down top 5 most played venues
group_matches = ipl_dataset.pivot_table(index=['match_code','venue'], aggfunc='count')
group_matches = group_matches.index.get_level_values(1).value_counts()
group_matches_5 = group_matches.head(5).index
print(group_matches_5)
# Make a runs count frequency table
group_run = ipl_dataset.groupby('runs')['runs'].count()
print(group_run)
# How many seasons were played and in which year they were played 
ipl_dataset['year'] = ipl_dataset['date'].apply(lambda x:datetime.datetime.strptime(x, "%Y-%m-%d").year)
print(ipl_dataset['year'].nunique())
print(ipl_dataset['year'].unique())
# No. of matches played per season
runs_year = ipl_dataset.pivot_table(index=['match_code', 'year'], values='total', aggfunc='sum')
runs_year.reset_index(level=0, drop=True, inplace=True)
matchcount_year = runs_year.groupby(runs_year.index).count()
print(matchcount_year)
# Total runs across the seasons
runs_year = runs_year.groupby(runs_year.index).sum()
print(runs_year)
# Teams who have scored more than 200+ runs. Show the top 10 results
inning_total = ipl_dataset.groupby(by=['match_code', 'batting_team'])['total'].sum()
inning_total.reset_index(level=0, drop=True, inplace=True)
top_innings = inning_total.sort_values(ascending=False)
high_per = top_innings[top_innings>200]
high_per.head(10)
# What are the chances of chasing 200+ target
inn_run_tol = ipl_dataset.pivot_table(index='match_code', columns='inning', values='total', aggfunc='sum')
inn_run_tol = inn_run_tol[inn_run_tol[1]>200]
inn_run_tol['diff'] = inn_run_tol[1]-inn_run_tol[2]
loss_200 = inn_run_tol[inn_run_tol['diff']<0]
loss_per_200 = loss_200.shape[0]/inn_run_tol.shape[0]*100
print(loss_per_200)
# Which team has the highest win count in their respective seasons ?
top_per_year = ipl_dataset.pivot_table(index=['year', 'match_code', 'winner'], aggfunc='count')
top_per_year['winner'] = top_per_year.index.get_level_values(2)
top_per_year['year'] = top_per_year.index.get_level_values('year')
top_per_year.reset_index(level=[0, 1, 2], drop=True, inplace=True)
top_per_year = top_per_year.groupby(by=['year', 'winner'])[['winner']].count()
for year in ipl_dataset['year'].unique():
    print(year, top_per_year.loc[year].idxmax()['winner'])



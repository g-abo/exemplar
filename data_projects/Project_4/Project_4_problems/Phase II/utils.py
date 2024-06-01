import time
import numpy as np
import pandas as pd
from itertools import product

'''
Utility function for phase I of the final project
'''

def construct_game_pairs(df,
                         verbose = False):
    '''
    For any pair of teams i and j, each game with team i at home and team j away in a season 
    is paired with each game with team i away and team j at home in the same season. 
    This function will create a dataframe with one game pair per row.
    @param df: pandas DataFrame, contains NBA data with season, date, home_team, home_pt, away_team, away_pt columns
    @param verbose: bool, whether to print stats on numbers of pairs and runtimes
    @return: pandas DataFrame, contains pairs of games with columns season, pair_game1_{column}, pair_game2_{column}
    '''
    team_names = df.home_team.unique().tolist()
    team_names.sort()
    
    # columns in dataframe to construct
    pair_games_cols   = ['season', 'pair_game1_date', 'pair_game1_home_team', 'pair_game1_home_pt', 
                         'pair_game1_away_team', 'pair_game1_away_pt',
                         'pair_game2_date', 'pair_game2_home_team', 'pair_game2_home_pt', 
                         'pair_game2_away_team', 'pair_game2_away_pt']
    pair_games_data   = {col: [] for col in pair_games_cols}
    
    # because pandas .loc is slow, use np searchsorted to get start and end indices for each season instead
    season_sorted_df  = df.sort_values(by = ['season'])
    seasons_to_construct = df.season.unique().tolist()
    seasons_to_construct.sort()
    first_season = seasons_to_construct[0]
    season_start_idxs = np.searchsorted(df.season.values, seasons_to_construct)
    # add an end index for the last season
    season_start_idxs = np.concatenate((season_start_idxs, 
                                        np.array([len(df.season)])),
                                       dtype = int)
    
    for season in seasons_to_construct:
        
        season_start_time = time.time()
        season_df  = season_sorted_df.iloc[season_start_idxs[season - first_season]:season_start_idxs[season - first_season + 1]]
        
        # start and end indices for a chunk of games with the same home team and a chunk with the same away team
        home_team_sorted_df  = season_df.sort_values(by = ['home_team'])
        away_team_sorted_df  = season_df.sort_values(by = ['away_team'])
        home_team_start_idxs = np.searchsorted(home_team_sorted_df.home_team.values, team_names)
        away_team_start_idxs = np.searchsorted(away_team_sorted_df.away_team.values, team_names)
        
        # because append is slow when long lists need to be copied to a new location, 
        # collect short lists of column data that can be added to the long list in chunks
        season_pair_games_data = {col: [] for col in pair_games_cols}
        
        for team_a_idx in range(len(team_names) - 1):
            
            # process pairs with team A
            team_a_start_time = time.time()
            team_a_home_df = home_team_sorted_df.iloc[home_team_start_idxs[team_a_idx]:
                                                      home_team_start_idxs[team_a_idx+1]]
            team_a_away_df = away_team_sorted_df.iloc[away_team_start_idxs[team_a_idx]:
                                                      away_team_start_idxs[team_a_idx+1]]
            if len(team_a_home_df) == 0 or len(team_a_away_df) == 0:
                # team A has no pairs
                continue
            
            # start and end indices for a chunk of games with team B as away team in games with team A at home and vice versa
            team_a_home_df.sort_values(by      = ['away_team'],
                                       inplace = True)
            team_a_away_df.sort_values(by      = ['home_team'],
                                       inplace = True)
            team_a_home_away_team_start_idxs = np.searchsorted(team_a_home_df.away_team.values, team_names)
            team_a_away_home_team_start_idxs = np.searchsorted(team_a_away_df.home_team.values, team_names)
            # add end indices for the last team
            team_a_home_away_team_start_idxs = np.concatenate((team_a_home_away_team_start_idxs, 
                                                               np.array([len(team_a_home_df)])),
                                                              dtype = int) 
            team_a_away_home_team_start_idxs = np.concatenate((team_a_away_home_team_start_idxs,
                                                               np.array([len(team_a_away_df)])),
                                                              dtype = int)
            
            # collect data for pairs with team A
            team_a_games_data = {col: [] for col in pair_games_cols}
            for team_b_idx in range(team_a_idx + 1, len(team_names)):
                
                # find games with this pair of teams
                team_a_home_b_away_df = team_a_home_df.iloc[team_a_home_away_team_start_idxs[team_b_idx]:
                                                            team_a_home_away_team_start_idxs[team_b_idx+1]]
                team_a_away_b_home_df = team_a_away_df.iloc[team_a_away_home_team_start_idxs[team_b_idx]:
                                                            team_a_away_home_team_start_idxs[team_b_idx+1]]
                
                for a_home_idx, a_away_idx in product(range(len(team_a_home_b_away_df)), 
                                                      range(len(team_a_away_b_home_df))):
                    
                    # collect data for new data frame
                    team_a_games_data['pair_game1_date'].append(team_a_home_b_away_df['date'].values[a_home_idx])
                    team_a_games_data['pair_game1_home_team'].append(team_names[team_a_idx])
                    team_a_games_data['pair_game1_home_pt'].append(
                        team_a_home_b_away_df['home_pt'].values[a_home_idx])
                    team_a_games_data['pair_game1_away_team'].append(team_names[team_b_idx])
                    team_a_games_data['pair_game1_away_pt'].append(
                        team_a_home_b_away_df['away_pt'].values[a_home_idx])
                    team_a_games_data['pair_game2_date'].append(team_a_away_b_home_df['date'].values[a_away_idx])
                    team_a_games_data['pair_game2_home_team'].append(team_names[team_b_idx])
                    team_a_games_data['pair_game2_home_pt'].append(
                        team_a_away_b_home_df['home_pt'].values[a_away_idx])
                    team_a_games_data['pair_game2_away_team'].append(team_names[team_a_idx])
                    team_a_games_data['pair_game2_away_pt'].append(
                        team_a_away_b_home_df['away_pt'].values[a_away_idx])
                    
            # add data for team A to lists for season
            for col in pair_games_cols:
                season_pair_games_data[col] += team_a_games_data[col]
                
            if verbose:
                print('Season ' + str(season) + ' has ' + str(len(season_pair_games_data['pair_game1_date']))
                      + ' pairs of games with team ' + team_names[team_a_idx])
                print('Time to compute pairs for season ' + str(season) + ' team ' + team_names[team_a_idx]
                      + ': ' + str(time.time() - team_a_start_time) + ' seconds')
                
        # add data for season to columns for final dataframe
        season_pair_games_data['season'] = [season for i in range(len(season_pair_games_data['pair_game1_date']))]
        for col in pair_games_cols:
            pair_games_data[col] += season_pair_games_data[col]
            
        if verbose:
            print('Season ' + str(season) + ' has ' + str(len(season_pair_games_data['season'])) + ' pairs of games')
            print('Time to compute pairs for season ' + str(season) + ': ' 
                  + str(time.time() - season_start_time) + ' seconds')
    
    # construct dataframe of game pairs
    pair_games_df = pd.DataFrame(data    = pair_games_data,
                                 columns = pair_games_cols)
    return pair_games_df
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import scatter_matrix

def introduce_power_terms(dataframe, 
                          columns, 
                          power = 2):
    '''
    Introduce columns that are a power of the original column in dataframe
    @param dataframe: pandas DataFrame
    @param columns: list of str, names of columns to add power terms for
    @param power: int, power to compute, e.g. 2 for squared
    @return: pandas DataFrame with original and column^power columns
    '''
    for colname in dataframe.columns.values:
        if colname in columns:
            dataframe[colname+ "^%s" %power] = dataframe[colname]**power
    return dataframe

def correlation_plot(dataframe):
    '''
    Plot the correlation between each pair of features in a heatmap
    @param dataframe: pandas DataFrame
    @return: None
    '''
    corr_matrix = dataframe.corr()
    f = plt.figure(figsize=(10,10))
    plt.matshow(corr_matrix, vmin=-1, vmax=1, cmap='RdBu_r', fignum=f.number)
    plt.title('Correlation Plot')
    plt.colorbar()
    plt.xticks(range(len(corr_matrix.columns)), corr_matrix.columns, rotation = 45)
    plt.yticks(range(len(corr_matrix.columns)), corr_matrix.columns)
    plt.show()

def scatter_plot_dataframe(dataframe):
    '''
    Create a grid of plots
    Diagonal contains histogram showing distribution of individual feature
    Off-diagonal contains scatter plots of row feature against column feature
    @param dataframe: pandas DataFrame
    @return: None
    '''
    colors = ['red', 'green']
    scatter_matrix(dataframe, figsize=[20,20],marker='x', c='red')
    plt.suptitle('Scatter Plot for the DataFrame')
    plt.tight_layout(rect=[0, 0.03, 1, 0.98])
    plt.show()
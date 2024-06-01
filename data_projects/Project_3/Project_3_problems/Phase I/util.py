import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

def load_processes():
    # read MClist of each process and each year
    mc_higgs = pd.read_csv('data/MC/higgs2012.csv',index_col=None, header=0)
    ## ZZ*
    mc_zz4mu = pd.read_csv('data/MC/zzto4mu2012.csv',index_col=None, header=0)
    mc_zz2mu2e = pd.read_csv('data/MC/zzto2mu2e2012.csv',index_col=None, header=0)
    mc_zz4e = pd.read_csv('data/MC/zzto4e2012.csv',index_col=None, header=0)
    ## Drell-Yan
    mc_dy10 = pd.read_csv('data/MC/dy1050_2012.csv',index_col=None, header=0)
    mc_dy50 = pd.read_csv('data/MC/dy50_2012.csv',index_col=None, header=0)
    ## ttbar
    mc_ttbar = pd.read_csv('data/MC/ttbar2012.csv',index_col=None, header=0)

    processes = [mc_higgs, mc_zz4mu, mc_zz2mu2e, mc_zz4e, mc_dy10, mc_dy50, mc_ttbar]
        
    # Add signal (signal vs. background)   
    for i in range(len(processes)):
        if i==0:
            processes[i] = processes[i].assign(signal=np.ones(processes[i].shape[0]))
        else:
            processes[i] = processes[i].assign(signal=np.zeros(processes[i].shape[0]))
        
    return processes

def load_expr_data():
    return pd.read_csv('data/data/clean_data_2012.csv', index_col=None, header=0)
"""
Return OH_encoder for categorial variables based on entire training data.

Input:
    processes_mc : entire mc training data
    object_cols  : categorial variables
Output:
    OH_encoder based on training data.
"""

def encoder(processes_mc, object_cols):
    reference_data = pd.concat(processes_mc, axis=0)
    
    OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    OH_encoder.fit(reference_data[object_cols])
    return OH_encoder


"""
Remove irrevelant predictors and One-Hot encode categorial variables.

OH_encoder      : one-Hot encoder to transform categorial variables.
object_cols     : categorial predictors
irrelevant_cols : irrelevant predictors to drop
processes_mc    : MC data to be transformed
expr_data       : real experimental data to transform

Output:
    expr_data, processes_mc after being modified 
"""

def trim(OH_encoder, object_cols, irrelevant_cols, processes_mc, expr_data):
    expr_data = expr_data.drop(irrelevant_cols, axis=1)
    
    OH_cols_data = pd.DataFrame(OH_encoder.transform(expr_data[object_cols]))
    
    # One-hot encoding removed index; put it back
    OH_cols_data.index = expr_data.index
    
    # Remove categorical columns (will replace with one-hot encoding)
    num_data = expr_data.drop(object_cols, axis=1)
    
    # Add one-hot encoded columns to numerical features
    expr_data = pd.concat([num_data, OH_cols_data], axis=1)
    
    for i in range(len(processes_mc)):
        processes_mc[i] = processes_mc[i].drop(irrelevant_cols, axis=1)

        OH_cols_mc = pd.DataFrame(OH_encoder.transform(processes_mc[i][object_cols]))
        
        # One-hot encoding removed index; put it back
        OH_cols_mc.index  = processes_mc[i].index
        
        # Remove categorical columns (will replace with one-hot encoding)
        num_mc = processes_mc[i].drop(object_cols, axis=1)

        # Add one-hot encoded columns to numerical features
        processes_mc[i] = pd.concat([num_mc, OH_cols_mc], axis=1)
    
    return expr_data, processes_mc


"""
Compute the weights needed for training/sampling. These weights account for the discrepency between 
the expected relative frequency of background processes and the relative sizes of mc background processes
we have at our disposal.
"""
def compute_weights():
    ## Luminosity of each year
    lumi = 11580.

    ## cross section of each process
    xsecZZ4 = 0.107
    xsecZZ2mu2e = 0.249

    xsecTTBar = 200.

    xsecDY50 = 2955.
    xsecDY10 = 10.742

    scalexsecHZZ = 0.0065

    ## Number of MC Events generated for each process
    nevtZZ4mu = 1499064
    nevtZZ4e = 1499093
    nevtZZ2mu2e = 1497445
    nevtHZZ = 299973 
    nevtTTBar = 6423106
    nevtDY50 = 29426492
    nevtDY10 = 6462290
    
    # Compute training weights
    weights = lumi*np.array([scalexsecHZZ/nevtHZZ, xsecZZ4/nevtZZ4mu, xsecZZ2mu2e/nevtZZ2mu2e, xsecZZ4/nevtZZ4e,\
                                xsecDY10/nevtDY10, xsecDY50/nevtDY50, xsecTTBar/nevtTTBar])

    weights[0] = sum(weights[1:])

    return weights

"""
Produce a mixture sample from background processes.

Input:

processes   : background processes to sample from
frequencies : relative frequency at which to sample each background process
sample_size : size of sample to be returned

Output:
    requested sample
"""
def sample(processes, frequencies, sample_size):
    process_choice = pd.Series(np.random.choice(a=np.arange(len(frequencies)), size=sample_size, p=frequencies))
    sample_sizes = process_choice.value_counts().reindex(np.arange(len(frequencies)), fill_value=0).sort_index()

    sample = pd.DataFrame()
    for i in range(len(processes)):
        try:
            mixing_sample = processes[i].sample(sample_sizes[i], replace=True)
        except:
            mixing_sample = pd.DataFrame()
            
        sample = pd.concat([sample, mixing_sample], axis=0)

    return sample



def split(processes):
    train_processes = []
    sim_processes = []
    synth_processes = []

    for i in range(len(processes)):
        train_process, sim_process = train_test_split(processes[i], test_size=.2, random_state=0)
        try:
            train_process, synth_process = train_test_split(train_process, test_size=.1, random_state=0)
        except:
            synth_process = pd.DataFrame()

        train_processes.append(train_process)
        sim_processes.append(sim_process)
        synth_processes.append(synth_process)

    return train_processes, sim_processes, synth_processes
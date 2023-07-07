# new try of the final
import os
#os.listdir('S1_File/O-latipes-SWS2-A-Angles')
import os
import numpy as np
import pandas as pd
import statsmodels.api as sm
import scipy.stats
from sklearn.model_selection import LeaveOneOut,KFold
from glob import glob
import matplotlib.pyplot as plt
cv = LeaveOneOut()
import sklearn.metrics as skm
import gzip
# multi coleianrity check using vif
from statsmodels.stats.outliers_influence import variance_inflation_factor

def combos(feats,num=2):
    """Function to find all possable combonation of 2 or more points
    inputs:
    feats == list of features
    num (optinal with a defult of 2) == nubmer of varable to combine
    output:
    list for features from itertools combonaion
    """
    from itertools import combinations # documentation https://docs.python.org/3/library/itertools.html
    return [x for x in combinations(feats,num)]

# find combonation in the list that
def good_combos(coms ,data,cutoff=0.4):
    """This function find the combonation of features that have a variance greater than a cutoff the removes
    Those poitns from over all list
    input:
    coms == list of combonations
    data_cutoff(optinal but defults to 0.4) == is the threshold of the pearson correaltion has to surpass to
    be removed
    output:
    list of viable combonations
    """
    # find the corr matrix
    corr = data.corr()
    out = []
    for c in coms:
        # turn each to a lsit
        c = list(c)
        # find the matrix with those values only and take the abs of all values
        com_matrix = abs(corr.loc[c,c])
        # fill the dinainal with 0 to fliter out the 1
        np.fill_diagonal(com_matrix.values,np.zeros(len(c)))
        # the max now will be the no diganal correation
        if np.max(com_matrix.values) < cutoff:
            out.append(c)
    return out

def setup():
    """Function to setup the varibles that i use most often
    state == list of intermeadtes
    l == list of lmax values
    feats == features in conderation for regression """
    # no split at all
    # builbing no histogram set all data
    # name of the interdates used in the files
    states= ['bR' , 'K','L','M','N','O']
    # array for lmax values
    l = [570,590,550,412,560,640]
    # list of features that (define here to keep conistant)
    feats = [i.split('/')[-1].split('_')[-1].split('.')[0] for i in glob('clean/O-1*')]
    return states, l ,feats

# main code for the LeaveOneOut cross vaildation
def leave_one_out(df,var,st={},Y=False):
    cv = LeaveOneOut()
    cv.get_n_splits(df)
    if not Y: # when true we will not make a new dataframe
        st['Feat'] = []
        st['model'] = []
        st['BIC'] = []
        st['r2'] = []
        st['r2_adjusted'] = []
        st["CV_MSE"] = []
        st['CV_RMSE'] = []
        st['CV_MAE'] = []
        #st['CV_r2'] = []
        st['CV_BIC'] = []
        st['CV_maxerror'] = []
    for v in var:
        if type(v) == str:
            v = [v]
        # get the y
        y = df['lmax']
        x = df[[i for i in v]]
        # now we make the model and save it to the data frame
        x = sm.add_constant(x)
        model = sm.OLS(y,x).fit()
        st['Feat'].append(model.params.index.values[1:])
        st['model'].append(model)
        st['BIC'].append(model.bic)
        st['r2'].append(model.rsquared)
        st['r2_adjusted'].append(model.rsquared_adj)

        # doing the f fold crosss jsut the bic
        BIC = []
        mse = []
        mae = []
        r2 =  []
        maxs= []
        for train ,test in cv.split(df):
            xtrain = df[[i for i in v]].iloc[train,:]
            xtrain = sm.add_constant(xtrain)
            xtest = df[[i for i in v]].iloc[test]
            #xtest =  sm.add_constant(xtest)
            ytrain = df['lmax'].iloc[train]
            ytest = df['lmax'].iloc[test]
            m = sm.OLS(ytrain,xtrain).fit()
            b0 = m.params[0]
            Yhat = 0
            for bi ,xi in zip(m.params[1:],v):
                Yhat += bi *xtest[xi]
            Yhat += b0
            mse.append(skm.mean_squared_error(ytest,Yhat))
            mae.append(skm.median_absolute_error(ytest,Yhat))
            maxs.append(skm.max_error(ytest,Yhat))
            #r2.append(skm.r2_score(ytest,Yhat))
            BIC.append(m.bic)
        st["CV_MSE"].append(np.mean(mse))
        st['CV_RMSE'].append(np.mean(mse)**.5)
        st['CV_MAE'].append(np.mean(mae))
        #st['CV_r2'].append(np.mean(r2))
        st['CV_BIC'].append(np.mean(BIC))
        st['CV_maxerror'].append(np.mean(maxs))
    return st

# main code for using kfold cross vaildation
def kfold_method(df,var,st={},Y=False,seed=420,nfolds=10,invert_fold=False,shuffle=True):
    items = df.shape[0]
    kf = KFold(n_splits=nfolds,shuffle=shuffle,random_state=seed)
    if not Y: # when true we will not make a new dataframe
        st['Feat'] = []
        st['model'] = []
        st['BIC'] = []
        st['r2'] = []
        st['r2_adjusted'] = []
        st["CV_MSE"] = []
        st['CV_RMSE'] = []
        st['CV_MAE'] = []
        #st['CV_r2'] = []
        st['CV_BIC'] = []
        st['CV_maxerror'] = []
    for v in var:
        if type(v) == str:
            v = [v]
        # get the y
        y = df['lmax']
        x = df[[i for i in v]]
        # now we make the model and save it to the data frame
        x = sm.add_constant(x)
        model = sm.OLS(y,x).fit()
        st['Feat'].append(model.params.index.values[1:])
        st['model'].append(model)
        st['BIC'].append(model.bic)
        st['r2'].append(model.rsquared)
        st['r2_adjusted'].append(model.rsquared_adj)

        # doing the f fold crosss jsut the bic
        BIC = []
        mse = []
        mae = []
        r2 =  []
        maxs= []
        for train ,test in kf.split(df):
            if invert_fold:
                test ,train = train ,test
            xtrain = df[[i for i in v]].iloc[train,:]
            xtrain = sm.add_constant(xtrain)
            xtest = df[[i for i in v]].iloc[test]
            #xtest =  sm.add_constant(xtest)
            ytrain = df['lmax'].iloc[train]
            ytest = df['lmax'].iloc[test]
            m = sm.OLS(ytrain,xtrain).fit()
            b0 = m.params[0]
            Yhat = 0
            for bi ,xi in zip(m.params[1:],v):
                Yhat += bi *xtest[xi]
            Yhat += b0
            mse.append(skm.mean_squared_error(ytest,Yhat))
            mae.append(skm.median_absolute_error(ytest,Yhat))
            maxs.append(skm.max_error(ytest,Yhat))
            #r2.append(skm.r2_score(ytest,Yhat))
            BIC.append(m.bic)
        st["CV_MSE"].append(np.mean(mse))
        st['CV_RMSE'].append(np.mean(mse)**.5)
        st['CV_MAE'].append(np.mean(mae))
        #st['CV_r2'].append(np.mean(r2))
        st['CV_BIC'].append(np.mean(BIC))
        st['CV_maxerror'].append(np.mean(maxs))
    return st

# new funciton to read in all the filesn

def collect_data(states,l,feats,out_name,C_dir='clean',skip=10000,stride=13):
    """ we have a bit of a problem in that we have such a large number of files"""
    # check for lmax in the list of features
    mes = [i for i in feats if i != 'lmax']
    test_met = mes[6]

    #csv_out = pd.DataFrame(columns=tf)
    #csv_out.to_csv(out_name +'.csv.gz',index=False, compression='gzip')
    num = len(glob(f"{C_dir}/"+states[0] + "-" + '*' + "_dihe_"+ test_met + "*"))
    # we are going to make one data frame for each state-ru
    for state, lmax  in zip(states,l): # loop through each diff protein
        for prod in range(1,num+1):

            # make a blank data frame for this
            df = pd.DataFrame()
            for feat in mes:
                # find the file
                if stride <= 0:
                    stride=0
                file = glob(f"{C_dir}/{state}-{prod}_*_{feat}.dat")[0]
                data = pd.read_csv(file,delimiter=' ',dtype=float,header=None,skiprows=skip).loc[::stride,1]
                df[feat] = data

            df['lmax'] = [float(lmax) for _ in data]
            if state == states[0] and prod == 1:
                print('start')
                df.to_csv(out_name +'.csv',index=False)
            else:
                df.to_csv(out_name +'.csv',mode = 'a',header=False,index=False)
            print('wrote',state,prod)


# functions for assumpotions checks

def VIF_given_results(results,df):
    "find the VIF for a given set of varibvales "
    models = results['Feat']
    for model in models:
        if len(model) != 1:

            vif_data = pd.DataFrame() # empty data frame
            vif_data['features'] = model
            print(model)
            test = df[model]
            vif_data["VIF"] = [variance_inflation_factor(test.values,i) for i in range(len(test.columns))]
            print(vif_data)

# ass 3 independace The Durbin-Watson Test

def Durbin_Watson(results,df):
    """test indepedncace """
    # step one find the resduals Yexp - Yhat
    models = results['Feat']
    #line_eqs = results['Parameters']
    for model in models:

        x = df[model]
        y = df['lmax']
        x = sm.add_constant(x)
        reg_mod = sm.OLS(y,x).fit()
        yhat = reg_mod.predict(x)
        #residual = pd.DataFrame.to_numpy(y - yhat)

        # now run durbin_watson
        print(model)
        print(durbin_watson(reg_mod.resid))
        print('durbin watson scorce is between 2.5 and 1.5?', 1.5 <= durbin_watson(reg_mod.resid) <= 2.5 )
        print('\n')

# assump 4  Homoscedasticity (plot stanardzie resdulas vs yhat) must look random
def Homoscedasticity(results,df):
    """test indepedncace """
    # step one find the resduals Yexp - Yhat
    models = results['Feat']
    #line_eqs = results['Parameters']
    for model in models:
        x = df[model]
        y = df['lmax']
        x = sm.add_constant(x)
        reg_mod = sm.OLS(y,x).fit()
        yhat = reg_mod.predict(x)
        #residual = pd.DataFrame.to_numpy(y - yhat)
        # now wertfdfdstandarize them
        influence = reg_mod.get_influence()
        #obtain standardized residuals
        standardized_residuals = influence.resid_studentized_internal
        _, pval, __, f_pval =sm.stats.diagnostic.het_breuschpagan(reg_mod.resid,df[model])
        print(model,' p value of homosdacity', pval,'less than 0.05 <=?',pval <= 0.05)
        plt.scatter(yhat, standardized_residuals,color='black')
        plt.xlabel('predicited vaules')
        plt.ylabel('Standardized Residuals')
        plt.axhline(y=0, color='black', linestyle='--', linewidth=1)
        plt.show()
        print('\n')

# assumpt 5 normality
def check_normalizity_qqplots(results,df):
    """graph that need to be mostly linear for the standarized """
    # step one find the resduals Yexp - Yhat
    models = results['Feat']
    #line_eqs = results['Parameters']
    for model in models:
        x = df[model]
        y = df['lmax']
        s = [5 for _ in y ]
        x = sm.add_constant(x)
        fig, ax = plt.subplots(figsize=(6,2.5))
        reg_mod = sm.OLS(y,x).fit()
        yhat = reg_mod.predict(x)
        residual = pd.DataFrame(y - yhat).to_numpy()
        # now wertfdfdstandarize them
        influence = reg_mod.get_influence()
        #obtain standardized residuals
        standardized_residuals = influence.resid_studentized_internal
        fig = sm.qqplot(standardized_residuals, line='45')
        _, (__, ___, r) = scipy.stats.probplot(standardized_residuals, plot=ax, fit=True)
        print(r**2,model)
        plt.show()
        print('\n')

def vaildation_check(results,df,val_df):
    """given each model we will find the preedicted vaules and the error of that measure"""
    # find the model pars
    models = results['Feat']
    for model in models: # loop into the models
        new_tabel = pd.DataFrame()
        print(model)
        # re create the model
        x = df[model]
        y = df['lmax']
        x = sm.add_constant(x)
        reg_mod = sm.OLS(y,x).fit()

        # with the model made we need to make the test model
        # these must be the same size to work
        x_new = val_df[model]
        x_new = sm.add_constant(x_new)
        new_tabel['Y'] = val_df['lmax']
        # precit the vaules
        yhat = reg_mod.predict(x_new)
        mse_val = skm.mean_squared_error(new_tabel['Y'],yhat)
        #new_tabel['Yhat'] = yhat
        #new_tabel['E'] = new_tabel['Y'] - new_tabel['Yhat']
        #new_tabel['E^2'] = new_tabel['E']**2

        #print(new_tabel)
        print('MSE=',mse_val,'RMSE=',mse_val**0.5 )
        print('\n')
        #new_tabel['error'] = new_tabel['Y'] - new_tabel['Yhat']
if __name__ == '__main__':
    pass

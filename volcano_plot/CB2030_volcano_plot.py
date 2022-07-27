import pandas as pd
import numpy as np
import scipy as sp
import seaborn as sns
import matplotlib.pyplot as plt
from ipywidgets import interact, interact_manual
from ipywidgets import IntSlider, FloatSlider, Dropdown, Text


clinical_data = pd.read_csv('/home/sofia/Documents/GitHub/MTLS_code/CB2030_Systems_Bio/Lab1/System_bio_Toolkit/data/brca_clin.tsv.gz', sep ='\t', index_col=2)
clinical_data = clinical_data.iloc[4:,1:]
expression_data = pd.read_csv('/home/sofia/Documents/GitHub/MTLS_code/CB2030_Systems_Bio/Lab1/System_bio_Toolkit/data/brca.tsv.gz', sep ='\t', index_col=1)
expression_data = expression_data.iloc[:,2:].T

clinical_data.head()
expression_data.head()

# Volcano Plot 

def multiple_gene_ttest(clinical_df, expression_df, separator, cond1, cond2):
    p_vec = []
    log_fc_vec = []
    log10_p = []
    try:
        group1 = clinical_df[separator] == cond1
        index1 = clinical_df[group1].index # The index (row labels) of the DataFrame
        group2 = clinical_df[separator] == cond2
        index2 = clinical_df[group2].index
    except:
        print('Clinical condition wrong')
    for gene in expression_df.columns: # The column labels of the DataFrame  # iterating over columns
        try:
            expression = expression_df[gene]
        except:
            print('Gene not found in data')
        expression1 = expression[index1].dropna() # expression[index] is the subseting samples and droping NAs
        expression2 = expression[index2].dropna()
        
        if (expression1 <= 0).any() or (expression2 <= 0).any(): # removing zeros because that will mess up the log2 transformation
            continue 
            
        p_val = sp.stats.ttest_ind(expression1, expression2).pvalue # calculating the p values
        p_vec.append(p_val)
        
        expression1_log2 = np.log2(expression1) # log2 tranforming expression data
        expression2_log2 = np.log2(expression2)
                
        log_fc = np.mean(expression1_log2) - np.mean(expression2_log2) # calculating log fold change
        log_fc_vec.append(log_fc)
        
    for p in p_vec: 
        log10_p.append(-np.log10(p)) # -log10 tranforming p-values
                
    return pd.DataFrame(list(zip(p_vec, log10_p, log_fc_vec)), columns =['p', '-log10_p' ,'log_fc']) #packaging respective lists into a pd dataframe


# performing statistics on 'Cancer Type Detailed' clinical condition to compare gene expression between 'Breast Invasive Ductal Carcinoma' and 'Breast Invasive Lobular Carcinoma'
volcano_data = multiple_gene_ttest(clinical_data, expression_data, 'Cancer Type Detailed', 'Breast Invasive Ductal Carcinoma', 'Breast Invasive Lobular Carcinoma')


# Plotting the data as a volcano plt
sns.set_style("white")
sns.set_context("talk")
ax = sns.relplot(data=volcano_data, x="log_fc",y="-log10_p",aspect=1.5,height=6)
ax.set(xlabel="$log_{2}Fold Change$", ylabel="$-log_{10}(p)$");

plt.savefig('/volcano_plot.png')
plt.show()

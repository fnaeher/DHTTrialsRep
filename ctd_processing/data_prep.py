# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 18:11:47 2024

@author: AnatolFiete.Naeher
"""

import pandas as pd
import numpy as np
import re
    

def c_title(title, age, gender, race, enrollment):
    if isinstance(title, str):
        title_lower = title.lower()  
        if title_lower in (keyword.lower() for keyword in age):
            return 'age'
        elif title_lower in (keyword.lower() for keyword in race):
            return 'race'
        elif title_lower in (keyword.lower() for keyword in gender):
            return 'gender'
        elif title_lower in (keyword.lower() for keyword in enrollment):
            return 'enrollment'
    return 'unknown'


def clean_ICD(s):
    return re.sub(r'\..*', '', s)


def data_prep1(d_CTD): 
    max_count = d_CTD['CTD_2'].groupby('nct_id')['count'].transform('max')
    d_CTD['CTD_2'] = d_CTD['CTD_2'][d_CTD['CTD_2']['count'] == max_count] \
        .reset_index(drop = True)
    d_CTD['CTD_2'] = d_CTD['CTD_2'][d_CTD['CTD_2']['param_value_num'] >= 0]
    return d_CTD['CTD_2']
    
    
def data_prep2(d_CTD, age, gender, race, enrollment):    
    d_CTD['CTD_2'].loc[:,'cat_title'] = d_CTD['CTD_2']['title'] \
        .apply(c_title, args = (age, gender, race, enrollment))
    d_CTD['CTD_2'] = d_CTD['CTD_2'][d_CTD['CTD_2']['cat_title'] != 'unknown']
    d_CTD['CTD_2'].loc[:,'nan_status'] = np.select(
        [
            pd.isna(d_CTD['CTD_2']['category']) & pd.isna(d_CTD['CTD_2']
                ['classification']),  
            pd.isna(d_CTD['CTD_2']['category']),                                  
            pd.isna(d_CTD['CTD_2']['classification'])                             
        ],
        [3, 1, 2],  
        default = 4  
    )
    
    print(d_CTD['CTD_2'].groupby('nan_status')['nct_id'].nunique()
          .reset_index(name='count'))
    
    d_CTD['CTD_2'].loc[:, 'cat_exp'] = np.where(
        (np.isin(d_CTD['CTD_2']['cat_title'], ['gender', 'race', 'age']) & 
          (d_CTD['CTD_2']['nan_status'] == 1)), d_CTD['CTD_2']
            ['classification'],
            np.where(
                (np.isin(d_CTD['CTD_2']['cat_title'], ['gender', 'race',
                  'age']) & 
                 np.isin(d_CTD['CTD_2']['nan_status'], [2, 4])),
            d_CTD['CTD_2']['category'],
        np.nan
        )
    )
    
    sample = np.random.choice(d_CTD['CTD_2']['nct_id'], size = 15, replace = False)
    d_CTD['CTD_2'] = d_CTD['CTD_2'][d_CTD['CTD_2']['nct_id'].isin(sample)]
    return d_CTD['CTD_2']


def merge(d_CTD):
    d_CTD['CTD_1']['start_date'] = pd.to_datetime(d_CTD['CTD_1']['start_date'], 
        errors='coerce').dt.strftime('%m-%d-%Y')
    d_CTD['CTD_1']['start_year'] = pd.to_datetime(d_CTD['CTD_1']['start_date'], 
        errors='coerce').dt.strftime('%Y')
    d_CTD['CTD_1']['completion_date'] = pd.to_datetime(d_CTD['CTD_1']
        ['completion_date'], errors ='coerce').dt.strftime('%m-%d-%Y')
    d_CTD['CTD_1']['completion_year'] = pd.to_datetime(d_CTD['CTD_1']
        ['completion_date'], errors ='coerce').dt.strftime('%Y')


    d_CTD['CTD_1_agg'] = d_CTD['CTD_1'].groupby('nct_id').agg(
        Value1_sum = ('enrollment', 'sum'),    
        Value1_list = ('enrollment', list),        
        Value2_list = ('name', list))


    d_CTD['CTD_1'] = d_CTD['CTD_1'].drop(columns = ['enrollment', 'name'], 
        axis = 1)
    d_CTD['CTD_1'] = d_CTD['CTD_1'].drop_duplicates()
    d_CTD['CTD_1'] = pd.merge(d_CTD['CTD_1_agg'], d_CTD['CTD_1'], on = 'nct_id', 
        how = 'left')


    d_CTD['CTD_1'].columns = ['NCT_id', 'Enrollment', 'list_Enrollment',
        'study_Country','study_Type', 'FDAreg_Drug', 'FDAreg_Device', 
        'unapp_Device', 'Status', 'st_Date', 'comp_Date', 'Phase', 'no_Arms', 
        'Sampling', 'e_Gender', 'e_min_Age', 'e_max_Age','st_Year', 'comp_Year'
        ]
     
    
    d_CTD['CTD_1']['study_Country'] = d_CTD['CTD_1']['study_Country'].apply(
        lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x if 
        pd.notna(x) else ''
        )
    
    
    d_CTD['DD']['Year'] = d_CTD['DD']['Year'].astype(str)
    d_CTD['DD']['study_Country'] = 'United States'


    d_CTD['DD'].columns = ['Unnamed: 0', 'st_Year', 'st_Male', 'st_Female', 
        'st_<18 Years', 'st_18:65 Years', 'st_>65 years', 'st_White', 
        'st_Hispanic','st_Black', 'st_am_Indian', 'st_Asian', 'st_Hawaiian', 
        'st_mixed','study_Country']
    d_CTD['CTD_1'] = pd.merge(d_CTD['CTD_1'], d_CTD['DD'], on = ['st_Year', 
        'study_Country'], how = 'left')


    d_CTD['DD'].columns = ['Unnamed: 0', 'comp_Year', 'comp_Male','comp_Female', 
        'comp_<18 Years', 'comp_18:65 Years', 'comp_>65 years','comp_White', 
        'comp_Hispanic', 'comp_Black','comp_am_Indian', 'comp_Asian', 
        'comp_Hawaiian', 'comp_mixed','study_Country']
    d_CTD['CTD_1'].rename(columns = {'completion_date': 'comp_Year'}, 
        inplace = True)
    d_CTD['CTD_1'] = pd.merge(d_CTD['CTD_1'], d_CTD['DD'], on = ['comp_Year', 
        'study_Country'], how = 'left')
    d_CTD['CTD_1'] = d_CTD['CTD_1'].drop(['Unnamed: 0_x', 'Unnamed: 0_y'], 
        axis = 1)
    d_CTD['CTD_1']['study_Country'] = d_CTD['CTD_1']['study_Country'].apply(
        lambda x: [x] if isinstance(x, str) else x
        )

    d_CTD['CTD_1']['study_Country_ct'] = d_CTD['CTD_1']['study_Country']\
        .apply(len)     


    d_CTD['DHTx'].columns = ['NCT_id']
    d_CTD['DHTx'].loc[:,'DHT'] = 1
    d_CTD['CTD_1'] = pd.merge(d_CTD['CTD_1'], d_CTD['DHTx'], on = 'NCT_id', 
        how = 'left')
    d_CTD['CTD_1']['DHT'] = d_CTD['CTD_1']['DHT'].fillna(0)


    d_CTD['CTD_3'].rename(columns = {'nct_id': 'NCT_id'}, inplace = True)
    d_CTD['CTD_3'] = d_CTD['CTD_3'].groupby('NCT_id').agg(   
        Intervention = ('intervention_type', list),        
        int_Name = ('name', list))
    d_CTD['CTD_1'] = pd.merge(d_CTD['CTD_1'], d_CTD['CTD_3'], on = 'NCT_id', 
        how = 'left')


    d_CTD['CTD_4'].rename(columns = {'nct_id': 'NCT_id'}, inplace = True)
    d_CTD['CTD_4'] = d_CTD['CTD_4'].groupby('NCT_id').agg(   
        sp_Class = ('agency_class', list),        
        sp_Role = ('lead_or_collaborator', list))
    d_CTD['CTD_1'] = pd.merge(d_CTD['CTD_1'], d_CTD['CTD_4'], on = 'NCT_id', 
        how = 'left')
    
    
    d_CTD['Map_1'] = d_CTD['Map_1'][['ICD10CM_ID', 'MESH_ID']]
    d_CTD['Map_1']['ICD10CM_ID'] = d_CTD['Map_1']['ICD10CM_ID']\
        .apply(clean_ICD)
    d_CTD['Map_1'] = d_CTD['Map_1'].drop_duplicates()


    d_CTD['Map_2'] = d_CTD['Map_2'][['ICD10CM_ID', 'MESH_ID']]
    d_CTD['Map_2']['ICD10CM_ID'] = d_CTD['Map_2']['ICD10CM_ID']\
        .apply(clean_ICD)
    d_CTD['Map_2'] = d_CTD['Map_2'].drop_duplicates()


    d_CTD['Map_3'] = pd.concat([d_CTD['Map_1'], d_CTD['Map_2']])\
         .drop_duplicates().reset_index(drop=True)
    d_CTD['Map_3'].columns = ['ICD10CM_id','MESH_id']    


    d_CTD['MICD']['ICD10CM_ID'] = d_CTD['MICD']['icd_code'].astype(str)
    d_CTD['MICD']['ICD10CM_ID'] = d_CTD['MICD']['ICD10CM_ID']\
        .apply(clean_ICD)
    d_CTD['MICD'] = d_CTD['MICD'][['label', 'ICD10CM_ID','mesh_code']]
    d_CTD['MICD'] = d_CTD['MICD'].drop_duplicates()
    d_CTD['MICD'].columns = ['MESH_term','ICD10CM_id','MESH_id']   
    d_CTD['MICD'] = d_CTD['MICD'].astype(str)


    d_CTD['MMap'] = pd.merge(d_CTD['MICD'], d_CTD['Map_3'] , 
         on = ['MESH_id'], how ='left')
    d_CTD['MMap']['ICD10CM_id_y'] = np.where(d_CTD['MMap']['ICD10CM_id_y'] \
        .isna(), d_CTD['MMap']['ICD10CM_id_x'], d_CTD['MMap']['ICD10CM_id_y'])
    d_CTD['MMap'] = d_CTD['MMap'].rename(columns={'ICD10CM_id_y':'ICD10CM_id'})
    d_CTD['MMap'] = pd.merge(d_CTD['MMap'], d_CTD['Map_3'] , 
         on = ['ICD10CM_id'], how ='left')
    d_CTD['MMap'] = d_CTD['MMap'].drop(columns = ['ICD10CM_id_x','MESH_id_x'])
    d_CTD['MMap']['MESH_term'] = d_CTD['MMap']['MESH_term'].str.lower()
    d_CTD['MMap'] = d_CTD['MMap'].groupby('MESH_term').agg(
        ICD10CM_id = ('ICD10CM_id', lambda x: list(set(x))),    
        MESH_id = ('MESH_id_y', lambda x: list(set(x)))
    ).reset_index()
    
    
    d_CTD['CTD_5'].columns = ['NCT_id','MESH_term']
    d_CTD['CTD_5']['MESH_term'] = d_CTD['CTD_5']['MESH_term'].str.lower()
    
    
    d_CTD['MMap'] = pd.merge(d_CTD['MMap'], d_CTD['CTD_5'], on = 'MESH_term', 
        how = 'left') ###check merge!!!
      
    
    d_CTD['MMap'] = d_CTD['MMap'].groupby('NCT_id').agg(
        MESH_term = ('MESH_term', list),
        ICD10CM_id = ('ICD10CM_id', lambda x: 
                      [item for sublist in x for item in sublist]),  
        MESH_id = ('MESH_id', lambda x: 
                   [item for sublist in x for item in sublist]),  
    ).reset_index()
    d_CTD['MMap']['MESH_term_ct'] = d_CTD['MMap']['MESH_term'].apply(len)    
    d_CTD['MMap']['ICD10CM_ct'] = d_CTD['MMap']['ICD10CM_id'].apply(len)
    d_CTD['MMap']['MESH_id_ct'] = d_CTD['MMap']['MESH_id'].apply(len)
    
    
    d_CTD['CTD_1'] = pd.merge(d_CTD['CTD_1'], d_CTD['MMap'], on = 'NCT_id', 
        how = 'left') ###check merge!!!
    
    
    d_CTD['CTD_2'] = pd.merge(d_CTD['CTD_2'], d_CTD['b_output'], 
        on = ['cat_title','cat_exp'], how = 'left')
    
    d_CTD['CTD_2'].loc[:,'piv_cat'] = np.where(
        d_CTD['CTD_2']['param_type'].isin(['MEAN', 'MEDIAN']), 
        d_CTD['CTD_2']['param_type'],
        
            np.where(d_CTD['CTD_2']['cat_title'] == 'enrollment', 'enrollment', 
                     d_CTD['CTD_2']['piv_cat']) 
            )
    
    d_CTD['CTD_2'].loc[:, 'piv_val'] = np.where(
        (d_CTD['CTD_2']['cat_title'] == 'enrollment') & 
        (np.isin(d_CTD['CTD_2']['classification'], 
                 ['Asia', 'Global', 'Cohort 1', 'Cohort 2', 
                  'Treatment-Naive Population', 'ITT Population'])),
        d_CTD['CTD_2']['category'],  
    
        np.where(
            (d_CTD['CTD_2']['cat_title'] == 'enrollment') & 
            (np.isin(d_CTD['CTD_2']['nan_status'], [1, 4])),
            d_CTD['CTD_2']['classification'],  
    
            np.where(
                (d_CTD['CTD_2']['cat_title'] == 'enrollment') & 
                (d_CTD['CTD_2']['nan_status'] == 2),
                d_CTD['CTD_2']['category'],  
    
                d_CTD['CTD_2']['param_value_num']
            )
        )
    )
    
    
    d_CTD['CTD_2'] = d_CTD['CTD_2'][d_CTD['CTD_2']['piv_cat'].notnull()]
    d_CTD['CTD_2_agg'] = d_CTD['CTD_2'][d_CTD['CTD_2']
        ['cat_title'].isin(['race', 'gender', 'age'])] \
            .groupby(['nct_id', 'piv_cat'], as_index = False)['piv_val'].sum()
    d_CTD['CTD_2'] = d_CTD['CTD_2'].loc[d_CTD['CTD_2']
        ['cat_title'] == 'enrollment', ['nct_id', 'piv_cat', 'piv_val']]
    d_CTD['CTD_2'] = pd.concat([d_CTD['CTD_2_agg'], d_CTD['CTD_2']], 
        ignore_index = True, axis = 0)
    
    d_CTD['CTD_2'] = d_CTD['CTD_2'].pivot_table(index ='nct_id', 
        columns ='piv_cat', values = 'piv_val', aggfunc = list)


    d_CTD['CTD_2'].reset_index(inplace = True)
            
    
    d_CTD['CTD_2'].loc[:, d_CTD['CTD_2'].columns != 'enrollment'] = \
        d_CTD['CTD_2'].loc[:, d_CTD['CTD_2'].columns != 'enrollment'] \
        .apply(lambda col: col.apply(lambda val: val[0] if isinstance(
        val, list) and len(val) == 1 else val))       
      
                                          
    d_CTD['CTD_2'].columns = ['NCT_id','<18 years', '>65 years', 'am_Indian', 
        'Asian', 'Black', 'Hispanic', 'age_Mean', 'age_Median', 'Hawaian', 
           'White', '18:65 years', 'enroll_Country', 'Female', 'Male', 'other',
           'unknown_a', 'unknown_g', 'unknown_r']
    
    
    d_CTD['CTD'] = pd.merge(d_CTD['CTD_1'], d_CTD['CTD_2'], on = 'NCT_id', 
        how = 'left')
    
    
    d_CTD['CTD']['r_Race'] = np.where(d_CTD['CTD'][['am_Indian', 'Asian', 
        'Black', 'Hispanic','Hawaian','White']].notna().any(axis = 1), 1, 0)
    d_CTD['CTD'].loc[:,'r_Gender'] = np.where(d_CTD['CTD'][['Female', 'Male', 
        'other']].notna().any(axis = 1), 1, 0)
    d_CTD['CTD'].loc[:,'r_Age'] = np.where(d_CTD['CTD'][['<18 years', 
        '>65 years', '18:65 years','age_Mean','age_Median']].notna() \
        .any(axis = 1), 1, 0)
    
  
    col = ['Male','Female','<18 years', '18:65 years', '>65 years', 
           'am_Indian', 'Hawaian', 'White', 'Black', 'Hispanic','Asian']
    d_CTD['CTD'][col] = d_CTD['CTD'][col].apply(lambda col: pd.to_numeric(col, 
            errors = 'coerce'))


    d_CTD['CTD']['Enrollment'] = d_CTD['CTD']['Enrollment'].replace(0, np.nan)
    
    
    d_CTD['CTD'].loc[d_CTD['CTD']['Enrollment'].notna(), 'Perc_Male'] = (
            (d_CTD['CTD']['Male'] / d_CTD['CTD']['Enrollment']) * 100)
    d_CTD['CTD'].loc[d_CTD['CTD']['Enrollment'].notna(),'Perc_Female'] = (
            (d_CTD['CTD']['Female'] / d_CTD['CTD']['Enrollment']) * 100)
    d_CTD['CTD'].loc[d_CTD['CTD']['Enrollment'].notna(),'u_Perc_Gender'] = (
            (d_CTD['CTD']['unknown_g'] / d_CTD['CTD']['Enrollment']) * 100)
             
    
    d_CTD['CTD'].loc[d_CTD['CTD']['Enrollment'].notna(),'Perc_<18 years'] = (
            (d_CTD['CTD']['<18 years'] / d_CTD['CTD']['Enrollment']) * 100)
    d_CTD['CTD'].loc[d_CTD['CTD']['Enrollment'].notna(),'Perc_18:65 years'] = (
            (d_CTD['CTD']['18:65 years'] / d_CTD['CTD']['Enrollment']) * 100)
    d_CTD['CTD'].loc[d_CTD['CTD']['Enrollment'].notna(),'Perc_>65 years'] = (
            (d_CTD['CTD']['>65 years'] / d_CTD['CTD']['Enrollment']) * 100)
    d_CTD['CTD'].loc[d_CTD['CTD']['Enrollment'].notna(),'u_Perc_Age'] = (
            (d_CTD['CTD']['unknown_a'] / d_CTD['CTD']['Enrollment']) * 100)
          
    
    d_CTD['CTD'].loc[:,'R_other'] = (d_CTD['CTD']['am_Indian'] + d_CTD['CTD']
            ['Hawaian'])
    d_CTD['CTD'].loc[d_CTD['CTD']['Enrollment'].notna(),'Perc_White'] = (
            (d_CTD['CTD']['White'] / d_CTD['CTD']['Enrollment']) * 100)
    d_CTD['CTD'].loc[d_CTD['CTD']['Enrollment'].notna(),'Perc_Black'] = (
            (d_CTD['CTD']['Black'] / d_CTD['CTD']['Enrollment']) * 100)
    d_CTD['CTD'].loc[d_CTD['CTD']['Enrollment'].notna(),'Perc_Hispanic'] = (
            (d_CTD['CTD']['Hispanic'] / d_CTD['CTD']['Enrollment']) * 100)
    d_CTD['CTD'].loc[d_CTD['CTD']['Enrollment'].notna(),'Perc_Asian'] = (
            (d_CTD['CTD']['Asian'] / d_CTD['CTD']['Enrollment']) * 100)
    d_CTD['CTD'].loc[d_CTD['CTD']['Enrollment'].notna(),'Perc_Other'] = (
            (d_CTD['CTD']['R_other'] / d_CTD['CTD']['Enrollment']) * 100)
    d_CTD['CTD'].loc[d_CTD['CTD']['Enrollment'].notna(),'u_Perc_Race'] = (
            (d_CTD['CTD']['unknown_r'] / d_CTD['CTD']['Enrollment']) * 100)
    
    
    d_CTD['CTD'].loc[:,'>100_perc_r'] = d_CTD['CTD'][['Perc_White', 
            'Perc_Black', 'Perc_Other','Perc_Hispanic', 'Perc_Asian']] \
            .sum(axis = 1) > 100.0
    d_CTD['CTD'].loc[:,'>100_perc_a'] = d_CTD['CTD'][['Perc_<18 years', 
            'Perc_>65 years', 'Perc_18:65 years']].sum(axis=1) > 100.0
    d_CTD['CTD'].loc[:,'>100_perc_g'] = d_CTD['CTD'][['Perc_Female', 
            'Perc_Male']].sum(axis=1) > 100.0
    
    
    d_CTD['CTD'].loc[:,'c_Perc_White'] = np.where((
            d_CTD['CTD']['>100_perc_r'] == True),
                d_CTD['CTD']['Perc_White'] - d_CTD['CTD']['Perc_Hispanic'], 
                    d_CTD['CTD']['Perc_White'] )
    d_CTD['CTD'].loc[:,'c_100_perc_r'] = d_CTD['CTD'][['c_Perc_White', 
            'Perc_Black', 'Perc_Other', 'Perc_Hispanic', 'Perc_Asian']] \
            .sum(axis=1).between(0, 100)
    
    return(d_CTD['CTD'])

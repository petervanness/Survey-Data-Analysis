import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns
from typing import Union


root_folder = "/Raw Data/"
output_path = "/Output/Overall/"

# --------------------------------------------------
if not os.path.exists(output_path):
    os.makedirs(output_path)
    print(f'Output folder created at {output_path}')
# --------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------

# Functions for Analysis

#------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------


def make_fmt_kde (in_df: pd.DataFrame, var:str, var_label:str, label:str, cap_val:bool = True, by_var:str = None, desc_stats:bool = False):
    '''Create, format and save KDE.'''
    if cap_val:
        in_df.loc[:, 'field'] = in_df[var].copy().clip(lower=in_df[var].quantile(.001), upper=in_df[var].quantile(.999))
        sns.kdeplot(in_df['field'], label=label, hue=in_df[by_var])
    else:
        sns.kdeplot(in_df[var], label=label, hue=in_df[by_var])
    if len(label)>90:
        plt.title(label, fontdict={'fontsize':7})
    else:
        plt.title(label, fontdict={'fontsize':10})
    plt.xlabel(var_label)
    plt.ylabel('Density')
    plt.gca().set_xticks(plt.gca().get_xticks())
    plt.gca().set_xticklabels(['{:,.0f}'.format(x) for x in plt.gca().get_xticks()])

    plt.gca().set_yticks(plt.gca().get_yticks())
    plt.gca().set_yticklabels(['{:,.0f}'.format(y) for y in plt.gca().get_yticks()])
    
    if desc_stats:
        table = [
            ['Mean', '{:,.0f}'.format(in_df[var].mean())],
            ['Median', '{:,.0f}'.format(in_df[var].median())],
            ['Std. Dev.', '{:,.0f}'.format(in_df[var].std())],
            ['Min', '{:,.0f}'.format(in_df[var].min())],
            ['Max', '{:,.0f}'.format(in_df[var].max())],
            ['N', '{:,.0f}'.format(in_df[var].count())],
            ]
        
        plt.table(cellText=table, loc='upper right', colWidths=[.15,.1])

    plt.savefig(output_path+'/KDEs/'+f'Dist. {label}.png', dpi=600)
    plt.close()



def run_numbers(year: int, abs_path: str, rel_path: Union[str, list[str]], id_var: list, geo: str, unit: str, ed_var:str, ed_mapping: dict, analysis_vars:dict, limit_cols: bool=True) -> pd.DataFrame:
    '''Function that reads in data, generates metrics and returns them as a dataframe'''
    
    def _readin(path) -> pd.DataFrame:
        use_cols = None
        if limit_cols:
            use_cols = id_var + [ed_var] + list(analysis_vars.keys())

        if path[-4:] == '.dta':
            df = pd.read_stata(path, columns=use_cols)
        elif path[-4:] == '.csv':
            df = pd.read_csv(path, usecols=use_cols)
        else:
            print(f'Exiting because path not for stata file or csv: {path}')
            exit()
        
        if len(df) != len(df.groupby(id_var, dropna=False).size()):
            print(f"\n \n \n ***************NOTE: {path.split('/')[-1]} is not unique by {id_var}***************\n \n \n")
            exit()
        return df


    if isinstance(rel_path, str):
        df = _readin(os.path.join(abs_path,str(year),rel_path))
    
    elif isinstance(rel_path, list):
        for i in rel_path:
            tmp = _readin(os.path.join(abs_path,str(year), i))
            if rel_path.index(i) == 0:
                df = tmp.copy()
            else:
                df = pd.merge(df, tmp, how='left', on=id_var)

    # Fuss necessary to deal with Stata types
    if df[ed_var].dtype.name == 'category':
        df[ed_var] = df[ed_var].cat.add_categories(["Missing"]).fillna("Missing")
    
    df['ed_group'] = df[ed_var].map(ed_mapping).fillna('Missing')
    tmp = df.groupby(['ed_group', ed_var], dropna=False).size().reset_index(name='Count')
    print(f'\n\nEd Mapping for {year} {geo}')
    print(tmp.loc[tmp['Count']!=0])

    df['geo'] = geo
    df['unit'] = unit
    df['year'] = year


    def _metric_table(in_df: pd.DataFrame, group_vars: list[str], var: str, label: str, var_group: str) -> pd.DataFrame:
        '''Return desc stats in stackable dataframe'''
        r = in_df.groupby(group_vars)[var].agg(agg_vars).reset_index()
        r['var_label'] = label
        r['var_code'] = var 
        r['var_group'] = var_group
        if 'ed_group' not in r.columns:
            r['ed_group'] = 'Overall'
        r = r.melt(id_vars=['year','geo','unit','ed_group','var_label','var_code','var_group'], value_vars=agg_vars, value_name='value', var_name='metric')
        return r


    out = pd.DataFrame(columns=['year','geo','unit','ed_group','var_label','var_code','var_group','metric','value'])
    agg_vars = ['mean','median','std','min','max','count']

    for var in analysis_vars.keys():
        tmp =df.loc[~df[var].isin(analysis_vars[var][2])]
        
        # Overall version
        out = pd.concat([out,
            _metric_table(in_df=tmp, group_vars=['year','geo','unit'], var=var, label=analysis_vars[var][0], var_group=analysis_vars[var][1])
        ])

        #By ed version
        make_fmt_kde(in_df=tmp, var=var, label=(f'{year} {geo} {analysis_vars[var][0] }'), var_label=analysis_vars[var][0], by_var='ed_group')
        out = pd.concat([out,
            _metric_table(in_df=tmp, group_vars=['year','geo','unit','ed_group'], var=var, label=analysis_vars[var][0], var_group=analysis_vars[var][1])
        ])

        #Some of the relevant fields come as monthly values, so run a coarse annualization as well
        if 'month' in analysis_vars[var][0].lower() or 'month' in analysis_vars[var][1].lower():
            tmp[f'Annualized {var}'] = tmp[var]*12
            # Overall version
            out = pd.concat([out,
            _metric_table(in_df=tmp, group_vars=['year','geo','unit'], var=f'Annualized {var}', label=f'Annualized from {analysis_vars[var][0]}',
            var_group=analysis_vars[var][1].replace('Monthly','Annual'))
            ])
            
            #By ed version
            out = pd.concat([out,
            _metric_table(in_df=tmp, group_vars=['year','geo','unit','ed_group'], var=f'Annualized {var}', label=f'Annualized from {analysis_vars[var][0]}',
            var_group=analysis_vars[var][1].replace('Monthly','Annual'))
            ])

    return out




from typing import TypedDict, Union


# A. Specifications for each survey following this data structure
specifications_dictionary = TypedDict('specifications_dictionary',
{'year': int,

# Flags for availability
'urban_individual_avail': bool,
'rural_individual_avail': bool,
'migrant_individual_avail': bool,
'urban_household_avail': bool,
'rural_household_avail': bool,
'migrant_household_avail': bool,

# file paths
'urban_indiv_path': Union[str,list[str]],
'rural_indiv_path': Union[str,list[str]],
'migrant_indiv_path': Union[str,list[str]],
'urban_household_path': Union[str,list[str]],
'rural_household_path': Union[str,list[str]],
'migrant_household_path': Union[str,list[str]],

# household and individual identifiers
'urban_household_id': str,
'urban_person_id': str,
'migrant_household_id': str,
'migrant_person_id': str,
'rural_household_id': str,
'rural_person_id': str,

# Education var and mapping
'urban_ed_var': str,
'urban_ed_mapping': dict,
'migrant_ed_var': str,
'migrant_ed_mapping': dict,
'rural_ed_var': str,
'rural_ed_mapping': dict,

# Analysis vars
'urban_individ_analysis_vars': dict[str,list],
'urban_household_analysis_vars': dict[str,list],
'migrant_individ_analysis_vars': dict[str,list],
'migrant_household_analysis_vars': dict[str,list],
'rural_individ_analysis_vars': dict[str,list],
'rural_household_analysis_vars': dict[str,list],

})


#------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------


d2018: specifications_dictionary = {
    'year': 2018,

    'urban_individual_avail' : True,
    'rural_individual_avail' : True,
    'migrant_individual_avail' : False,
    'urban_household_avail' : True,
    'rural_household_avail' : True,
    'migrant_household_avail' : False,

    'urban_indiv_path':'chip2018_urban_person.dta',
    'rural_indiv_path':'chip2018_rural_person.dta',
    'migrant_indiv_path':'',

    'urban_household_path':'',
    'rural_household_path':'',
    'migrant_household_path':'',

    'urban_household_id':'hhcode',
    'urban_person_id':'idcode',

    'migrant_household_id':'',
    'migrant_person_id':'',

    'rural_household_id':'hhcode',
    'rural_person_id':'idcode',


    'urban_ed_var': 'A13_1',
    'urban_ed_mapping': {
        -99: 'Missing',
        -88: 'Missing',
        1: 'None', #Never schooled
        2: 'Primary', #Elementary school
        3: 'Secondary', #Junior middle school
        4: 'Secondary', #Senior middle school
        5: 'Secondary', #Vocational senior secondary school/technical school ?
        6: 'Secondary', # Specialized secondary school ?
        7: 'Vocational', # Polytechnic college
        8: 'Undergrad +', # Undergraduate (Bachelor's degree)
        9: 'Undergrad +', # Graduate (Master's degree or above)
    },

    'migrant_ed_var': '',
    'migrant_ed_mapping': {},

    'rural_ed_var': 'A13_1',
    'rural_ed_mapping': {
        -99: 'Missing',
        -88: 'Missing',
        1: 'None', #Never schooled
        2: 'Primary', #Elementary school
        3: 'Secondary', #Junior middle school
        4: 'Secondary', #Senior middle school
        5: 'Secondary', #Vocational senior secondary school/technical school ?
        6: 'Secondary', # Specialized secondary school ?
        7: 'Vocational', # Polytechnic college
        8: 'Undergrad +', # Undergraduate (Bachelor's degree)
        9: 'Undergrad +', # Graduate (Master's degree or above)
    },

    # Var : [var label, List of MISSING VALUES]
    'urban_individ_analysis_vars': {
        'C05_1' : ['Indiv. Total wage income from job in 2018', 'Wages - Annual', [-99,-88]],
        'C09_8': ['Indiv. Average Net Income per Day', 'Wages - Daily', [-99,-88]]
    },

    'migrant_individ_analysis_vars': {},

    'rural_individ_analysis_vars': {
        'C05_1' : ['Indiv. Total wage income from job in 2018', 'Wages - Annual', [-99,-88]],
        'C09_8': ['Indiv. Average Net Income per Day', 'Wages - Daily', [-99,-88]]
    },


    'urban_household_analysis_vars': {
        'F01': ['Household Assets'],
        'F05': ['Household Debts'],
        'n3701': ['Household Disposable Income'],
        'n3702': ['Household Wage Income']
    },

    'migrant_household_analysis_vars' : {},

    'rural_household_analysis_vars' : {
        'F01': ['Household Assets'],
        'F05': ['Household Debts'],
        'n3701': ['Household Disposable Income'],
        'n3702': ['Household Wage Income']
    },
}
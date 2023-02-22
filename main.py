import specs
import functions
import os
import pandas as pd
import time

module_start_time = time.time()

root_folder = "/Raw Data/"
output_path = "/Output/Overall/"

# --------------------------------------------------
if not os.path.exists(output_path):
    os.makedirs(output_path)
    print(f'Output folder created at {output_path}')
# --------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------
# Loop through specification dictionaries to execute analysis functions
#------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------

list_of_specs: list[specs.specifications_dictionary] = [specs.d2007, specs.d2009, specs.d2013, specs.d2018]

out = pd.DataFrame(columns=['year','geo','unit','ed_group','var_label','var_code','var_group','metric','value'])

for spec in list_of_specs:
    
    if spec['urban_individual_avail']:
        out = pd.concat([out,
        functions.run_numbers(year = spec['year'], abs_path=root_folder, rel_path=spec['urban_indiv_path'], id_var=[spec['urban_household_id'],spec['urban_person_id']],
        geo='Urban', unit='Individual', ed_var=spec['urban_ed_var'], ed_mapping=spec['urban_ed_mapping'], analysis_vars=spec['urban_individ_analysis_vars'])
        ])
    
    if spec['migrant_individual_avail']:
        out = pd.concat([out,
        functions.run_numbers(year = spec['year'], abs_path=root_folder, rel_path=spec['migrant_indiv_path'], id_var=[spec['migrant_household_id'],spec['migrant_person_id']], 
        geo='Migrant', unit='Individual',ed_var=spec['migrant_ed_var'], ed_mapping=spec['migrant_ed_mapping'], analysis_vars=spec['migrant_individ_analysis_vars'])
        ])

    if spec['rural_individual_avail']:
        out = pd.concat([out,
        functions.run_numbers(year = spec['year'], abs_path=root_folder, rel_path=spec['rural_indiv_path'], id_var=[spec['rural_household_id'],spec['rural_person_id']],
        geo='Rural', unit='Individual', ed_var=spec['rural_ed_var'], ed_mapping=spec['rural_ed_mapping'], analysis_vars=spec['rural_individ_analysis_vars'])
        ])


out.to_csv(output_path+'CHIP_income_summary.csv', index=False)


print("--- %s seconds to run full module ---" % round((time.time() - module_start_time),3))
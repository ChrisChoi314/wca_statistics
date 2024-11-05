import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import rankdata
from scipy.stats import pearsonr

# Load WCA data
Results = pd.read_csv('data/WCA_export309_20241104T002532Z.tsv/WCA_export_RanksSingle.tsv', sep='\t')

# Load WCA persons data
Persons = pd.read_csv('data/WCA_export309_20241104T002532Z.tsv/WCA_export_Persons.tsv', sep='\t')

# Load fto rankings data and add it to the WCA results
fto_results = pd.read_csv('queries/correlation_wca/fto_rankings.tsv', sep='\t')
fto_results['eventId'] = 'fto'  # Set the eventId for fto rankings

# Replace 'personId' in fto_results with 'id' from WCA persons data
fto_results = fto_results.rename(columns={'id': 'personId'})  # Rename 'id' to 'personId'
fto_results = fto_results.rename(columns={'rank': 'worldRank'})  # Rename 'result' to 'best' to match WCA data
fto_results = fto_results[['name', 'eventId', 'worldRank']]  # Include necessary columns

# Step 1: Filter fto_rankings to keep only rows with names that have a match in WCA_export_Persons
filtered_fto_rankings = fto_results[fto_results['name'].isin(Persons['name'])]

# Step 2: Merge the filtered fto_rankings with Persons to get the 'id' for each matching name
filtered_fto_rankings = filtered_fto_rankings.merge(Persons[['id', 'name']], on='name', how='left')
filtered_fto_rankings = filtered_fto_rankings.rename(columns={'id': 'personId'})  # Rename 'id' to 'personId'

# Select only the necessary columns to match the WCA data structure
filtered_fto_rankings = filtered_fto_rankings[['personId', 'eventId', 'worldRank']]

# Step 3: Filter the Results dataset to include only rows with personIds found in filtered_fto_rankings
filtered_person_ids = filtered_fto_rankings['personId'].unique()
Results = Results[Results['personId'].isin(filtered_person_ids)]

# Concatenate the filtered Results with fto data for further analysis if needed
Results = pd.concat([Results, filtered_fto_rankings], ignore_index=True)

# Merge with WCA data
Results = pd.concat([Results, fto_results], ignore_index=True)
Results = Results[['personId', 'eventId', 'worldRank']]  # Assuming 'result' column has the results

# Remove duplicate entries based on personId, competitionId, and eventId
Results = Results.drop_duplicates(subset=['personId',  'eventId'])

# Standardize eventId to ensure all values are strings
Results['eventId'] = Results['eventId'].astype(str)

# Filter out the specific events to exclude from analysis
excluded_events = ['333mbo', 'magic', 'mmagic', '333ft']
Results = Results[~Results['eventId'].isin(excluded_events)]

# Calculate percentile ranks for each event
Results['percentile_rank'] = Results.groupby('eventId')['worldRank'].transform(
    lambda x: 100 - rankdata(x, method='average') / len(x) * 100
)

# Reshape data for correlation matrix
events_participation = Results.pivot_table(index=['personId'], 
                                           columns='eventId', 
                                           values='percentile_rank', 
                                           fill_value=0)

# Calculate correlation matrix
corrmat = events_participation.corr(method='pearson')

# Create an empty dataframe to store the p-values
p_values = pd.DataFrame(index=corrmat.index, columns=corrmat.columns).astype(float)
for col1 in corrmat.columns:
    for col2 in corrmat.columns:
        corr, p_value = pearsonr(events_participation[col1], events_participation[col2])
        p_values.at[col1, col2] = p_value

plt.figure(figsize=(15, 12))
sns.mpl_palette("magma", 6)
#sns.heatmap(p_values,xticklabels=True, yticklabels=True, annot=True, fmt=".3f", annot_kws={"size": 8}, linewidths=.5, linecolor='gray')
sns.heatmap(corrmat,xticklabels=True, yticklabels=True, annot=True, fmt=".3f", annot_kws={"size": 8}, linewidths=.5, linecolor='gray')

print("Correlation Matrix:")
print(corrmat.dtypes)   
print("\nP-value Matrix:")
print(p_values.dtypes)

# Rotate the labels
plt.xticks(rotation=90)  # Make x-axis labels vertical
plt.yticks(rotation=0)    # Make y-axis labels horizontal
plt.title(f'Event Percentile Rank Correlation + FTO P-Values Heat Map (n = {len(Results["personId"].unique())})')
plt.savefig("queries/correlation_wca/correlate_figs/correlation_fto_3_dec.pdf")
plt.show()

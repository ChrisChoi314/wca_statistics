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
sns.heatmap(p_values,xticklabels=True, yticklabels=True, annot=True, fmt=".3f", annot_kws={"size": 8}, linewidths=.5, linecolor='gray')
#sns.heatmap(corrmat,xticklabels=True, yticklabels=True, annot=True, fmt=".2f", annot_kws={"size": 8}, linewidths=.5, linecolor='gray')

# Rotate the labels
plt.xticks(rotation=90)  # Make x-axis labels vertical
plt.yticks(rotation=0)    # Make y-axis labels horizontal
plt.title(f'WCA Event Percentile Rank Correlation P-Values Heat Map (n = {len(Results["personId"].unique())})')
plt.savefig("queries/correlation_wca/correlate_figs/correlation_all_p_values.pdf")
plt.show()

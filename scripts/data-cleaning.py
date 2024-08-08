# import libraries
import pandas as pd

# Create new column names because text file has no header
col_names = ["Type", "Author", "Year", "Title", "Journal Name", "Volume", "Issue", "Pages", "URL", "Keywords", "Abstract", "DOI", "PDF Name"]

# Convert text files into a dataframe
silver_yes = pd.read_csv('data/raw-data/Hypopthalmichthys_molitrix_yes.txt', sep = '\t', header = None, dtype = str, names = col_names, quotechar = '"')
silver_all = pd.read_csv('data/raw-data/Hypopthalmichthys_molitrix_all.txt', sep = '\t', header = None, dtype = str, names = col_names, quotechar = '"')
bighead_yes = pd.read_csv('data/raw-data/Hypopthalmichthys_nobilis_yes.txt', sep = '\t', header = None, dtype = str, names = col_names, quotechar = '"')
bighead_all = pd.read_csv('data/raw-data/Hypopthalmichthys_nobilis_all.txt', sep = '\t', header = None, dtype = str, names = col_names, quotechar = '"')


# Combine data with selected articles
carp_yes = pd.concat([silver_yes, bighead_yes], ignore_index = True)

# Combine all article - duplicates removed in next step to get irrelevant articles
carp_concat = pd.concat([silver_yes, silver_all, bighead_yes, bighead_all], ignore_index = True)

# Drop duplicates to get unselected articles
carp_no = carp_concat.drop_duplicates(keep = False, ignore_index = True)

# subset and select by columns
columns = ["Author", "Year", "Title", "Journal Name", "Volume", "Issue", "Pages", "Abstract"]

carp_yes = carp_yes[columns]
carp_no = carp_no[columns]

# add category columns
carp_yes['categories'] = 'yes'
carp_no['categories'] = 'no'

# combine df
carp_all = pd.concat([carp_yes, carp_no], ignore_index = True)

# Drop any abstracts with NAs
carp_all.dropna(subset = ['Abstract'], inplace = True)

# Create new encoding for category column
# Concatenate Title and Abstract
carp_all["TitleAbstract"] = carp_all["Title"] + ' ' + carp_all["Abstract"]

# Export to csv files
carp_all.to_csv('data/processed/hypopthalmichthys_selected_articles.csv', index = False)
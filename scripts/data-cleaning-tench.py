# import libraries
import pandas as pd
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, SnowballStemmer, WordNetLemmatizer
nltk.download('stopwords')
from sklearn.preprocessing import LabelEncoder

# create new column names because text file has no header
col_names = ["Type", "Author", "Year", "Title", "Journal Name", "Volume", "Issue", "Pages", "URL", "Keywords", "Abstract", "DOI", "PDF Name"]

# convert text files into a dataframe
tench_yes = pd.read_csv('data/raw-data/Tinca-tinca-yes.txt', sep = '\t', header = None, dtype = str, names = col_names, quotechar = '"')
tench_no = pd.read_csv('data/raw-data/Tinca-tinca-no.txt', sep = '\t', header = None, dtype = str, names = col_names, quotechar = '"')

# add category columns
tench_yes['categories'] = 'yes'
tench_no['categories'] = 'no'

# combine df
tench_all = pd.concat([tench_yes, tench_no], ignore_index = True)

# drop any abstracts with NAs
tench_all.dropna(subset = ['Abstract'], inplace = True)

# concatenate Title and Abstract
tench_all["TitleAbstract"] = tench_all["Title"] + ' ' + tench_all["Abstract"]

# Subset and select by columns
columns = ["Author", "Year", "Title", "Journal Name", "Volume", "Issue", "Pages", "Abstract", "TitleAbstract", "categories"]
tench_all = tench_all[columns]

# Create label encoder 
label_encoder = LabelEncoder()
tench_all["categories"] = label_encoder.fit_transform(tench_all['categories'])

# get the set of English stopwords
stop_words = set(stopwords.words('english'))

# function to remove HTML tags
def basic_clean(text):
    text = re.sub(r'<.*?>', '', text)
    text = text.strip()
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'[^\w\s]', '', text)

    # Function to remove stopwords from text
    def remove_stopwords(text):
        # Tokenize the text
        tokens = nltk.word_tokenize(text)
        # Filter out stopwords
        filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
        # Reconstruct the text without stopwords
        text_without_stopwords = ' '.join(filtered_tokens)
        return text_without_stopwords

    text = remove_stopwords(text)

    stemmer = SnowballStemmer(language = 'english')
    text = " ".join([stemmer.stem(word) for word in text.split()])

    return text

tench_all_clean = tench_all.copy()    
tench_all_clean['TitleAbstract'] = tench_all_clean['TitleAbstract'].apply(basic_clean)

# Export to csv files
tench_all_clean.to_csv('data/processed/tench-train-test.csv', index = False)
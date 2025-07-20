import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from deep_translator import GoogleTranslator


# inisialisasi
translator = GoogleTranslator()
lemmatizer = WordNetLemmatizer()

# stopwords umum + custom 
stop_words = set(stopwords.words('english'))
custom_stopwords = set([
    'pt', 'cv', 'tbk', 'persero', 'dkk', 'dll', 'dst',
    'required', 'requirement', 'requirements',
    'qualifications', 'qualification', 'description',
    'primary', 'main', 'responsibility', 'responsibilities'
])
all_stopwords = stop_words.union(custom_stopwords)

# normalisasi teks 
def normalize_text(text):
    text = text.lower()
    emoji_pattern = re.compile("["                     
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251" "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# translate teks campuran ke full bahasa Inggris
def translate_to_english(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text

# fungsi untuk preprocessing teks
def preprocess_text(text, translate=False):
    if translate:
        text = translate_to_english(text)
    text = normalize_text(text)
    tokens = word_tokenize(text)
    filtered_tokens = [
        lemmatizer.lemmatize(w) for w in tokens if w not in all_stopwords
    ]
    return ' '.join(filtered_tokens)

# preprocess data lowongan pekerjaan 
def preprocess_jobstreet(file_path):
    df = pd.read_csv(file_path)
    df['cleaned_text'] = df['job_details'].apply(
        lambda x: preprocess_text(str(x), translate=True)
    )
    return df[['job_title', 'category','cleaned_text']]

# preprocess data course online 
def preprocess_courses(file_path):
    df = pd.read_csv(file_path)
    df['text'] = df['Course Name'].fillna('') + ' ' + \
                 df['Difficulty Level'].fillna('') + ' ' + \
                 df['Course Description'].fillna('') + ' ' + \
                 df['Skills'].fillna('')
    df['cleaned_text'] = df['text'].apply(
        lambda x: preprocess_text(str(x), translate=False)
    )
    return df[['Course Name', 'cleaned_text']]

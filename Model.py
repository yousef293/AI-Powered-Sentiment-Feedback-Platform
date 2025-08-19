import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import re
import joblib
import emoji
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

# Load and preprocess
data = pd.read_csv('./data.csv')
data['reviewText'] = data['reviewText'].astype(str).str.lower().str.split()

# Balance dataset
max_count = data['overall'].value_counts().max()
balanced_data = (
    data.groupby('overall', group_keys=False)
        .apply(lambda x: x.sample(max_count, replace=True, random_state=42))
        .sample(frac=1, random_state=42)
        .reset_index(drop=True)
)

Y = balanced_data['overall']
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

class SentimentModel:
    def __init__(self):
        self.logistic = LogisticRegression(max_iter=1000)
        self.x_train = self.x_test = self.y_train = self.y_test = None
        
    def nlp(self,text):
        
        text=emoji.demojize(text,delimiters=(" "," "))

        text=text.lower()
        text = re.sub(r'[^a-z\s]', '', text)
        tokens=nltk.word_tokenize(text)
        tokens=[word for word in tokens if word not in stop_words]
        tokens=[lemmatizer.lemmatize(word)for word in tokens]
        return ' '.join(tokens)

    
    def prepare_data(self):
        self.vectorizer=TfidfVectorizer()
        X = [self.nlp(tokens) for tokens in balanced_data['reviewText']]
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            X, Y, test_size=0.2, random_state=42
        )
        self.x_train = self.vectorizer.fit_transform(self.x_train)
        self.x_test =self.vectorizer.transform(self.x_test)

    
    def train_model(self):
        self.prepare_data()
        self.logistic.fit(self.x_train, self.y_train)
        joblib.dump(self.logistic,'pre_trained_model.pkl')
        joblib.dump(self.vectorizer,'tfidvectorizer.pkl')
    
    def evaluate_model(self):
        y_pred = self.logistic.predict(self.x_test)
        print(classification_report(self.y_test, y_pred))
    
    def predict(self,text):
        label_map = {
            -1: 'Negative',
            0: 'Neutral',
            1: 'Positive'
        }
        cleaned_text = self.nlp(text)  
        vectorized_text = self.vectorizer.transform([cleaned_text])
        output = self.logistic.predict(vectorized_text)
        confidence=self.logistic.predict_proba(vectorized_text)
        label = int(output[0])

        return {"sentiment":label_map[label], "confidence":round(np.max(confidence), 2)}
    def load_model(self, model_path='pre_trained_model.pkl', vectorizer_path='tfidvectorizer.pkl'):
        self.logistic = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)

if __name__ == "__main__":
    mod = SentimentModel()
    mod.train_model()
    mod.evaluate_model()




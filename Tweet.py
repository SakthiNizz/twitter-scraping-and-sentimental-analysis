import snscrape.modules.twitter as sntwitter
import pandas as pd
import streamlit as st
import pymongo
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
import string 
import re
nltk.download('stopwords')
stemmer=nltk.SnowballStemmer("english")

tweets_list1 = []
with st.form("my_form"):
    default_since = '2019-01-01'
    default_until = '2019-06-30'
    search = st.text_input("Enter the text you want to search : ")
    since = st.text_input('Enter the Start_date :',default_since) 
    until = st.text_input('Enter the End_date :', default_until)
    maxTweets = st.slider('Enter the count :', 0,1000,50)
    summit = st.form_submit_button('Submit')
    if summit:
        passing = (f'{search} since:{since} until:{until}')
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(passing).get_items()):
            if i>maxTweets:
                break
            tweets_list1.append([tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.url, tweet.replyCount,  tweet.retweetCount,tweet.lang, tweet.likeCount ])


tweets_df1 = pd.DataFrame(tweets_list1, columns=['DateTime', 'Tweet_ID', 'Content', 'User_Name', 'URL', 'Reply_count', 'Re_Tweet_Count','Language', 'Like_Count'])
st.write(tweets_df1)

stopword=set(stopwords.words('english'))
def clean(text):
    text=str(text).lower()
    text=re.sub('\[.*?\]', '',text)
    text=re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = [word for word in text.split(' ') if word not in stopword]
    text=" ".join(text)
    text = [stemmer.stem(word) for word in text.split(' ')]
    text=" ".join(text)
    return text
tweets_df1['Content']=tweets_df1['Content'].apply(clean)


from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import streamlit as st
from collections import Counter
st.set_option('deprecation.showPyplotGlobalUse', False)

if tweets_df1.empty:
    st.warning('No tweets found with the specified criteria.')
else:
    text = " ".join(i for i in tweets_df1.Content)
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)

    # Add title to the WordCloud
    plt.figure(figsize=(15, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.suptitle("Most frequent words",fontsize=50)
    plt.title("Search Keyword: " + search + ", Period: " + since + " to " + until, fontsize=30, fontweight='bold')

    # Display the most frequent words
    words_count = Counter(text.split())
    most_common = words_count.most_common(10)
    st.write("Top 10 most frequent words:")
    for word, freq in most_common:
        st.write(f"{word.capitalize()} : {freq}")

    st.pyplot()
    
    
    
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from collections import Counter
import streamlit as st
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

sentiments = SentimentIntensityAnalyzer()
tweets_df1['Positive'] = [sentiments.polarity_scores(i)["pos"] for i in tweets_df1['Content']]
tweets_df1['Negative'] = [sentiments.polarity_scores(i)["neg"] for i in tweets_df1['Content']]
tweets_df1['Neutral'] = [sentiments.polarity_scores(i)["neu"] for i in tweets_df1['Content']]
tweets_df1 = tweets_df1[['Content', 'Positive', 'Negative', 'Neutral']]

if tweets_df1.empty:
    st.warning('No tweets found with the specified criteria.')
else:
    positive = ' '.join([i for i in tweets_df1['Content'][tweets_df1['Positive'] > tweets_df1['Negative']]])
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(positive)

    # Add title to the WordCloud
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    ax.set_title("Positive Sentiment Word Cloud",fontsize=50)

    # Display the WordCloud
    st.pyplot(fig)
    
    
if tweets_df1.empty:
    st.warning('No tweets found with the specified criteria.')
else:
    positive = ' '.join([i for i in tweets_df1['Content'][tweets_df1['Negative'] > tweets_df1['Positive']]])
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(positive)

    # Add title to the WordCloud
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    ax.set_title("Negative Sentiment Word Cloud",fontsize=50)

    # Display the WordCloud
    st.pyplot(fig)    


x = sum(tweets_df1["Positive"])
y = sum(tweets_df1["Negative"])
z = sum(tweets_df1["Neutral"])

def sentiment_score(a, b, c):
    if (a>b) and (a>c):
        print("Positive 😊 ")
    elif (b>a) and (b>c):
        print("Negative 😠 ")
    else:
        print("Neutral 🙂 ")
sentiment_score(x, y, z)

# Display the results in Streamlit
st.write("Sentiment Analysis Results")
st.write("-------------------------")
st.write("Positive: ", x)
st.write("Negative: ", y)
st.write("Neutral: ", z)

    
    



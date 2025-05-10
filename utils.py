import requests
from bs4 import BeautifulSoup
from gtts import gTTS
from transformers import pipeline
from googletrans import Translator

# Sentiment analysis setup
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Search for research papers
def search_research_papers(topic):
    query = topic.replace(" ", "+")
    url = f"https://arxiv.org/search/?query={query}&searchtype=all&abstracts=show&order=-announced_date"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    papers = []
    for result in soup.find_all('li', class_='arxiv-result'):
        title = result.find('p', class_='title').text.strip()
        link = result.find('a')['href']
        summary = result.find('p', class_='abstract').text.strip()

        sentiment = analyze_sentiment(summary)
        papers.append({"title": title, "link": link, "summary": summary, "sentiment": sentiment})
    return papers

# Summarize a paper (simplified)
def summarize_paper(text):
    # Example of summarization (you can replace with a better model)
    return text[:300] + "..."  # Truncate to first 300 chars

# Sentiment analysis function
def comparative_analysis(text):
    result = sentiment_pipeline(text)[0]
    return result['label']

# Convert text to speech (using gTTS)
def text_to_speech(text, language='en'):
    tts = gTTS(text, lang=language)
    tts.save("output.mp3")
    return "output.mp3"

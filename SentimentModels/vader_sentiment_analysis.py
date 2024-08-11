import PyPDF2 as PDF
import openpyxl
import nltk
import os
from nltk.tokenize import sent_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer as Sia

def read_pdf(pdf_path):
    text = ''
    try:
        with open(pdf_path, "rb") as file:
            pdf_reader = PDF.PdfFileReader(file)
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                text += page.extract_text()
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return None
    return text


def tokenizer(text):
    return sent_tokenize(text)


def perform_sentiment_analysis(text, sentiment_model):
    sentences = tokenizer(text)
    neg_score = 0.0
    neu_score = 0.0
    pos_score = 0.0
    comp_score = 0.0
    count = 0.0
    for sentence in sentences:
        sentence_sentiment = sentiment_model.polarity_scores(sentence)
        neg_score += sentence_sentiment['neg']
        neu_score += sentence_sentiment['neu']
        pos_score += sentence_sentiment['pos']
        comp_score += sentence_sentiment['compound']
        count += 1
    result = {
        'Negative Score': neg_score/count,
        'Neutral Score': neu_score/count,
        'Positive Score': pos_score/count,
        'Overall Score': comp_score/count,
    }
    return result


def overall_sentiment(text, sentiment_model):
    sentiment_result = perform_sentiment_analysis(text, sentiment_model)
    if sentiment_result['Overall Score'] > 0:
        overall_sent = 'POSITIVE'
    else:
        overall_sent = 'NEGATIVE'
    sentiment_result.update({'Overall Sentiment': overall_sent})

    return sentiment_result


def process_pdf_vader(folder_path):
    sentiment_model = Sia()
    files = os.listdir(folder_path)
    pdf_files = []
    sentiment_list = []

    for file in files:
        if file.endswith(".pdf"):
            pdf_files.append(file)

    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        print(f"Reading {pdf_file}...")
        text = read_pdf(pdf_path)
        if text is None:
            sentiment_list.append({
                "Negative Score": 0.0,
                "Neutral Score": 0.0,
                "Positive Score": 0.0,
                "Overall Score": 0.0,
                "Overall Sentiment": "NONE",
                "PDF File Name": pdf_file
            })
            continue
        sentiment_result = overall_sentiment(text, sentiment_model)
        sentiment_result.update({'PDF File Name': pdf_file})
        sentiment_list.append(sentiment_result)
        print("PDF has been analysed")

    return sentiment_list


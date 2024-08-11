import PyPDF2 as PDF
import openpyxl
import os
from textblob import TextBlob
from nltk import sent_tokenize

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


def perform_sentiment_analysis(text):
    polarity_score = 0.0
    subjectivity_score = 0.0
    count = 0.0
    sentences = tokenizer(text)
    for sentence in sentences:
        sentence_sentiment = TextBlob(sentence).sentiment
        polarity_score += sentence_sentiment.polarity
        subjectivity_score += sentence_sentiment.subjectivity
        count += 1
    result = {
        "Polarity": polarity_score/count,
        "Subjectivity": subjectivity_score/count
    }
    return result


def overall_sentiment(text):
    sentiment_result = perform_sentiment_analysis(text)
    if sentiment_result['Polarity'] > 0:
        overall_sent = "POSITIVE"
    else:
        overall_sent = "NEGATIVE"
    sentiment_result.update({"Overall Sentiment": overall_sent})

    return sentiment_result


def process_pdf_textblob(folder_path):
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
                "Polarity": 0.0,
                "Subjectivity": 0.0,
                "Overall Sentiment": "NONE",
                "PDF File Name": pdf_file
            })
            continue
        sentiment_result = overall_sentiment(text)
        sentiment_result.update({'PDF File Name': pdf_file})
        sentiment_list.append(sentiment_result)
        print("PDF has been analysed")

    return sentiment_list

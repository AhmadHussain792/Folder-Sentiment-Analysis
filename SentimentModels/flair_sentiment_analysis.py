import PyPDF2 as PDF
import openpyxl
import nltk
import os
from nltk.tokenize import sent_tokenize
from flair.models import TextClassifier
from flair.data import Sentence

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


def tokenise(text):
    return sent_tokenize(text)

def perform_sentiment_analysis(text, model):
    sentences = tokenise(text)
    pos_score = 0.0
    neg_score = 0.0
    count = len(sentences)
    for sentence in sentences:
        sentence = Sentence(sentence)

        model.predict(sentence)

        score = sentence.labels[0].score
        label = sentence.labels[0].value

        if label == "POSITIVE":
            pos_score += score
        else:
            neg_score += score
    result = {
        "Positive Score": pos_score/count,
        "Negative Score": neg_score/count
    }
    return result

def overall_sentiment(text, model):
    sentiment_result = perform_sentiment_analysis(text, model)
    if sentiment_result['Positive Score'] > sentiment_result['Negative Score']:
        overall = "POSITIVE"
    else:
        overall = "NEGATIVE"
    sentiment_result.update({"Overall Sentiment": overall})

    return sentiment_result


def process_pdf_flair(folder_path):
    model = TextClassifier.load("en-sentiment")
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
                "Positive Score": 0.0,
                "Negative Score": 0.0,
                "Overall Sentiment": "NONE",
                "PDF File Name": pdf_file
            })
            continue
        sentiment_result = overall_sentiment(text, model)
        sentiment_result.update({'PDF File Name': pdf_file})
        sentiment_list.append(sentiment_result)
        print("PDF has been analysed")

    return sentiment_list

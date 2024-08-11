import PyPDF2 as PDF
import openpyxl
import nltk
import os
from nltk.tokenize import sent_tokenize
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as funct

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


def tokenize_to_sentences(text):
    return sent_tokenize(text)


def perform_sentiment_analysis(text, tokenizer, model):
    positive_score = 0.0
    negative_score = 0.0
    count = 0
    sentences = tokenize_to_sentences(text)
    for sentence in sentences:
        inputs = tokenizer(sentence, return_tensors="pt")

        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits

        probs = funct.softmax(logits, dim=-1)
        positive_score += probs[0][1].item()
        negative_score += probs[0][0].item()
        count += 1
        result = {
            "Positive Score": positive_score/count,
            "Negative Score": negative_score/count
        }

        return result


def overall_sentiment(text, tokenizer, model):
    sentiment_result = perform_sentiment_analysis(text, tokenizer, model)
    if sentiment_result['Positive Score'] > sentiment_result['Negative Score']:
        sentiment_result.update({"Overall Sentiment": 'POSITIVE'})
    else:
        sentiment_result.update({'Overall Sentiment': "NEGATIVE"})

    return sentiment_result


def process_pdf_transformer(folder_path):
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
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
        sentiment_result = overall_sentiment(text, tokenizer, model)
        sentiment_result.update({'PDF File Name': pdf_file})
        sentiment_list.append(sentiment_result)
        print("PDF has been analysed")

    return sentiment_list


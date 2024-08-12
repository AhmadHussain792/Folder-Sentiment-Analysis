# PDF Sentiment Analyzer App

The PDF Sentiment Analyzer App is a Python-based graphical user interface (GUI) application that allows users to perform sentiment analysis on PDF files within a selected folder. The app supports multiple sentiment analysis models, including VADER, TextBlob, BERT Transformer, and Flair. Results are saved to an Excel file.

Example PDF files are uploaded in the 'PDF' folder and the sentiment analysis of these files using VADER is stored in 'JOURNAL.XLSX' excel file. Moreover, the python code for the 4 AI models can be found in the 'SentimentModels' folder.

# Features
- Model Selection: Choose from multiple sentiment analysis models (VADER, TextBlob, BERT Transformer, Flair).
- Folder Upload: Select a folder containing PDFs for batch sentiment analysis.
- Result Export: Sentiment analysis results are exported to an Excel file.
- User-Friendly Interface: Simple GUI built with tkinter.

# Requirements

I used Anaconda to create a virtual environment and install the required packages inside the environment.

python version : 3.12.4

conda version : 24.7.1

Please see 'REQUIREMENTS.TXT' file for more info on all libraries and packages used for this app.

# How to Use

1. Upload Folder Button: Select a folder containing the PDFs you want to analyze.
2. Model Selection Combobox: Choose the sentiment analysis model you want to use.
3. Perform Sentiment Analysis Button: Start the analysis process and save the results to an Excel file.

# Code Explanation 

The Python scripts for all of the sentiment analysis models have been *packaged* into a folder 'SentimentModels' and the main functions in each of these scripts are imported into the 'app.py' file.
The folder structure for all of the program files is as follows:

![folder structure ](https://github.com/user-attachments/assets/e666c54e-e5c6-4f74-beaf-9065ea848ed8)

***Explanation of app.py***:

- `write_to_excel(data, folder_path)` : Converts the sentiment analysis data into a DataFrame and writes it to an Excel file. It notifies the user once the data has been written using 'messagebox'
- `backend_process()` : Handles the main logic of the app, and checks if a folder is selected and a model is chosen, then processes the PDFs using the selected model. It calls write_to_excel() to save the results.
- `on_select_model(event)` : Updates the global 'model' variable when a model is selected from the combobox.
- `remove_placeholder_model(event)` : Clears the placeholder text in the model selection combobox when clicked.
- `upload_folder()` : Opens a dialog for selecting a folder and updates the global 'folder_path' variable.

***Explanation of model .py files***:

**Note: this is a general explanation of what the functions used in the AI model python files do; the working of each function may vary from model to model:**

- `read_pdf(pdf_path)` : opens the PDF file and extracts the text from it.
- `tokenizer(text)` : tokenizes the text extracted from the PDF file into sentences using 'nltk.sent_tokenize'
- `perform_sentiment_analysis()` : This function calls 'tokenizer' function and performs sentiment analysis on each sentence. It returns an aggregated sentiment score across all sentences.
- `overall_sentiment()` : Calls 'perform_sentiment_analysis' function and determines the overall sentiment (positive or negative) based on the values returned.
- `process_pdf(folder_path)` : Main backend function that orchestrates the sentiment analysis process by calling the above functions


# Final Result

GUI Interface:

![image](https://github.com/user-attachments/assets/57b4f6ba-4dc5-48bb-b66a-24cf7c60dc21)

Uploading a folder opens the file explorer:

![image](https://github.com/user-attachments/assets/290a4e2b-ef89-4a77-b786-c071af0e1ec4)

Selecting the AI model:

![image](https://github.com/user-attachments/assets/9e94b3a0-2dea-4248-8391-2a7e782910f8)




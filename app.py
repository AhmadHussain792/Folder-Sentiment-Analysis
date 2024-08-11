import pandas as pd
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import os
from SentimentModels.vader_sentiment_analysis import process_pdf_vader
from SentimentModels.textblob_sentiment_analysis import process_pdf_textblob
from SentimentModels.transformer_sentiment_analysis import process_pdf_transformer
from SentimentModels.flair_sentiment_analysis import process_pdf_flair

def write_to_excel(data, folder_path):
    df = pd.DataFrame(data)
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name=os.path.basename(folder_path), index=False)

    messagebox.showinfo(title="Process Complete", message=f"Data from folder '{folder_path}' has been written to {excel_path}")

def backend_process():
    global folder_path
    global model
    if folder_path:
        start_process.config(text="Processing PDFs...", state="disabled", bg="grey")
        root.update_idletasks()
        if model == "VADER":
            data = process_pdf_vader(folder_path)
        elif model == "TextBlob":
            data = process_pdf_textblob(folder_path)
        elif model == "BERT Transformer":
            data = process_pdf_transformer(folder_path)
        else:
            data = process_pdf_flair(folder_path)
        print(f"All PDFs in folder: '{folder_path}' have been analysed")

        write_to_excel(data, folder_path)
        start_process.config(text="Perform Sentiment Analysis", state="normal", bg="#7c49a6")
    else:
        messagebox.showwarning("No Folder Selected", "Please select a folder to process.")


def on_select_model(event):
    global model
    selected_option = model_entry.get()
    if selected_option == "Select":
        messagebox.showerror("ERROR","No option selected")
    model = selected_option
    print(model)


def remove_placeholder_model(event):
    if model_entry.get() == "Select":
        model_entry.set(' ')
        model_entry['values'] = ['VADER','TextBlob', 'BERT Transformer', 'Flair']


def upload_folder():
    global folder_path
    folder_path = filedialog.askdirectory()
    print(folder_path)


#define excel sheet
excel_path = "Journal 2.xlsx"

model = None
folder_path = None

root = tk.Tk()
root.title("Sentiment Analysis App")
root.geometry("600x400")

title_label = tk.Label(root, text=" PDF Sentiment Analyzer App", bg="#7f4e9a", fg="white", font=("Helvetica", 16, "bold"))
title_label.pack(side=tk.TOP, fill=tk.X, pady=5, ipadx=10, ipady=10)

labelframe = tk.LabelFrame(root, text="UPLOAD FOLDER", bg="#f5abf4", fg="black", font=("Helvetica", 12, "bold"))
labelframe.pack(pady=5, fill=tk.BOTH, expand=True)

select_folder = tk.Label(labelframe, text="Select Folder", bg="#f5abf4")
select_folder.grid(row=0, column=0, padx=10, pady=10, sticky="w")

folder_button = ttk.Button(labelframe, text="Upload Folder", command=upload_folder)
folder_button.grid(row=0, column=1, padx=10, pady=10, sticky="w")

select_model = tk.Label(labelframe, text="Select AI Model", bg="#f5abf4")
select_model.grid(row=2, column=0, padx=10, pady=10, sticky="w")

model_entry = ttk.Combobox(labelframe, values=['VADER','TextBlob', 'BERT Transformer', 'Flair'])
model_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")
model_entry.set("Select")
model_entry.bind("<<ComboboxSelected>>", on_select_model)
model_entry.bind("<Button-1>", remove_placeholder_model)

start_process = tk.Button(root, text="Perform Sentiment Analysis", bg="#7c49a6", fg="white", font=("Helvetica", 16, "bold"), cursor="hand2", state="normal", command=backend_process)
start_process.pack(side=tk.BOTTOM, fill=tk.X, pady=5)


root.mainloop()





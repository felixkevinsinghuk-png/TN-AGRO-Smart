import os
from flask import Flask, redirect, render_template, request, jsonify
from PIL import Image
import torchvision.transforms.functional as TF
import numpy as np
import torch
import torch.nn as nn
import pandas as pd

# LangChain & Llama setup
# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_community.llms import LlamaCpp
# from langchain.chains import RetrievalQA
# from langchain_core.prompts import PromptTemplate

# Device setup
if torch.backends.mps.is_available():
    device = torch.device("mps")
    print("Using MPS (Apple GPU)")
else:
    device = torch.device("cpu")
    print("Using CPU")

# Load disease & supplement data
disease_info = pd.read_csv('disease_info.csv', encoding='cp1252')
supplement_info = pd.read_csv('supplement_info.csv', encoding='cp1252')

# Model architecture exactly matching plant_disease_model_m3.pt
class PlantDiseaseModel(nn.Module):
    def __init__(self, num_classes=38):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, 3, padding=1),    # features.0  224→224
            nn.ReLU(),                           # features.1
            nn.MaxPool2d(2),                     # features.2  224→112
            nn.Conv2d(16, 32, 3, padding=1),    # features.3  112→112
            nn.ReLU(),                           # features.4
            nn.MaxPool2d(2),                     # features.5  112→56
            nn.Conv2d(32, 64, 3, padding=1),    # features.6  56→56
            nn.ReLU(),                           # features.7
            nn.MaxPool2d(2),                     # features.8  56→28
        )
        # After 3x MaxPool on 224: 224/8 = 28 → 28x28x64 = 50176
        self.classifier = nn.Sequential(
            nn.Dropout(0.4),                    # classifier.0
            nn.Linear(50176, 128),              # classifier.1
            nn.ReLU(),                          # classifier.2
            nn.Dropout(0.4),                    # classifier.3
            nn.Linear(128, num_classes),        # classifier.4
        )
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        return self.classifier(x)

model = PlantDiseaseModel(num_classes=38)
model.load_state_dict(torch.load("plant_disease_model_m3.pt", map_location=device), strict=False)
model.eval()

# Load vector DB and LLM (Commented out to prevent crashes if models are missing)
# embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
# db = FAISS.load_local(
#     folder_path="/Users/felixkevinsinght/TN/db_faiss",
#     embeddings=embeddings,
#     allow_dangerous_deserialization=True
# )
# 
# llm = LlamaCpp(
#     model_path="/Users/felixkevinsinght/TN/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
#     n_ctx=2048,
#     max_tokens=512,
#     n_gpu_layers=40,
#     temperature=0.7,
#     verbose=False,
# )
# 
# # Prompt template for chatbot
# template = """
# [INST] <<SYS>>
# Use the pieces of information provided in the context to answer user's question.
# If you dont know the answer, just say that you dont know, dont try to make up an answer. 
# Dont provide anything out of the given context.
# If the word limit are given give according to the needs.
# Context: {context}
# <</SYS>>
# Question: {question} [/INST]
# """
# prompt = PromptTemplate.from_template(template)
# 
# # Retrieval-based QA Chain
# qa_chain = None # RetrievalQA.from_chain_type(
# #     llm=llm,
# #     chain_type="stuff",
# #     retriever=db.as_retriever(search_kwargs={"k": 3}),
# #     chain_type_kwargs={"prompt": prompt},
# #     return_source_documents=True
# # )

# Prediction function
def prediction(image_path):
    image = Image.open(image_path).convert("RGB")
    image = image.resize((224, 224))
    input_data = TF.to_tensor(image).unsqueeze(0)
    with torch.no_grad():
        output = model(input_data)
    output = output.detach().numpy()
    index = np.argmax(output)
    return index

# Initialize Flask app
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('login_page.html')
# Routes
@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact-us.html')

@app.route('/index')
def ai_engine_page():
    return render_template('index.html')

@app.route('/mobile-device')
def mobile_device_detected_page():
    return render_template('mobile-device.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        image = request.files['image']
        filename = image.filename
        file_path = os.path.join('static/uploads', filename)
        image.save(file_path)
        pred = prediction(file_path)
        title = disease_info['disease_name'][pred]
        description = disease_info['description'][pred]
        prevent = disease_info['Possible Steps'][pred]
        image_url = disease_info['image_url'][pred]
        supplement_name = supplement_info['supplement name'][pred]
        supplement_image_url = supplement_info['supplement image'][pred]
        supplement_buy_link = supplement_info['buy link'][pred]
        return render_template('submit.html', title=title, desc=description, prevent=prevent,
                               image_url=image_url, pred=pred, sname=supplement_name,
                               simage=supplement_image_url, buy_link=supplement_buy_link)

@app.route('/market', methods=['GET', 'POST'])
def market():
    return render_template('market.html',
                           supplement_image=list(supplement_info['supplement image']),
                           supplement_name=list(supplement_info['supplement name']),
                           disease=list(disease_info['disease_name']),
                           buy=list(supplement_info['buy link']))

# Chatbot route
@app.route('/chat', methods=['POST'])
def chat_response():
    data = request.get_json()
    message = data.get('message', '').strip()

    if not message:
        return jsonify({"reply": "Please ask a valid question."})

    try:
        result = qa_chain.invoke({"query": message})
        reply = result['result']
        sources = [doc.metadata.get("source", "unknown") for doc in result["source_documents"]]
        return jsonify({"reply": reply, "sources": sources})
    except Exception as e:
        print("Error during chatbot response:", e)
        return jsonify({"reply": "Sorry, I encountered an error while processing your question."})

# Run Flask
if __name__ == '__main__':
    app.run(debug=True)

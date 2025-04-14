# MediQuery

MediQuery is an AI-powered symptom checker chatbot that helps users identify potential health conditions based on their described symptoms.

This project was developed during my internship at the **Applied Technologies for Learning in the Arts & Sciences (ATLAS)** at the **University of Illinois Urbana-Champaign**.

---

## Features

- Symptom extraction using a local LLM via [Ollama](https://ollama.com/) or Gemini API
- Disease matching from a local medical database
- Medical specialization mapping
- Nearby doctor recommendations based on ZIP code or city
- Web-based frontend with an interactive chat UI

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/sharmaaaryan4012/MediQuery
cd MediQuery
```

### 2. Install dependencies

Make sure you have Python 3 installed. Then install required packages:

```bash
pip install -r requirements.txt
```

### 3. Set up the database

- Download the required database file from the link below:  
  [Download MediQueryData.db](https://drive.google.com/file/d/1WwowTkYJjeIlwpS7GCc-vGF2VCwFgcF3/view?usp=sharing)

- Replace the placeholder `MediQueryData.db` inside the `data/` directory with the downloaded file.

### 4. Choose a Language Model Backend

You have **two options** for enabling the AI functionality in MediQuery:

#### Option 1: Use a local LLM via Ollama

- Download and install Ollama: https://ollama.com
- Pull a model of your choice (e.g., DeepSeek, LLaMA2, Mistral):

```bash
ollama pull deepseek
```

- Update the `MODEL_NAME` variable in `chatbotBackend.py` to match the model you pulled:

```python
MODEL_NAME = "deepseek-r1:8b"
```

Make sure the Ollama server is running in the background.

#### Option 2: Use Gemini via API Key

- Create a file named `api.env` in the root directory.
- Add your Gemini API key to it in the following format:

```
GEMINI_API_KEY=your_api_key_here
```

- The app will detect this environment variable and use Gemini for LLM responses.

---

## Running the App

Start the Flask development server:

```bash
python3 app.py
```

Then, open your browser and navigate to:

```
http://127.0.0.1:5000
```

You will see the MediQuery web interface, where you can enter symptoms, city, and ZIP code to receive diagnoses and doctor suggestions.

---

## Requirements

Dependencies are listed in `requirements.txt`.

---

## Notes

- This app uses a local SQLite database stored in `data/MediQueryData.db`.
- Ollama must be running in the background **if you’re using local LLMs**.
- If you’re using **Gemini**, only an API key is needed—no additional downloads.
- The doctor recommendation system queries a cleaned and structured healthcare provider database by specialization and location.

---

## Author

**Aaryan Sharma**  
Developed during ATLAS Internship, Spring 2025  
University of Illinois Urbana-Champaign

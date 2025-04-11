Here’s your complete, detailed `README.md` file content in Markdown format:

```markdown
# MediQuery

MediQuery is an AI-powered symptom checker chatbot that helps users identify potential health conditions based on their described symptoms.

This project was developed during my internship at the **Applied Technologies for Learning in the Arts & Sciences (ATLAS)** at the **University of Illinois Urbana-Champaign**.

---

## Features

- Symptom extraction using a local LLM via [Ollama](https://ollama.com/)
- Disease matching from a local medical database
- Medical specialization mapping
- Nearby doctor recommendations based on ZIP code or city
- Web-based frontend with an interactive chat UI

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd MediQuery
```

### 2. Create and activate a virtual environment (optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

Make sure you have Python 3 installed. Then install required packages:

```bash
pip install -r requirements.txt
```

### 4. Set up the database

- Download the required database file from the link below:  
  [Download MediQueryData.db](https://drive.google.com/file/d/1WwowTkYJjeIlwpS7GCc-vGF2VCwFgcF3/view?usp=sharing)

- Replace the placeholder `MediQueryData.db` inside the `data/` directory with the downloaded file.

### 5. Install and configure Ollama

- Download and install Ollama: https://ollama.com
- Pull any large language model (e.g., DeepSeek, LLaMA2, Mistral):

```bash
ollama pull deepseek
```

- Update the `MODEL_NAME` variable in `chatbotBackend.py` to match the name of the model you installed:

```python
MODEL_NAME = "deepseek-r1:8b"  # or any other local LLM name from Ollama
```

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
- Ollama must be running in the background for the LLM-based diagnosis features to work.
- The doctor recommendation system queries a cleaned and structured healthcare provider database by specialization and location.

---

## Author

**Aaryan Sharma**  
Developed during ATLAS Internship, Spring 2025  
University of Illinois Urbana-Champaign

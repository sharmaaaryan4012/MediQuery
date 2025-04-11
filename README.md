# MediQuery

MediQuery is an AI-powered symptom checker chatbot that helps users identify potential health conditions based on their described symptoms. It integrates a SQLite database of diseases and doctors, and returns nearby doctor suggestions based on the matched disease.

## Setup Instructions

1. Clone the repository.
2. Ensure all dependencies are installed (Flask, SQLite3, etc.).
3. Download the required database file from the link below:

   [Download database](https://drive.google.com/file/d/1WwowTkYJjeIlwpS7GCc-vGF2VCwFgcF3/view?usp=sharing)

4. Replace the placeholder "MediQueryData.db" file inside the `data/` directory with the downloaded database file.

## Usage

Run the Flask app locally:

```bash
python3 app.py

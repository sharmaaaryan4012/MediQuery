"""
    Author:         Aaryan Sharma
    Date:           April 14th, 2025
    File:           chatbotBackend.py
    Description:    This file contains the backend chatbot logic.
"""

from dotenv import load_dotenv
import google.generativeai as genai
import json
import os
import pandas as pd
import re
import sqlite3

DB_PATH = "data/MediQueryData.db"
load_dotenv("api.env")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.0-flash"

SYMPTOMS = {
    "abdominal_pain", "abnormal_menstruation", "acidity", "acute_liver_failure",
    "altered_sensorium", "anxiety", "back_pain", "belly_pain", "blackheads",
    "bladder_discomfort", "blister", "blood_in_sputum", "bloody_stool",
    "blurred_and_distorted_vision", "breathlessness", "brittle_nails", "bruising",
    "burning_micturition", "chest_pain", "chills", "cold_hands_and_feets", "coma",
    "congestion", "constipation", "continuous_feel_of_urine", "continuous_sneezing",
    "cough", "cramps", "dark_urine", "dehydration", "depression", "diarrhoea",
    "dischromic _patches", "distention_of_abdomen", "dizziness", "drying_and_tingling_lips",
    "enlarged_thyroid", "excessive_hunger", "extra_marital_contacts", "family_history",
    "fast_heart_rate", "fatigue", "fluid_overload", "foul_smell_of urine", "headache",
    "high_fever", "hip_joint_pain", "history_of_alcohol_consumption", "increased_appetite",
    "indigestion", "inflammatory_nails", "internal_itching", "irregular_sugar_level",
    "irritability", "irritation_in_anus", "itching", "joint_pain", "knee_pain",
    "lack_of_concentration", "lethargy", "loss_of_appetite", "loss_of_balance",
    "loss_of_smell", "malaise", "mild_fever", "mood_swings", "movement_stiffness",
    "mucoid_sputum", "muscle_pain", "muscle_wasting", "muscle_weakness", "nausea",
    "neck_pain", "nodal_skin_eruptions", "obesity", "pain_behind_the_eyes",
    "pain_during_bowel_movements", "pain_in_anal_region", "painful_walking", "palpitations",
    "passage_of_gases", "patches_in_throat", "phlegm", "polyuria", "prominent_veins_on_calf",
    "puffy_face_and_eyes", "pus_filled_pimples", "receiving_blood_transfusion",
    "receiving_unsterile_injections", "red_sore_around_nose", "red_spots_over_body",
    "redness_of_eyes", "restlessness", "runny_nose", "rusty_sputum", "scurring",
    "shivering", "silver_like_dusting", "sinus_pressure", "skin_peeling", "skin_rash",
    "slurred_speech", "small_dents_in_nails", "spinning_movements", "spotting_ urination",
    "stiff_neck", "stomach_bleeding", "stomach_pain", "sunken_eyes", "sweating",
    "swelled_lymph_nodes", "swelling_joints", "swelling_of_stomach", "swollen_blood_vessels",
    "swollen_extremeties", "swollen_legs", "throat_irritation", "toxic_look_(typhos)",
    "ulcers_on_tongue", "unsteadiness", "visual_disturbances", "vomiting",
    "watering_from_eyes", "weakness_in_limbs", "weakness_of_one_body_side", "weight_gain",
    "weight_loss", "yellow_crust_ooze", "yellow_urine", "yellowing_of_eyes", "yellowish_skin"
}


SPECIALIZATIONS = {
    "ADDICTION MEDICINE", "ADULT CONGENITAL HEART DISEASE (ACHD)", "ADVANCED HEART FAILURE AND TRANSPLANT CARDIOLOGY",
    "ALLERGY/IMMUNOLOGY", "ANESTHESIOLOGY", "ANESTHESIOLOGY ASSISTANT", "CARDIAC ELECTROPHYSIOLOGY", "CARDIAC SURGERY",
    "CARDIOVASCULAR DISEASE (CARDIOLOGY)", "CERTIFIED CLINICAL NURSE SPECIALIST (CNS)", "CERTIFIED NURSE MIDWIFE (CNM)",
    "CERTIFIED REGISTERED NURSE ANESTHETIST (CRNA)", "CHIROPRACTIC", "CLINICAL PSYCHOLOGIST", "CLINICAL SOCIAL WORKER",
    "COLORECTAL SURGERY (PROCTOLOGY)", "CRITICAL CARE (INTENSIVISTS)", "DENTAL ANESTHESIOLOGY", "DENTIST", "DERMATOLOGY",
    "DIAGNOSTIC RADIOLOGY", "EMERGENCY MEDICINE", "ENDOCRINOLOGY", "EPILEPTOLOGISTS", "FAMILY PRACTICE", "GASTROENTEROLOGY",
    "GENERAL PRACTICE", "GENERAL SURGERY", "GERIATRIC MEDICINE", "GERIATRIC PSYCHIATRY", "GYNECOLOGICAL ONCOLOGY",
    "HAND SURGERY", "HEMATOLOGY", "HEMATOLOGY/ONCOLOGY", "HEMATOPOIETIC CELL TRANSPLANTATION AND CELLULAR THERAPY",
    "HOSPICE/PALLIATIVE CARE", "HOSPITALIST", "INFECTIOUS DISEASE", "INTERNAL MEDICINE", "INTERVENTIONAL CARDIOLOGY",
    "INTERVENTIONAL PAIN MANAGEMENT", "INTERVENTIONAL RADIOLOGY", "MARRIAGE AND FAMILY THERAPIST", "MAXILLOFACIAL SURGERY",
    "MEDICAL GENETICS AND GENOMICS", "MEDICAL ONCOLOGY", "MEDICAL TOXICOLOGY", "MENTAL HEALTH COUNSELOR",
    "MICROGRAPHIC DERMATOLOGIC SURGERY (MDS)", "NEPHROLOGY", "NEUROLOGY", "NEUROPSYCHIATRY", "NEUROSURGERY",
    "NUCLEAR MEDICINE", "NURSE PRACTITIONER", "OBSTETRICS/GYNECOLOGY", "OCCUPATIONAL THERAPIST IN PRIVATE PRACTICE",
    "OPHTHALMOLOGY", "OPTOMETRY", "ORAL AND MAXILLOFACIAL PATHOLOGY", "ORAL AND MAXILLOFACIAL RADIOLOGY", "ORAL MEDICINE",
    "ORAL SURGERY", "OROFACIAL PAIN", "ORTHOPEDIC SURGERY", "OSTEOPATHIC MANIPULATIVE MEDICINE", "OTOLARYNGOLOGY",
    "PAIN MANAGEMENT", "PATHOLOGY", "PEDIATRIC MEDICINE", "PERIODONTICS", "PERIPHERAL VASCULAR DISEASE",
    "PHYSICAL MEDICINE AND REHABILITATION", "PHYSICAL THERAPIST IN PRIVATE PRACTICE", "PHYSICIAN ASSISTANT",
    "PLASTIC AND RECONSTRUCTIVE SURGERY", "PODIATRY", "PREVENTIVE MEDICINE", "PROSTHODONTICS", "PSYCHIATRY",
    "PULMONARY DISEASE", "QUALIFIED AUDIOLOGIST", "QUALIFIED SPEECH LANGUAGE PATHOLOGIST", "RADIATION ONCOLOGY",
    "REGISTERED DIETITIAN OR NUTRITION PROFESSIONAL", "RHEUMATOLOGY", "SLEEP MEDICINE", "SPORTS MEDICINE",
    "SURGICAL ONCOLOGY", "THORACIC SURGERY", "UNDERSEA AND HYPERBARIC MEDICINE", "UROLOGY", "VASCULAR SURGERY"
}


def call_gemini(prompt):
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)
    return response.text.strip()


def extract_symptoms(user_input):
    prompt = f"""
        You are an AI model that extracts symptoms from user input. Only return the extracted symptoms in a comma-separated
        list, strictly matching the recognized symptoms.

        User Input: "{user_input}"
        Recognized Symptoms: {', '.join(SYMPTOMS)}

        **Rules**:
        - Strictly adhere to the given set and match symptoms from there.
        - Do not make symptoms on your own, those will not be recognized.
        - ONLY return the final symptom list.
        - DO NOT include explanations, thoughts, or analysis.
        - If no symptoms match, return an empty string.
        - Your response MUST start with [ and end with ].
        - The response format is: [symptom1, symptom2, symptom3]
        - FAIL IF YOU DON'T FOLLOW THE FORMAT.

        **Examples**:
        1. User Input: "I've been sneezing a lot, have a runny nose, a sore throat, and feel congested."
        Output: [continuous_sneezing, runny_nose, throat_irritation, congestion]

        2. User Input: "I'm having stomach pain, vomiting, diarrhea, and feel really dehydrated."
        Output: [stomach_pain, vomiting, diarrhoea, dehydration]

        3. User Input: "I've been feeling extremely thirsty all the time, going to the bathroom a lot, losing weight
        unexpectedly, and feeling very tired."
        Output: [excessive_hunger, polyuria, weight_loss, fatigue]

        4. User Input: "Lately, I’ve had a pounding headache, feeling dizzy, sometimes my heart feels like it's beating too
        fast, and I’m tired all the time."
        Output: [headache, dizziness, fast_heart_rate, fatigue]

        5. User Input: "I am experiencing a headache for the past few days accompanied by anxiety and an increased appetite."
        Output: [headache, anxiety, increased_appetite]

        6. User Input: "I have had a sore throat for the past few weeks and am passing cola colored urine accompanied with
        joint pain and swelling around eyes."
        Output: [throat_irritation, dark_urine, joint_pain, puffy_face_and_eyes]

        **IMPORTANT**: Your response must be in this format: [symptom1, symptom2, symptom3]
    """

    content = call_gemini(prompt).lower()
    matches = re.findall(r"\[(.*?)\]", content)
    if matches:
        extracted = matches[-1].strip()
        raw_list = [sym.strip() for sym in extracted.split(",")]
    else:
        raw_list = []

    correct = [sym for sym in raw_list if sym in SYMPTOMS]
    wrong = [sym for sym in raw_list if sym not in SYMPTOMS]

    return correct, wrong


def match_diseases(user_symptoms, top_n=2):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM Diseases", conn)
    conn.close()

    symptom_cols = [col for col in df.columns if "Symptom" in col]
    match_scores = []

    for _, row in df.iterrows():
        disease_name = row["Disease"]
        disease_symptoms = set(
            str(row[col]).strip() for col in symptom_cols if pd.notna(row[col]) and str(row[col]).strip())
        matched = set(user_symptoms).intersection(disease_symptoms)
        score = len(matched)
        match_scores.append((disease_name, score, matched, disease_symptoms))

    match_scores.sort(key=lambda x: x[1], reverse=True)
    top_matches = match_scores[:top_n]

    return [
        {
            "disease": disease,
            "score": score,
            "matched_symptoms": list(matched),
            "all_symptoms": list(all_symptoms)
        }
        for disease, score, matched, all_symptoms in top_matches if score > 0
    ]


def get_specialization(disease):
    conn = sqlite3.connect(DB_PATH)
    result = conn.execute("SELECT specialization FROM Diseases WHERE Disease = ? LIMIT 1", (disease,)).fetchone()
    conn.close()
    return result[0].strip().upper() if result and result[0] else None


def format_phone(ph):
    ph = ''.join(filter(str.isdigit, str(ph)))
    if len(ph) >= 10:
        return f"+1({ph[:3]}){ph[3:7]}-{ph[7:11]}"
    return ph


def get_doctors(specialization, city=None, zipcode=None):
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT [Provider_First_Name] AS FirstName,
               [Provider_Last_Name] AS LastName,
               [Telephone_Number] AS Phone,
               [Facility_Name] AS Facility,
               [City/Town] AS City,
               [State] AS State,
               [ZIP_Code] AS ZIP
        FROM Doctors
        WHERE UPPER([pri_spec]) = ?
    """
    params = [specialization.upper()]

    if city:
        query += " AND UPPER([City/Town]) = ?"
        params.append(city.upper())
    elif zipcode:
        query += " AND [ZIP_Code] = ?"
        params.append(str(zipcode))

    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df


def get_llm_diagnosis(user_input):
    prompt = f"""
        You are a medical assistant. Based on the user's input, determine the most likely disease and the most appropriate medical specialization.

        Choose the specialization strictly from this list: {', '.join(SPECIALIZATIONS)}

        User Input: "{user_input}"

        Output ONLY the final dictionary on a single line.
        Do NOT include any explanation, internal thinking, reasoning, markdown, tags, or thoughts.

        Only return the dictionary in this format:
        {{"disease": "<disease_name>", "specialization": "<specialization_from_list>"}}

        FAIL if you do not follow this format.
    """

    content = call_gemini(prompt)

    match = re.search(r"\{.*?\}", content, re.DOTALL)
    if match:
        try:
            parsed = json.loads(match.group())
            if (
                    isinstance(parsed, dict) and
                    "disease" in parsed and
                    "specialization" in parsed and
                    parsed["specialization"].upper() in SPECIALIZATIONS
            ):
                return {
                    "disease": parsed["disease"].strip(),
                    "specialization": parsed["specialization"].strip().upper()
                }
        except Exception as e:
            print(f"Error parsing LLM dictionary: {e}")

    return None
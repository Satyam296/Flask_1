import google.generativeai as genai
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Your existing SUBJECT_DESCRIPTIONS dictionary
SUBJECT_DESCRIPTIONS = {
    "Mathematics": "Questions related to mathematical concepts, problem-solving, logical reasoning, numerical analysis, and mathematical reasoning.",
    "Science": "Inquiries about natural phenomena, scientific principles, experimental methods, scientific theories, and understanding the physical and natural world.",
    "History": "Questions exploring past events, civilizations, historical periods, cultural developments, and historical analysis and interpretation.",
    "Geography": "Queries about physical landscapes, human geography, environmental systems, global patterns, and spatial relationships.",
    "English": "Topics involving language use, literature analysis, writing skills, comprehension, linguistic structures, and communication.",
    "Computer Science": "Questions about computational thinking, programming concepts, technology, algorithmic problem-solving, and digital systems."
}

# Configure Gemini API
GOOGLE_API_KEY = "AIzaSyB7rmrMrhCUgVQjJly7fzYv9ZplZFEmrWI"
genai.configure(api_key=GOOGLE_API_KEY)


def is_subject_relevant(question, subject):
    relevance_prompt = f"""
    Determine if the following question is related to {subject}. 
    Context for {subject}: {SUBJECT_DESCRIPTIONS[subject]}
    
    Question: "{question}"
    
    Respond with ONLY 'YES' or 'NO'. 
    """
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(relevance_prompt)
    return "YES" in response.text.upper().strip()


def get_gemini_response(question, subject):
    contextual_prompt = f"""
    Provide a comprehensive answer to the following question, 
    ensuring the response is appropriately scoped to {subject}:
    
    {question}
    
    Context for {subject}: {SUBJECT_DESCRIPTIONS[subject]}
    """
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(contextual_prompt)
    return response.text


@app.route("/get_answer", methods=["POST"])
def get_answer():
    data = request.get_json()
    subject = data.get("subject")
    question = data.get("question")

    if not subject or not question:
        return jsonify({"error": "Subject and question are required"}), 400

    if subject not in SUBJECT_DESCRIPTIONS:
        return jsonify({"error": "Invalid subject"}), 400

    if is_subject_relevant(question, subject):
        response = get_gemini_response(question, subject)
        return jsonify({"answer": response})
    else:
        return jsonify({"error": f"The question does not seem to relate to {subject}. Please check and try again."}), 400


if __name__ == "__main__":
    app.run(debug=True)
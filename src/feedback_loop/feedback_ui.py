import json

def load_key_terms(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_feedback(feedback_data, file_path):
    with open(file_path, 'w') as file:
        json.dump(feedback_data, file, indent=4)

def label_terms(terms):
    feedback = {}
    for term in terms:
        print(f"\nTerm: {term}")
        print("Labels: green, yellow, red, uncertain, high-priority")
        label = input("Enter label: ").strip().lower()
        while label not in ['green', 'yellow', 'red', 'uncertain', 'high-priority']:
            print("Invalid label. Please choose from: green, yellow, red, uncertain, high-priority.")
            label = input("Enter label: ").strip().lower()
        feedback[term] = label
    return feedback
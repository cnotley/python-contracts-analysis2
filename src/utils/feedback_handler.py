class FeedbackHandler:
    def __init__(self):
        self.feedback_data = {'green': set(), 'yellow': set(), 'red': set(), 'uncertain': set(), 'high-priority': set()}

    def update_feedback(self, new_feedback):
        for term, label in new_feedback.items():
            if label in self.feedback_data:
                self.feedback_data[label].add(term)

    def adjust_prompt(self, prompt):
        red_terms = ' '.join(self.feedback_data['red'])
        green_terms = ' '.join(self.feedback_data['green'])
        high_priority_terms = ' '.join(self.feedback_data['high-priority'])
        uncertain_terms = ' '.join(self.feedback_data['uncertain'])

        adjusted_prompt = prompt + "\n\n"
        if green_terms:
            adjusted_prompt += f"Focus on terms similar to: {green_terms}.\n"
        if red_terms:
            adjusted_prompt += f"Avoid terms similar to: {red_terms}.\n"
        if high_priority_terms:
            adjusted_prompt += f"Prioritize terms similar to: {high_priority_terms}.\n"
        if uncertain_terms:
            adjusted_prompt += f"Review uncertain terms: {uncertain_terms}.\n"

        return adjusted_prompt

    def categorize_feedback(self):
        return {
            'important': self.feedback_data['green'],
            'moderate': self.feedback_data['yellow'],
            'irrelevant': self.feedback_data['red'],
            'uncertain': self.feedback_data['uncertain'],
            'high-priority': self.feedback_data['high-priority']
        }
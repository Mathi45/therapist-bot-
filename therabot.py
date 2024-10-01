import streamlit as st
import nltk
from nltk.tokenize import word_tokenize
import google.generativeai as genai

class PsychologicalChatbot:
    def __init__(self):
        self.name = ""
        self.age = ""
        self.responses = []

    def get_basic_info(self):
        st.title("Psychological Chatbot")
        st.write("Welcome to the Psychological Chatbot!\nPlease provide the following basic information:")
        self.get_name()

    def get_name(self):
        self.name = st.text_input("Name:")
        if self.name:
            st.write(f"Hello {self.name}! Let's proceed.")
            self.get_age()

    def get_age(self):
        self.age = st.text_input("Age:")
        if self.age:
            st.write(f"Thanks, {self.name}. Let's continue.")
            self.ask_question(0)

    def ask_question(self, question_index):
        question = questions[question_index]
        options = answer_options[question_index]
        st.write(question)
        for idx, option in enumerate(options):
            st.write(f"{idx+1}. {option}")
        response = st.radio("Enter your choice:", options)
        self.on_response_given(response, question_index)

    def on_response_given(self, response, question_index):
        options = answer_options[question_index]
        try:
            response_index = int(response[0]) - 1
            selected_option = options[response_index]
            self.responses.append(selected_option)
            question_index += 1
            if question_index < len(questions):
                self.ask_question(question_index)
            else:
                self.analyze_responses()
        except ValueError:
            st.error("Invalid input. Please select a valid option.")
            self.ask_question(question_index)

    def analyze_responses(self):
        analyzer = PsychologicalAnalyzer(self.responses)
        identified_issues = analyzer.analyze()
        for issue in identified_issues:
            self.handle_issue(issue)

    def handle_issue(self, issue):
        if issue == "stress":
            stress_handler = StressHandler()
            stress_handler.provide_counseling()
            stress_handler.suggest_activities()
        elif issue == "anxiety":
            anxiety_handler = AnxietyHandler()
            anxiety_handler.provide_counseling()
            anxiety_handler.suggest_activities()
        elif issue == "depression":
            depression_handler = DepressionHandler()
            depression_handler.provide_counseling()
            depression_handler.suggest_activities()
        else:
            # If issue not handled locally, call API chatbot
            self.call_api_chatbot(issue)

    def call_api_chatbot(self, issue):
        response = genai.chat.send_message(issue)
        st.write(f"API BOT: {response.text}")

questions = [
    "Gender",
    "Educational qualification",
    "Employment status",
    "Relationship status",
    "How's your day been?",
    "Any new hobbies?",
    "Favorite way to unwind?",
    "Any upcoming plans?",
    "Feeling energized?",
    "Handling setbacks?",
    "Sleeping well?",
    "Staying focused?",
    "Enjoy socializing?",
    "Any appetite changes?"
]

answer_options = [
    ["Male", "Female", "Other"],
    ["School", "Higher education", "Graduated"],
    ["Employed", "Unemployed", "Student"],
    ["Married", "Unmarried", "Divorced"],
    ["Great!", "Not bad.", "Rough."],
    ["Yes!", "No, same old.", "Not interested."],
    ["Reading/watching TV.", "Walking/exercising.", "Hard to relax."],
    ["Yes, exciting!", "Taking it day by day.", "Nothing to look forward to."],
    ["Yes, very.", "Bit drained.", "Low energy."],
    ["Stay positive.", "Assess then react.", "Feel overwhelmed."],
    ["Yes, feeling rested.", "Disrupted sleep.", "Trouble sleeping."],
    ["Yes, very.", "Bit distracted.", "Hard to focus."],
    ["Love it!", "Enjoy but draining.", "Prefer solitude."],
    ["No, normal.", "Some changes.", "Significant change."]
]

class PsychologicalAnalyzer:
    def __init__(self, responses):
        self.responses = responses

    def analyze(self):
        stress_keywords = ['rough', 'drained', 'overwhelmed', 'disrupted sleep']
        depression_keywords = ['not interested', 'hard to relax', 'nothing to look forward to', 'low energy', 'solitude']
        anxiety_keywords = ['overwhelmed', 'distracted', 'hard to focus', 'trouble sleeping', 'solitude']

        response_tokens = word_tokenize(' '.join(self.responses).lower())

        stress_count = sum(keyword in response_tokens for keyword in stress_keywords)
        depression_count = sum(keyword in response_tokens for keyword in depression_keywords)
        anxiety_count = sum(keyword in response_tokens for keyword in anxiety_keywords)

        psychological_issues = []

        if stress_count > anxiety_count and stress_count > depression_count:
            stress_handler = StressHandler()
            stress_handler.provide_counseling()
            stress_handler.suggest_activities()
            psychological_issues.append("stress")

        if anxiety_count > stress_count and anxiety_count > depression_count:
            anxiety_handler = AnxietyHandler()
            anxiety_handler.provide_counseling()
            anxiety_handler.suggest_activities()
            psychological_issues.append("anxiety")

        if depression_count > stress_count and depression_count > anxiety_count:
            depression_handler = DepressionHandler()
            depression_handler.provide_counseling()
            depression_handler.suggest_activities()
            psychological_issues.append("depression")

        return psychological_issues

    def call_api_chatbot(self, issue):
        # Send the issue to the API chatbot
        response = genai.chat.send_message(issue)
        st.write(f"API BOT: {response.text}")

        # Continuously interact with the API chatbot until the session ends
        while True:
            user_input = st.text_input("YOU:")
            if not user_input.strip():
                break

            # Send user input to the API chatbot
            response = genai.chat.send_message(user_input)
            st.write(f"API BOT: {response.text}")

class StressHandler:
    def provide_counseling(self):
        st.write("It seems like you're dealing with stress. It's important to find healthy ways to manage stress, such as exercise, meditation, or talking to someone you trust.")

    def suggest_activities(self):
        st.write("Here are some activities you can try to alleviate stress:")
        st.write("- Practice deep breathing exercises")
        st.write("- Go for a walk in nature")
        st.write("- Listen to calming music")
        st.write("- Journal about your feelings")

class AnxietyHandler:
    def provide_counseling(self):
        st.write("It seems like you're dealing with anxiety. It's important to practice relaxation techniques and consider seeking support from a therapist.")

    def suggest_activities(self):
        st.write("Here are some activities you can try to alleviate anxiety:")
        st.write("- Practice mindfulness meditation")
        st.write("- Engage in regular physical activity")
        st.write("- Challenge negative thoughts with positive affirmations")
        st.write("- Spend time with supportive friends or family members")

class DepressionHandler:
    def provide_counseling(self):
        st.write("It sounds like you may be experiencing depression. Remember that it's okay to ask for help. Consider talking to a therapist or counselor about how you're feeling.")

    def suggest_activities(self):
        st.write("Here are some activities you can try to alleviate depression:")
        st.write("- Engage in regular exercise to boost endorphin levels")
        st.write("- Establish a daily routine to provide structure")
        st.write("- Connect with loved ones for social support")
        st.write("- Set small, achievable goals to regain a sense of accomplishment")

def provide_counseling(input_text):
    # Analyze the input_text to identify psychological issues
    # For simplicity, let's assume we're looking for keywords indicating common issues
    psychological_issues = ["anxiety", "depression", "stress", "loneliness"]

    for issue in psychological_issues:
        if issue in input_text.lower():
            return f"It seems like you're dealing with {issue}. It's important to address these feelings. Would you like to talk more about it?"

    return None

def main():
    chatbot = PsychologicalChatbot()
    chatbot.get_basic_info()

    API_KEY = "AIzaSyBrnxplbFtZZLwQaaKYNt1NcvHFqnv50Ww"
    genai.configure(api_key=API_KEY)

    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])

    while True:
        user_input = st.text_input("YOU:")
        if not user_input.strip():
            break

        counseling_response = provide_counseling(user_input)
        if counseling_response:
            st.write(f"BOT: {counseling_response}")
        else:
            response = chat.send_message(user_input)
            st.write(f"BOT: {response.text}")

if __name__ == "__main__":
    main()
streamlit run your_script.py
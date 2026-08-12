import speech_recognition as sr
import pyttsx3
from datetime import datetime
import webbrowser

from intent import detect_intent
from reminder import set_reminder, get_pending_reminders
from reminder_parser import extract_duration
from weather import get_weather
from weather_parser import extract_city
from email_sender import send_email
from email_parser import extract_email_details
from qa import answer_question
from custom_commands import execute_custom_command


class VoiceAssistant:

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.operation_timeout = 10
        self.engine = pyttsx3.init()

    def speak(self, text):
        print("Assistant:", text)
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        print("\nListening...")

        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.5
                )

                print("Speak now...")

                audio = self.recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=7
                )

        except sr.WaitTimeoutError:
            print("No speech detected.")
            return ""

        except Exception as e:
            print("Microphone error:", e)
            return ""

        try:
            print("Processing speech...")

            text = self.recognizer.recognize_google(
                audio,
                language="en-IN"
            )

            print("You said:", text)
            return text.lower()

        except sr.UnknownValueError:
            print("Could not understand the audio.")
            return ""

        except sr.RequestError as e:
            print("Speech recognition error:", e)
            self.speak(
                "I am unable to connect to the speech recognition service."
            )
            return ""

        except Exception as e:
            print("Unexpected recognition error:", e)
            return ""

    def process_command(self, command):

        intent = detect_intent(command)

        print("Detected intent:", intent)

        if intent == "GREETING":

            self.speak(
                "Hello! How can I help you?"
            )

        elif intent == "GET_TIME":

            current_time = datetime.now().strftime(
                "%I:%M %p"
            )

            self.speak(
                f"The current time is {current_time}"
            )

        elif intent == "GET_DATE":

            current_date = datetime.now().strftime(
                "%d %B %Y"
            )

            self.speak(
                f"Today's date is {current_date}"
            )

        elif intent == "WEATHER":

            city = extract_city(command)

            if city:

                self.speak(
                    f"Let me check the weather in {city}."
                )

                weather_result = get_weather(city)

                self.speak(weather_result)

            else:

                self.speak(
                    "Which city would you like the weather for?"
                )

        elif intent == "SEND_EMAIL":

            receiver, message = extract_email_details(
                command
            )

            if receiver and message:

                self.speak(
                    f"Sending an email to {receiver}."
                )

                result = send_email(
                    receiver,
                    "Voice Assistant Email",
                    message
                )

                self.speak(result)

            elif receiver:

                self.speak(
                    "What message would you like me to send?"
                )

                email_message = self.listen()

                if email_message:

                    result = send_email(
                        receiver,
                        "Voice Assistant Email",
                        email_message
                    )

                    self.speak(result)

                else:

                    self.speak(
                        "I could not understand the message."
                    )

            else:

                self.speak(
                    "Sure. What email address should I send it to?"
                )

                receiver_command = self.listen()

                receiver, _ = extract_email_details(
                    receiver_command
                )

                if receiver:

                    self.speak(
                        "What message would you like me to send?"
                    )

                    email_message = self.listen()

                    if email_message:

                        result = send_email(
                            receiver,
                            "Voice Assistant Email",
                            email_message
                        )

                        self.speak(result)

                    else:

                        self.speak(
                            "I could not understand the message."
                        )

                else:

                    self.speak(
                        "I could not find a valid email address."
                    )

        elif intent == "QUESTION":

            self.speak(
                "Let me find the answer to that."
            )

            answer = answer_question(command)

            self.speak(answer)

        elif intent == "WEB_SEARCH":

            search_query = command

            search_phrases = [
                "please search for",
                "please search",
                "search for",
                "search",
                "look up",
                "can you search for",
                "can you search"
            ]

            for phrase in search_phrases:

                if phrase in search_query:

                    search_query = search_query.replace(
                        phrase,
                        ""
                    )

            search_query = search_query.strip()

            if search_query:

                self.speak(
                    f"Searching for {search_query}"
                )

                webbrowser.open(
                    "https://www.google.com/search?q="
                    + search_query.replace(" ", "+")
                )

            else:

                self.speak(
                    "What would you like me to search for?"
                )

        elif intent == "SET_REMINDER":

            duration = extract_duration(command)

            if duration is not None:

                if duration < 60:

                    time_text = f"{duration} seconds"

                elif duration < 3600:

                    minutes = duration // 60
                    time_text = f"{minutes} minutes"

                else:

                    hours = duration // 3600
                    time_text = f"{hours} hours"

                self.speak(
                    f"Okay, I will remind you in {time_text}."
                )

                set_reminder(duration)

            else:

                self.speak(
                    "I could not understand the reminder duration."
                )

        elif intent == "EXIT":

            self.speak(
                "Goodbye! Have a great day."
            )

            return False

        else:

            if execute_custom_command(command):

                self.speak(
                    "Custom command executed successfully."
                )

            else:

                self.speak(
                    "Sorry, I don't understand that command yet."
                )
        return True

    def run(self):

        self.speak(
            "Voice assistant started. How can I help you?"
        )

        while True:

            reminders = get_pending_reminders()

            for reminder in reminders:

                self.speak(reminder)

            command = self.listen()

            if command:

                should_continue = self.process_command(
                    command
                )

                if not should_continue:

                    break
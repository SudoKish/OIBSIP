import speech_recognition as sr


recognizer = sr.Recognizer()
recognizer.operation_timeout = 10

print("Starting microphone test...")

with sr.Microphone() as source:

    print("Adjusting microphone...")
    recognizer.adjust_for_ambient_noise(
        source,
        duration=1
    )

    print("Speak something...")

    audio = recognizer.listen(
        source,
        timeout=5,
        phrase_time_limit=7
    )

print("Audio captured.")
print("Sending audio to Google...")

try:

    text = recognizer.recognize_google(
        audio,
        language="en-IN"
    )

    print("You said:", text)

except sr.UnknownValueError:

    print("Google could not understand the audio.")

except sr.RequestError as e:

    print("Google Speech Recognition error:")
    print(e)

except Exception as e:

    print("Unexpected error:")
    print(e)
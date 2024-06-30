import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import threading

# Initialize the pyttsx3 engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
# Set the voice property to the second voice in the list
engine.setProperty("voice", voices[1].id)

# Function to take voice command from the user
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1.0  # Adjust as needed
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        print("Please say that again...")
        return "None"
    return query.lower()

# Function to speak a given text
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to wish the user based on the current time
def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning")
    elif 12 <= hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    speak("Hello sir! I am GodAI, how may I help you?")

# Function to search Wikipedia
def searchWikipedia(query):
    speak("Searching Wikipedia...")
    query = query.replace("wikipedia", "")
    results = wikipedia.summary(query, sentences=2)
    print(results)
    speak(results)

# Function to open websites based on query
def openWebsite(query):
    if "youtube" in query:
        webbrowser.open("https://www.youtube.com")
    elif "google" in query:
        webbrowser.open("https://www.google.com")
    elif "instagram" in query:
        webbrowser.open("https://www.instagram.com")
    elif "code" in query:
        codePath = "C:\\Users\\YourUsername\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        os.startfile(codePath)

# Function to send email asynchronously
def sendEmail(to, content):
    def send():
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login("shahmann232@gmail.com", "njjqzdbgoslyxhiz")
            server.sendmail("shahmann232@gmail.com", to, content)
            server.close()
            speak("Email sent successfully")
        except Exception as e:
            print(e)
            speak("Sorry, I couldn't send the email.")

    thread = threading.Thread(target=send)
    thread.start()

if __name__ == '__main__':
    wishMe()
    while True:
        query = takeCommand()

        if 'wikipedia' in query:
            searchWikipedia(query)

        elif "open" in query:
            openWebsite(query)

        elif "send email" in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                speak("Please enter the email address you want to send the mail to")
                to = input("Enter email address: ")
                sendEmail(to, content)
            except Exception as e:
                print(e)
                speak("Sorry, I couldn't send the email.")

        elif "exit" in query or "bye" in query:
            speak("Goodbye!")
            break

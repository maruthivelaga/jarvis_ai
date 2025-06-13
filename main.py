from core.listener import listen
from core.speaker import speak
from core.brain import ask_gpt
from datetime import datetime
import subprocess
import os
import webbrowser

def offline_reply(command):
    command = command.lower()

    if "your name" in command:
        return "I am Jarvis, your personal assistant."
    elif "who made you" in command:
        return "I was developed by my creator using Python."
    elif "how are you" in command:
        return "I'm functioning at full capacity!"
    elif "thank you" in command:
        return "You're welcome!"
    else:
        return "I'm sorry, I don't know how to handle that yet."
# Function to execute NirCmd commands
def execute_nircmd(command):
    path = "C:\\Program Files\\nircmd\\nircmd.exe"  # Update to your actual path
    try:
        if command == "unmute volume":
            subprocess.run([path, "mutesysvolume", "0"])
            return "Volume muted."
        elif command == "mute volume":
            subprocess.run([path, "mutesysvolume", "1   "])
            return "Volume unmuted"
        elif command == "increase volume":
            subprocess.run([path, "changesysvolume", "9876"])  # ~10% up
            return "Volume increased."
        elif  command == "volume down":
            subprocess.run([path, "changesysvolume", "-6553"])  # ~10% down
            return "Volume decreased."
        elif command == "shutdown":
            subprocess.run([path, "exitwin", "poweroff"])
            return "Shutting down the system."
        elif command == "restart":
             subprocess.run([path, "exitwin", "reboot"])
             return "Restarting the system."
        elif command == "log off":
            subprocess.run([path, "exitwin", "logoff"])
            return "Logging off."
        elif command == "open notepad":
            subprocess.run([path, "exec", "notepad.exe"])
            return "Opening Notepad."
        elif command == "open chrome":
            subprocess.run([path, "exec", "chrome.exe"])  # Ensure Chrome is in PATH or give full path
            return "Opening Chrome."
        elif command == "turn off monitor":
            subprocess.run([path, "monitor", "off"])
            return "Turning off the monitor."
        elif command.startswith("kill "):
            app = command.replace("kill ", "").strip()
            subprocess.run([path, "killprocess", f"{app}.exe"])
            return f"Killing process: {app}"
        else:
            return offline_reply(command)
        
    except Exception as e:
        return f"Error controlling volume: {e}"
def main():
    speak("Jarvis is now running. Say 'Jarvis' to wake me up.")

    while True: 
        try:
            print("🎙️ Listening for wake word...")
            wake_text = listen().lower()
            print(f"Wake word: {wake_text}")

            if "jarvis" in wake_text:
                speak("Yes? I’m listening.")

                while True:  # This stays active until you say "stop" or "sleep"
                    command = listen().lower()
                    print(f"🗣️ You said: {command}")

                    if not command:
                        speak("Sorry, I didn’t catch that.")
                        continue

                    if "stop" in command or "sleep" in command:
                        speak("Okay, going to sleep. Call me if you need me.")
                        break  # This breaks the inner loop and returns to wake word mode

                    # Handle system commands
                    elif "unmute volume" in command:
                        speak(execute_nircmd("unmute volume"))
                    elif "mute volume" in command:
                        speak(execute_nircmd("mute volume"))
                    elif "increase volume" in command or "volume up" in command:
                         speak(execute_nircmd("increase volume"))
                    elif "volume down" in command or "decrease volume" in command:
                        speak(execute_nircmd("volume down"))
                    elif "open website" in command:
                        url = command.split("open website")[-1].strip()
                        speak(execute_nircmd(f'exec show "{url}"'))
                    elif "turn off monitor" in command:
                        speak(execute_nircmd("turn off monitor"))
                    elif "open chrome" in command:
                         speak(execute_nircmd("open chrome"))
                    elif "open notepad" in command:
                        speak(execute_nircmd("open notepad"))
                    elif "shutdown" in command:
                        speak(execute_nircmd("shut down"))
 
                    # Handle other queries like time, date, weather, etc.
                    elif "time" in command:
                        now = datetime.now().strftime("%I:%M %p")
                        speak(f"The current time is {now}")
                    elif "date" in command:
                        today = datetime.now().strftime("%B %d, %Y")
                        speak(f"Today's date is {today}")
                    elif "weather" in command:
                        speak("Weather feature is coming soon!")
                    elif "your name" in command:
                        speak(offline_reply("your name"))
                    elif "who made you" in command:
                        speak(offline_reply("who made you"))
                    elif "how are you" in command:
                        speak(offline_reply("how are you"))
                    elif "thank you" in command:
                        speak(offline_reply("thank you"))

                    else:
                        try:
                            ai_reply = ask_gpt(command)
                            speak(ai_reply)
                        except Exception as e:
                            print(f"GPT error: {e}")
                            speak("Sorry, I’m having trouble accessing AI features right now.")

        except KeyboardInterrupt:
            print("🛑 Exiting...")
            break

        except Exception as e:
            print(f"❗ Error in main loop: {e}")
            speak("Something went wrong. Restarting listener.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error occurred: {e}")

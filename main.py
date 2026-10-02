import json
import os
import datetime
import webbrowser
import re


MEMORY_FILE = "memory.json"


# -----------------------------
# MEMORY
# -----------------------------

def load_memory():

    try:
        with open(MEMORY_FILE, "r") as file:
            data = json.load(file)

            # Make sure memory has the expected structure
            if "facts" not in data:
                data["facts"] = {}

            if "notes" not in data:
                data["notes"] = []

            return data

    except (FileNotFoundError, json.JSONDecodeError):

        return {
            "facts": {},
            "notes": []
        }


def save_memory(memory):

    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)


# -----------------------------
# CALCULATOR
# -----------------------------

def calculate(expression):

    try:

        # Only allow basic mathematical characters
        if not re.fullmatch(r"[0-9+\-*/(). %]+", expression):
            return "I can only calculate basic mathematics for now."

        result = eval(
            expression,
            {"__builtins__": None},
            {}
        )

        return result

    except:

        return "I couldn't calculate that."


# -----------------------------
# TIME
# -----------------------------

def tell_time():

    current_time = datetime.datetime.now()

    return current_time.strftime("%I:%M %p")


# -----------------------------
# MEMORY COMMANDS
# -----------------------------

def remember_fact(command, memory):

    patterns = [
        r"remember that (.+?) is (.+)",
        r"remember (.+?) is (.+)",
        r"my (.+?) is (.+)"
    ]

    for pattern in patterns:

        match = re.search(pattern, command)

        if match:

            key = match.group(1).strip()
            value = match.group(2).strip()

            memory["facts"][key] = value

            save_memory(memory)

            return f"I'll remember that {key} is {value}."

    return None


def recall_memory(command, memory):

    for key, value in memory["facts"].items():

        if key.lower() in command.lower():

            return f"You told me that {key} is {value}."

    return None


# -----------------------------
# NOTES
# -----------------------------

def add_note(command, memory):

    patterns = [
        r"make a note that (.+)",
        r"add a note (.+)",
        r"note that (.+)"
    ]

    for pattern in patterns:

        match = re.search(pattern, command)

        if match:

            note = match.group(1).strip()

            memory["notes"].append(note)

            save_memory(memory)

            return f"Note saved: {note}"

    return None


def show_notes(memory):

    notes = memory["notes"]

    if not notes:

        return "You don't have any notes yet."

    result = "Here are your notes:\n"

    for i, note in enumerate(notes, start=1):

        result += f"{i}. {note}\n"

    return result


# -----------------------------
# WEB
# -----------------------------

def search_web(command):

    query = command.replace("search", "", 1).strip()

    if not query:

        return "What should I search for?"

    url = "https://www.google.com/search?q=" + query.replace(" ", "+")

    webbrowser.open(url)

    return f"Searching Google for {query}."


# -----------------------------
# OPEN WEBSITES
# -----------------------------

def open_website(command):

    if "youtube" in command:

        webbrowser.open("https://www.youtube.com")

        return "Opening YouTube."

    if "google" in command:

        webbrowser.open("https://www.google.com")

        return "Opening Google."

    if "github" in command:

        webbrowser.open("https://github.com")

        return "Opening GitHub."

    return None


# -----------------------------
# JARVIS BRAIN
# -----------------------------

def process_command(command, memory):

    command = command.lower().strip()

    # EXIT

    if command in [
        "exit",
        "quit",
        "bye",
        "goodbye",
        "shutdown"
    ]:

        return "EXIT"


    # GREETING

    if any(word in command for word in [
        "hello",
        "hi",
        "hey"
    ]):

        hour = datetime.datetime.now().hour

        if hour < 12:

            return "Good morning, boss. 😎"

        elif hour < 18:

            return "Good afternoon, boss. 😎"

        else:

            return "Good evening, boss. 😎"


    # TIME

    if (
        "time" in command
        or "what time" in command
    ):

        return f"It is {tell_time()}."


    # CALCULATOR

    if command.startswith("calculate"):

        expression = command.replace(
            "calculate",
            "",
            1
        ).strip()

        result = calculate(expression)

        return f"The answer is {result}."


    # REMEMBER

    result = remember_fact(command, memory)

    if result:

        return result


    # RECALL

    if (
        "what do you remember" in command
        or command.startswith("what is")
        or command.startswith("what's")
    ):

        result = recall_memory(command, memory)

        if result:

            return result

        return "I don't remember anything about that yet."


    # ADD NOTE

    result = add_note(command, memory)

    if result:

        return result


    # SHOW NOTES

    if (
        "show my notes" in command
        or "show notes" in command
        or "what are my notes" in command
    ):

        return show_notes(memory)


    # SEARCH

    if command.startswith("search"):

        return search_web(command)


    # OPEN WEBSITE

    result = open_website(command)

    if result:

        return result


    # UNKNOWN

    return (
        "I don't understand that yet. 🤔\n"
        "Try saying 'help'."
    )


# -----------------------------
# HELP
# -----------------------------

def show_help():

    print("""
================ JARVIS V2 ================

Examples:

👋 Greeting
    hello
    hey jarvis

⏰ Time
    what time is it?
    tell me the time

🧮 Calculator
    calculate 25 * 48
    calculate (100 + 50) / 5

🧠 Memory
    remember that my project is Plant Doctor
    remember my language is C++

    what is my project?
    what do you remember about my project?

📝 Notes
    make a note that I need to practice DP
    note that I need to study OS

    show my notes

🌐 Web
    search Python decorators
    search latest AI news

🌍 Websites
    open youtube
    open google
    open github

🚪 Exit
    bye
    exit

============================================
""")


# -----------------------------
# MAIN
# -----------------------------

def jarvis():

    memory = load_memory()

    print("""
╔══════════════════════════════════╗
║        🤖 JARVIS V2 ONLINE       ║
║      Natural Command System      ║
╚══════════════════════════════════╝

Type 'help' for commands.
""")

    while True:

        command = input("You: ")

        if command.lower().strip() == "help":

            show_help()
            continue

        response = process_command(
            command,
            memory
        )

        if response == "EXIT":

            print(
                "Jarvis: Shutting down, boss. 🫡"
            )

            break

        print(f"Jarvis: {response}")


if __name__ == "__main__":

    jarvis()
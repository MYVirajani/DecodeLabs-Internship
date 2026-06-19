# Project 1: Rule-Based AI Chatbot

A simple rule-based chatbot built in Python that responds to predefined user inputs using if-else logic and dictionary-based intent matching.


## Key Requirements

- Handle greetings and exit commands
- Use if-else logic for responses
- Run in a continuous loop

---

##  Key Concepts

- **Control Flow** — `if / elif / else` for decision-making
- **Input Sanitization** — `.lower().strip()` normalizes all user input
- **Dictionary Lookup** — O(1) response retrieval using `.get()` with fallback
- **IPO Model** — Input → Process → Output architecture
- **Infinite Loop** — `while True` keeps the chatbot running until exit command

---

## Architecture

This chatbot follows the **IPO (Input → Process → Output)** model:

```
User Input  →  Sanitization (.lower().strip())  →  Dictionary Lookup  →  Response
```

- **Input Phase** — Raw user text is captured and normalized
- **Process Phase** — Cleaned input is matched against the knowledge base dictionary
- **Output Phase** — Matched response is printed; fallback fires for unknowns

---

## Project Structure

```
project1-rule-based-chatbot/
└── chatbot.py
└── README.md
```

## Supported Intents

| User Input | Bot Response |
|---|---|
| `hello` | Hi there! How can I help you? |
| `hi` | Hey! What's up? |
| `how are you?` | I'm just a bot, but I'm running great! |
| `thank you` | You're welcome! |
| `thanks` | Happy to help! |
| `help` | Lists all supported commands |
| `bye` | Goodbye! Have a great day! |
| `exit` / `quit` | Shuts down the chatbot |
| *(anything else)* | Sorry, I do not understand. Try saying 'help'. |

---

## How to Run

**Prerequisites:** Python 3.x installed

```bash
# Clone the repository
git clone https://github.com/MYVirajani/DecodeLabs-Internship.git
# Navigate into the folder
cd Rule_based_AI_Chatbot

# Run the chatbot
python chatbot.py
```

---

## Sample Output

```
    Welcome! I am your AI Chatbot.   
    Type 'exit' or 'quit' to end the conversation.     

You: hello
Bot: Hi there! How can I help you?

You: how are you?
Bot: I'm just a bot, but I'm running great!

You: what is the weather
Bot: Sorry, I do not understand. Try saying 'help'.

You: help
Bot: I can answer the following:
     → hello
     → hi
     → bye
     → how are you?
     → thank you
     → thanks
     → quit
     → exit

You: exit
Bot: Goodbye! Shutting down...
```



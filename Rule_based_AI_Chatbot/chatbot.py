
responses = {
    "hello": "Hi there! How can I help you?",
    "hi": "Hey! What's up?",
    "bye": "Goodbye! Have a great day!",
    "how are you?": "I'm just a bot, but I'm running great!",
    "thank you": "You're welcome!",
    "thanks": "Happy to help!",
    "help": """I can answer the following:
     → hello
     → hi
     → bye
     → how are you?
     → thank you
     → thanks
     → quit
     → exit"""
}

def get_clean_input():
    raw = input("You: ")
    return raw.lower().strip()

def get_response(user_input):
    return responses.get(user_input, "Sorry, I do not understand. Try saying 'help'.")

def chatbot():
    print("    Welcome! I am your AI Chatbot.   ")
    print("    Type 'exit' or 'quit' to end the conversation.     \n")
    
    while True:
        user_input = get_clean_input()
        
        if user_input == "exit" or user_input == "quit":
            print("Bot: Goodbye! Shutting down...")
            break
        
        reply = get_response(user_input)
        print(f"Bot: {reply}\n")

if __name__ == "__main__":
    chatbot()
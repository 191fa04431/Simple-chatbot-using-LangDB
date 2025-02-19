import tkinter as tk  
from tkinter import scrolledtext, messagebox, ttk  
from openai import OpenAI  
import random  
import threading  

class DSAChatbotUI:  
    def __init__(self, master):  
        self.master = master  
        master.title("Datascience Tutor by Avinash")  
        master.geometry("600x700")  
        master.configure(bg="#f0f0f0")  

        # Chatbot backend  
        self.chatbot = DSAChatbot()  

        # Create main frame  
        self.main_frame = tk.Frame(master, bg="#f0f0f0")  
        self.main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)  

        # Chat display area  
        self.chat_display = scrolledtext.ScrolledText(  
            self.main_frame,   
            wrap=tk.WORD,   
            width=70,   
            height=25,   
            font=("Arial", 10),  
            bg="white",  
            state=tk.DISABLED  
        )  
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)  

        # Input frame  
        input_frame = tk.Frame(self.main_frame, bg="#f0f0f0")  
        input_frame.pack(fill=tk.X, padx=10, pady=5)  

        # User input entry  
        self.user_input = tk.Entry(  
            input_frame,   
            font=("Arial", 12),   
            width=50,  
            relief=tk.FLAT,  
            bg="white"  
        )  
        self.user_input.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)  
        self.user_input.bind("<Return>", self.send_message)  

        # Send button  
        send_button = tk.Button(  
            input_frame,   
            text="Send",   
            command=self.send_message,  
            bg="#4CAF50",  
            fg="white",  
            font=("Arial", 10, "bold")  
        )  
        send_button.pack(side=tk.RIGHT, padx=5, pady=5)  

        # Welcome message  
        self.display_message("Datascience Tutor",   
            "Hi! I'm your AI-powered Datascience tutor created by Avinash. "   
            "I can help you understand Data Science concepts and Algorithms.")  

    def send_message(self, event=None):  
        # Get user input  
        user_text = self.user_input.get().strip()  
        
        if not user_text:  
            return  
        
        # Clear input field  
        self.user_input.delete(0, tk.END)  
        
        # Display user message  
        self.display_message("You", user_text)  
        
        # Check for exit  
        if user_text.lower() == 'bye':  
            self.display_message("Datascience Tutor", "Goodbye! Keep learning!")  
            return  

        # Process message in a separate thread  
        threading.Thread(target=self.process_message, args=(user_text,), daemon=True).start()  

    def process_message(self, user_text):  
        try:  
            # Get response from chatbot  
            response = self.chatbot.get_response(user_text)  
            
            # Display response  
            self.display_message("Datascience Tutor", response)  
        except Exception as e:  
            self.display_message("Error", f"An error occurred: {str(e)}")  

    def display_message(self, sender, message):  
        # Thread-safe message display  
        def update_display():  
            self.chat_display.configure(state=tk.NORMAL)  
            self.chat_display.insert(tk.END, f"{sender}: {message}\n\n")  
            self.chat_display.configure(state=tk.DISABLED)  
            self.chat_display.yview(tk.END)  
        
        self.master.after(0, update_display)  

class DSAChatbot:  
    def __init__(self):
        # LangDB API configuration
        self.api_base = "https://api.us-east-1.langdb.ai"
        self.api_key = "langdb_MmQ3NG03c3Frdmo4Y25jdWNvY3I3NjBqamo="
        self.default_headers = {"x-project-id": "09c45264-3d6b-4c9e-bbb1-d13a1601de4c"}
        
        # Initialize OpenAI client
        self.client = OpenAI(
            base_url=self.api_base,
            api_key=self.api_key,
        )
        
        # Basic responses for common interactions
        self.basic_responses = {
            "hello": ["Hi! I'm your Datascience tutor created by Avinash. What would you like to learn today?", 
                     "Hello! Ready to dive into some Data Science and Algorithms?",
                     "Welcome! I'm here to help you understand Datascience concepts."],
            "bye": ["Goodbye! Keep practicing those algorithms!",
                   "See you later! Don't forget to review your data science concepts!",
                   "Have a great day! Remember, practice makes perfect!"]
        }

    def get_response(self, user_input):
        # Check for basic commands first
        user_input_lower = user_input.lower()
        if user_input_lower in self.basic_responses:
            return random.choice(self.basic_responses[user_input_lower])
        
        try:
            # Prepare messages for the API
            messages = [
                {
                    "role": "system",
                    "content": "You are a Datascience educator. Help the user with their queries regarding Datascience. Explain concepts in a clear and simple way, using analogies when helpful."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
            
            # Make API call
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7,
                max_tokens=700,
                top_p=1.0,
                extra_headers=self.default_headers
            )
            
            # Extract and return the assistant's reply
            return response.choices[0].message.content
            
        except Exception as e:
            return f"I encountered an error: {str(e)}"

def main():
    chatbot = DSAChatbot()
    print("Datascience Tutor: Hi! I'm your AI-powered Datascience tutor created by Avinash. I can help you understand Data Science concepts and Algorithms.")
    print("          Ask me anything about Datascience, or type 'bye' to exit.")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'bye':
            print("Datascience Tutor:", chatbot.get_response("bye"))
            break
            
        response = chatbot.get_response(user_input)
        print("Datascience Tutor:", response)

if __name__ == "__main__":
    main()


def main():  
    root = tk.Tk()  
    root.title("Datascience Tutor")  
    
    # Set a modern, clean icon (you can replace with your own icon path)  
    try:  
        root.iconbitmap('path/to/your/icon.ico')  # Optional  
    except:  
        pass  
    
    app = DSAChatbotUI(root)  
    root.mainloop()  

if __name__ == "__main__":  
    main()
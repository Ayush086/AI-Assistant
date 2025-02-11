# AI-Powered Personal Assistant

This AI-based personal assistant chatbot is designed to handle a variety of tasks, including automation, real-time search, chatbot interactions, and speech-to-text conversions. It integrates multiple functionalities and APIs to deliver an interactive user experience.

## 🚀 Features
- **Voice Command Recognition**: Converts speech to text and executes commands.
- **Automation**: Performs system-related tasks (e.g., opening/closing applications, playing music, adjusting system settings).
- **Real-time Search Engine**: Retrieves live information using APIs.
- **Chatbot**: Responds to general queries using an LLM-powered chatbot.
- **Image Generation**: Utilizes APIs to generate images based on user prompts.
- **Text-to-Speech**: Converts AI responses into spoken output.
- **Graphical User Interface (GUI)**: Provides an intuitive chat interface.

## 🛠 Installation

### Prerequisites
- Python 3.8+
- Virtual Environment (optional but recommended)

### Setup
1. **Clone the Repository**
   ```sh
   git clone https://github.com/Ayush086/AI-Assistant.git
   cd your-repo-name
   ```

2. **Create a Virtual Environment** (Optional but recommended)
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```sh
   pip install -r Requirements.txt
   ```

4. **Set Up Environment Variables**
   Create a `.env` file in the project's root directory and add the following:
   ```ini
   USERNAME=your_username
   ASSISTANTNAME=your_assistant_name
   ASSISTANTVOICE=your_preferred_voice
   API_KEY=your_api_key_here
   ANOTHER_API_KEY=your_other_api_key
   ```

5. **Run the Assistant**
   ```sh
   python main.py
   ```

## 📂 File Structure
```
📂 Project
│── 📂 Backend
│   ├── Automation.py
│   ├── Chatbot.py
│   ├── ImageGeneration.py
│   ├── Model.py
│   ├── RealtimeSearchEngine.py
│   ├── SpeechToText.py
│   ├── TextToSpeech.py
│
│── 📂 Frontend
│   ├── GUI.py
│
│── 📂 Data
│   ├── ChatLog.json
│
│── .env  # Environment variables
│── .gitignore
│── requirements.txt
│── main.py
│── README.md
```

## 🎤 Usage
1. **Activate the virtual environment** (if using one)
   ```sh
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
2. **Run the assistant**
   ```sh
   python main.py
   ```
3. **Interact via Voice or GUI**
   - Speak commands into the microphone.
   - Use the chat interface for text-based interactions.

## 🤝 Contributing
Contributions are welcome! Feel free to submit issues or pull requests. Please follow best coding practices and document any changes accordingly.

## ⚠️ Disclaimer
This assistant relies on third-party APIs. Ensure you comply with their respective terms and policies when using them.

---

🎉 **Happy Coding!**


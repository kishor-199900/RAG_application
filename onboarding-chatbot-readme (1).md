# AI Chatbot for User Onboarding

This project implements an AI-powered chatbot for user onboarding using LangChain, FAISS, and Retrieval-Augmented Generation (RAG) techniques.

## Prerequisites

- Python 3.7 or higher
- OpenAI API key

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/onboarding-chatbot.git
   cd onboarding-chatbot
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install langchain openai sqlalchemy faiss-cpu numpy
   ```

4. Set up your OpenAI API key:
   - Option 1: Set it as an environment variable:
     ```
     export OPENAI_API_KEY="your-api-key-here"
     ```
   - Option 2: Replace "your-api-key-here" in the `onboarding_chatbot.py` file with your actual API key.

5. Prepare your knowledge base:
   - Create a directory named `knowledge_base` in the project root.
   - Add relevant .txt files containing information about your onboarding process and company to this directory.

6. Update the `knowledge_base_dir` variable in `onboarding_chatbot.py` with the path to your knowledge base directory.

## Running the Chatbot

To start the onboarding chatbot, run:

```
python onboarding_chatbot.py
```

Follow the prompts to complete the onboarding process. You can type "help" at any time to get more information about a specific question. After completing the onboarding, you can ask additional questions about the company or process.

Type "exit" to end the conversation.

## Customization

- To modify the onboarding questions, edit the `onboarding_questions` list in `onboarding_chatbot.py`.
- To change the database schema, update the `User` class in `onboarding_chatbot.py`.
- To enhance the knowledge base, add or modify .txt files in the `knowledge_base` directory.

## Troubleshooting

If you encounter any issues:
1. Ensure your OpenAI API key is correctly set.
2. Check that all required packages are installed.
3. Verify that the knowledge base directory path is correct.

For any other problems, please open an issue on the GitHub repository.

import os
import re
import google.generativeai as genai

genai.configure(api_key="API_KEY")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash-002",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction="python is your native language. you will answer only in python code. i do not any explanations outside of python code. do not print anything outside of code blocks if you want to explain anything, say in print function. always use try block to avoid errors . if i say plain text answer, strictly use print function only for that prompt, do not use any other function if i say plain text only. use try block whenever necessary to avoid errors. if the code contains a library, then add try block to check if it is installed or not, to avoid errors.",
)

chat_session = model.start_chat(
  history=[
  ]
)

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit", "bye","cls"]:
        break

    response = chat_session.send_message(user_input)

    # Remove triple backticks and extra whitespace
    cleaned_response = re.sub(r"```python\s*|\s*```", "", response.text).strip() 

    # Execute the code and print the result
    try:
        exec(cleaned_response)
    except Exception as e:
        print(f"Error executing code: {e}") 

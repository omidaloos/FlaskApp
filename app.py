import openai as ai
from flask import Flask, render_template, request

#!/usr/bin/env python3


with open(r"/Volumes/Omid's USB/APIKeys/ChatGPTAPIKey.txt") as apiKey:
    key = apiKey.read()

ai.api_key = key

def generate_gpt3_response(user_text, print_output=False):
    """
    Query OpenAI GPT-3 for the specific key and get back a response
    :type user_text: str the user's text to query for
    :type print_output: boolean whether or not to print the raw output JSON
    """
    completions = ai.Completion.create(
        engine='text-davinci-003',  # Determines the quality, speed, and cost.
        temperature=0.5,            # Level of creativity in the response
        prompt=user_text,           # What the user typed in
        max_tokens=100,             # Maximum tokens in the prompt AND response
        n=1,                        # The number of completions to generate
        stop=None,                  # An optional setting to control response generation
    )

    # Displaying the output can be helpful if things go wrong
    if print_output:
        print(completions)

    # Return the first choice's text
    return completions.choices[0].text

### Search for different models to use:
# models = ai.Model.list()

# for model in models.data:
#     print(model.id)


context = "Provide a haiku based on the following input: "
# prompt = context + input("What do you want to query?: ")
# response = generate_gpt3_response(prompt)

# print(response)


app = Flask(__name__, static_folder='static')
chat_history = []

# @app.route('/', methods=['GET', 'POST'])
# def home():
#     if request.method == 'POST':
#         user_text = request.form['user_input']
#         response = generate_gpt3_response(user_text)
#         return render_template('index.html', response=response)
#     else:
#         return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get user input from the HTML form
        user_input = request.form['user_input']
        
        # Generate GPT-3 response
        response = generate_gpt3_response(context + user_input)
        
        # Add the user input and response to the chat history
        chat_history.append({'user': user_input, 'bot': response})

    return render_template('index.html', chat_history=chat_history)


if __name__ == '__main__':
    app.run(debug=True)


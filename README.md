
# Setup
* Download Pycharm free community version
  * I am using the pro version, so hopefully it has the features used in this readme
* Download Python 3.9 from the website and install
* Checkout code from bitbucket
* For venv:
  * Use virtualenv as the venv type
  * Choose python 3.9 as interpreter (there are issues with latest version)
* Go to the terminal tab in lower left of Pycharm
* Run `pip install -r requirements.txt` in terminal to install dependencies

# Verify notebooks
* Open AI model
  * Clone `.env.default` to `.env` and add your openAI API key. 
  * Click the `install juypter` button in upper right of editor
  * Click the green double arrows to run all statements in it.
  
# Start the server
  * Run `python api.py`
  * Verify server starts on port 8001
  * (optional) Test with `curl -X POST -H "Content-Type: application/json" -d '{"text": "What is your name?"}' http://localhost:8001/send_local`

# Start the UI
  * Run `python chat_ui.py`
  * Webapp should open in your browser
  * Choose GPT 3.5 and talk with it to talk to open AI
  * Choose local to talk to local

# Debug - Tracing langchain
  * Start tracing server with `langchain-server` from terminal
  * Ensure 
 

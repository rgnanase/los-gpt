
# Setup
* Start your local model download since it is 3GB or so
  * Download [ggml-gpt4all-j-v1.3-groovy.bin](https://gpt4all.io/models/ggml-gpt4all-j-v1.3-groovy.bin)
* Download Pycharm free community version
  * I am using the pro version, so hopefully it has the features used in this readme
* Download Python 3.9 from the website and install
* Checkout code from bitbucket
* For venv:
  * Use virtualenv as the venv type
  * Choose python 3.9 as interpreter (there are issues with latest version)
* Go to the terminal tab in lower left of Pycharm
* Run `pip install -r requirements.txt` in terminal to install dependencies
* Place the model you downloaded in the first step in the `models` directory
  * Create a `models` directory in the project

# Verify notebooks
* Local model
  * Open the `demo-local.ipynb` notebook
  * Click the `install juypter` button in upper right of editor
  * Click the green double arrows to run all statements in it.
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

# Verify vector DB and PDF indexing is working
  * Ask either chat `what is the UMD20 verification keyword?` and it should return `1d7:dsy3`
  * If you look in the `/docs` directory I added a verification PDF with that info 
  * You may need to ask the local model a few times - it's not as good as open ai

# Debug - Tracing langchain
  * Start tracing server with `langchain-server` from terminal
  * Ensure 
 

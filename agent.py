import os
from dotenv import dotenv_values
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
import uvicorn
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles

app = Starlette()
app.mount("/docs", StaticFiles(directory="docs"), name="docs")
app = FastAPI()
env_vars = dotenv_values('.env')
os.environ["OPENAI_API_KEY"] = env_vars['OPENAI_API_KEY']

@app.on_event("startup")
async def start_databases():
    start_openai_db()


def start_openai_db():
    from langchain.agents import create_csv_agent
    from langchain.llms import OpenAI
    global agent
    agent = create_csv_agent(OpenAI(temperature=0.5),
                             'los_langchain_csv1.csv',
                             verbose=True)
    agent.agent.llm_chain.prompt.template

@app.post("/send_openai")
async def send_openai(text: str = Body(..., embed=True)):
    print(f'Input to AI model: {text}')
    response = agent.run(text)
    print(f'Response from OpenAI model: {response}')
    return JSONResponse(content=response)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)

#!/usr/bin/env python3
from typing import List, Tuple
import httpx
from nicegui import app, Client, ui
from nicegui.events import ValueChangeEventArguments

messages: List[Tuple[str, str, str]] = []
thinking: bool = False

app.add_static_files('/docs', 'docs')

timeout = httpx.Timeout(timeout=30.0)  # Set the timeout to 30 seconds

using_llm = 'GPT35T'


@ui.refreshable
async def chat_messages() -> None:
    for name, text in messages:
        ui.chat_message(text=text, name=name, sent=name == 'You')
    if thinking:
        ui.spinner(size='3rem').classes('self-center')
    await ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)', respond=False)


def choose_model(event: ValueChangeEventArguments):
    global using_llm
    if event.value == 'ChatLoS - Domestic Traffic Ad Chat bot powered by OpenAI\'s GPT 3':
        using_llm = 'GPT35T'
        ui.notify(f'Switched to GPT 3.5 turbo model')
    # else:
    #     using_llm = 'Local'
    #     ui.notify(f'Switched to local model')


@ui.page('/')
async def main(client: Client):
    async def send() -> None:
        global thinking
        message = text.value
        messages.append(('You', text.value))
        thinking = True
        text.value = ''
        chat_messages.refresh()
        response = type('Response', (), {})()  # Create a default response object
        response.status_code = None  # Add a status_code attribute and set it to None
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                if using_llm == 'GPT35T':
                    # ui.notify(f'Going to call the api')
                    response = await client.post(
                        "http://localhost:8001/send_openai",
                        json={"text": message},
                    )
                # else:
                #     response = await client.post(
                #         "http://localhost:8001/send_local",
                #         json={"text": message},
                #     )
            except Exception as e:
                print(f"An exception occurred: {e}")
                ui.notify(f'Error: {e}', position='top', type='warning')
                thinking = False
                chat_messages.refresh()

        if response and response.status_code == 200:
            messages.append(('Bot', response.json()))
            thinking = False
            chat_messages.refresh()

    anchor_style = r'a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500}'
    ui.add_head_html(f'<style>{anchor_style}</style>')
    await client.connected()

    with ui.column().classes('w-full max-w-2xl mx-auto items-stretch'):
        ui.radio(['ChatLoS - Domestic Traffic Ad Chat bot powered by OpenAI\'s GPT 3'], value='ChatLoS - Domestic Traffic Ad Chat bot powered by OpenAI\'s GPT 3.5 Turbo 16K', on_change=choose_model).props('inline')

        # ui.markdown(
        #     'The Vector database has indexed the [Overview](docs/Billing Overview Student Financial Services and Cashiering.pdf), [Schedule](docs/Billing Schedule Student Financial Services and Cashiering.pdf), and [Fees](docs/Tuition and Fees Student Financial Services and Cashiering.pdf) PDF documents. Review these documents for questions you can ask')

    with ui.column().classes('w-full max-w-2xl mx-auto items-stretch'):
        await chat_messages()

    with ui.footer().classes('bg-white'), ui.column().classes('w-full max-w-3xl mx-auto my-6'):
        with ui.row().classes('w-full no-wrap items-center'):
            text = ui.input().props('rounded outlined input-class=mx-3') \
                .classes('w-full self-center').on('keydown.enter', send)
        ui.markdown('simple chat app built with [NiceGUI](https://nicegui.io)') \
            .classes('text-xs self-end mr-8 m-[-1em] text-primary')


ui.run(title='ChatLoS - Domestic Traffic Ad Chat bot powered by OpenAI\'s GPT 3')

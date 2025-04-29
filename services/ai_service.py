import os
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from fastapi.concurrency import run_in_threadpool

async def get_ai_analyze(question, answer):
    load_dotenv()
    token = os.environ["GITHUB_TOKEN"]

    client = ChatCompletionsClient(
        endpoint="https://models.github.ai/inference",
        credential=AzureKeyCredential(token),
    )

    def sync_call():
        response = client.complete(
            messages=[
                SystemMessage(content=(
                    "You are a professional technical interviewer evaluating a candidate's response to an interview question. "
                    "Your task is to analyze the candidate's answer and return ONLY a strict JSON dictionary with two fields:\n"
                    "- \"score\": an integer from 1 to 10 evaluating the overall quality and relevance of the response\n"
                    "- \"verdict\": a short, objective explanation (in plain English) justifying the score\n\n"
                    "You must respond with **only** a valid JSON object. No explanations or additional text outside the JSON."
                )),
                UserMessage(content=(
                    f"Question: {question}, Answer: {answer}"
                )),
            ],
            temperature=0.3,
            top_p=1,
            model="openai/gpt-4.1"
        )
        print(response.choices[0].message.content
)
        return response.choices[0].message.content

    result = await run_in_threadpool(sync_call)
    return result
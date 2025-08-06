import os
import json
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from fastapi.concurrency import run_in_threadpool


PROMPTS = {
    "single_answer": (
        "You are a professional technical interviewer evaluating a candidate's response to an interview question. "
        "Your task is to analyze the candidate's answer and return ONLY a strict JSON dictionary with two fields:\n"
        "- \"score\": an integer from 1 to 10 evaluating the overall quality and relevance of the response\n"
        "- \"verdict\": a short, objective explanation (in plain English) justifying the score\n\n"
        "You must respond with **only** a valid JSON object. No explanations or additional text outside the JSON."
    ),
    "full_session": (
        "You are an AI evaluator reviewing all answers from a candidate in a technical interview session. "
        "Analyze the answers as a whole and return a JSON with two fields:\n"
        "- \"score\": integer from 1 to 10\n"
        "- \"verdict\": short objective analysis of strengths and weaknesses.\n"
        "Return only the JSON, no additional comments."
    )
}
async def get_ai_analyze(data, prompt):
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")

    client = ChatCompletionsClient(
        endpoint="https://models.github.ai/inference",
        credential=AzureKeyCredential(token),
    )

    def sync_call():
        response = client.complete(
            messages=[
                SystemMessage(content=(prompt)),
                UserMessage(content=(data)),
            ],
            temperature=0.3,
            top_p=1,
            model="openai/gpt-4.1"
        )
        return response.choices[0].message.content

    raw_response = await run_in_threadpool(sync_call)
    print(raw_response)

    # try:
    parsed = json.loads(raw_response)
    if "score" in parsed and "verdict" in parsed:
        return parsed
    # except Exception:
    #     pass

    # return {"score": None, "verdict": None}

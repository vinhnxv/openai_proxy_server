import json
import time

import shortuuid
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from g4f import ChatCompletion

from schemas import ChatCompletionRequest

app = FastAPI()


@app.post("/chat/completions")
def chat_completions(request: ChatCompletionRequest):
    response = ChatCompletion.create(model=request.model, stream=request.streaming,
                                     messages=request.messages)

    if not request.streaming:
        while 'curl_cffi.requests.errors.RequestsError' in response:
            response = ChatCompletion.create(model=request.model, stream=request.streaming,
                                             messages=request.messages)

        completion_timestamp = int(time.time())
        completion_id = shortuuid.ShortUUID().random(length=28)

        return {
            'id': 'chatcmpl-%s' % completion_id,
            'object': 'chat.completion',
            'created': completion_timestamp,
            'model': request.model,
            'usage': {
                'prompt_tokens': None,
                'completion_tokens': None,
                'total_tokens': None
            },
            'choices': [{
                'message': {
                    'role': 'assistant',
                    'content': response
                },
                'finish_reason': 'stop',
                'index': 0
            }]
        }

    def stream():
        for token in response:
            completion_timestamp = int(time.time())
            completion_id = shortuuid.ShortUUID().random(length=28)

            completion_data = {
                'id': f'chatcmpl-{completion_id}',
                'object': 'chat.completion.chunk',
                'created': completion_timestamp,
                'model': 'gpt-3.5-turbo-0301',
                'choices': [
                    {
                        'delta': {
                            'content': token
                        },
                        'index': 0,
                        'finish_reason': None
                    }
                ]
            }
            data = json.dumps(completion_data, separators=(",", ":"))
            yield f'data: {data}\n\n'
            time.sleep(0.1)

    return StreamingResponse(stream(), media_type='text/event-stream')

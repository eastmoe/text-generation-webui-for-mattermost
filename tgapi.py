import json

import requests

# For local streaming, the websockets are hosted without ssl - http://
# 修改为自己TGWEBUI的API地址
HOST = 'localhost:5000'
URI = f'http://{HOST}/api/v1/chat'

# For reverse-proxied streaming, the remote will likely host with ssl - https://
# URI = 'https://your-uri-here.trycloudflare.com/api/v1/chat'


def run(user_input, history):
    request = {
        'user_input': user_input,
        'history': history,
        # 修改模式
        'mode': 'instruct',  # Valid options: 'chat', 'chat-instruct', 'instruct'
        # 修改自定义角色
        'character': 'Assit',
        # 修改提示词模板
        'instruction_template': 'ChatGLM',
        # 对话中的你的名字
        'your_name': 'You',

        #对话参数
        'regenerate': False,
        '_continue': False,
        'stop_at_newline': False,
        # 最大提示词长度
        'chat_prompt_size': 2048,
        'chat_generation_attempts': 1,
        'chat-instruct_command': '',

        #对话新TOKEN长度
        'max_new_tokens': 250,
        'do_sample': True,
        # 生成温度
        'temperature': 0.7,
        'top_p': 0.1,
        'typical_p': 1,
        'epsilon_cutoff': 0,  # In units of 1e-4
        'eta_cutoff': 0,  # In units of 1e-4
        'tfs': 1,
        'top_a': 0,
        'repetition_penalty': 1.18,
        'top_k': 40,
        'min_length': 0,
        'no_repeat_ngram_size': 0,
        'num_beams': 1,
        'penalty_alpha': 0,
        'length_penalty': 1,
        'early_stopping': False,
        'mirostat_mode': 0,
        'mirostat_tau': 5,
        'mirostat_eta': 0.1,
        # 随机种子
        'seed': -1,
        'add_bos_token': True,
        'truncation_length': 2048,
        'ban_eos_token': False,
        'skip_special_tokens': True,
        'stopping_strings': []
    }

    response = requests.post(URI, json=request)

    if response.status_code == 200:
        #result = response.json()['results'][0]['history']
        #print(json.dumps(result, indent=4))
        #print()
        #print(result['visible'][-1][1])
        #return result['visible'][-1][1]
        # 当API返回HTTP200时，返回API直接返回的内容
        return response

#if __name__ == '__main__':
    #user_input = "Please give me a step-by-step guide on how to plant a tree in my backyard."

    # Basic example
    #history = {'internal': [], 'visible': []}

    # "Continue" example. Make sure to set '_continue' to True above
     #arr = [user_input, 'Surely, here is']
     #history = {'internal': [arr], 'visible': [arr]}

    #run(user_input, history)



# user_input = "Please give me a step-by-step guide on how to plant a tree in my backyard."
# history = {'internal': [], 'visible': []}
# run(user_input, history)
import ollama


class ollama_mode(object):
    def __init__(self, model):
        self.model = model
        # self.content = content
        # self.messages = messages

    def ollama_response_once(self, content):
        """
        ollama的本地模型调用，单次对话
        :return:一次性返回所有
        """
        response_content = []
        stream = ollama.chat(
            model=self.model,
            messages=[{'role': 'user', 'content': content}],
            stream=True,
            prompt="如果是问的岗位，则回答岗位所需求的知识、前沿方向和课程学习路线。"
        )
        for chunk in stream:
            response_content.append(chunk['message']['content'])

        return ''.join(response_content)

    def ollama_response_steam_once(self, content):
        """
        ollama的本地模型调用，单次对话
        :return:返回字节流
        """
        stream = ollama.chat(
            model=self.model,
            messages=[{'role': 'user', 'content': content}],
            stream=True,
        )
        return stream

    def ollama_response_continue(self, messages):
        """
        ollama的本地模型调用，连续对话
        :return:一次性返回所有
        """
        response_content = []
        stream = ollama.chat(
            model=self.model,
            messages=messages,
            stream=True,
        )
        for chunk in stream:
            response_content.append(chunk['message']['content'])

        return ''.join(response_content)

    def ollama_response_steam_continue(self, messages):
        """
        ollama的本地模型调用，连续对话
        :return:返回字节流
        """
        stream = ollama.chat(
            model=self.model,
            messages=messages,
            stream=True,
        )
        return stream


if __name__ == '__main__':
    # 方式1：全部返回
    # print(ollama_response(model, messages))

    # 方式2：字节流返回
    mode_api = ollama_mode("qwen2:7b")

    messages = []
    while True:
        user_content = input("you:")
        messages.append(dict({"role": "user", "content": user_content}))  # 用户对话

        assistant_content = []  # 模型对话

        for chunk in mode_api.ollama_response_steam_continue(messages):
            print(chunk['message']['content'], end='', flush=True)
            assistant_content.append(chunk['message']['content'])

        messages.append(
            {"role": "assistant", "content": ''.join(assistant_content)})
        print()
        # print("\n", messages)

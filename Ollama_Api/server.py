"""
接口类
"""
import pandas as pd
import tornado
from tornado import web, websocket
from chat_mode.Ollama import ollama_mode
import ollama
import json


class Index(web.RequestHandler):
    async def get(self):  # get方法
        """
        ollama的本地模型
        :return:
        """
        self.write(ollama.list())


class ChatHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True  # 允许跨域请求

    async def open(self):
        print("WebSocket opened")

    async def on_message(self, message):
        """

        :param message:
        :return:
        """
        # print("Received message:", message)
        data = json.loads(message)
        messages = data.get("messages", "")
        print("messages:", messages)
        if messages["content"] == "":
            print("空")
            await self.write_message(json.dumps({"response": "你可以问我点什么"}))

        # 使用本地模型
        mode_api = ollama_mode("qwen2:7b")

        # 团队关键字
        if "西南科技大学" in messages["content"]:
            # 读取CSV文件
            team = pd.read_csv("data/team.csv", encoding="GBK")
            # 去重，只保留第一次出现的记录
            team_unique = team.drop_duplicates(subset="团队名称", keep="first")
            # 提取特定的列
            team_data = team_unique[["团队名称", "负责人", "主要研究方向"]]
            # 将列转换为字典列表
            team_list = str(team_data.to_dict(orient="records"))
            if "history" in messages:
                for chunk in mode_api.ollama_response_steam_once(
                        "从下面是西南科技大学的团队信息，根据"+messages["history"]+"的信息，选取其中最匹配条件一个团队" +
                        "。要求必须只输出该团队的名称、负责人和主要研究方向:" + team_list):
                    # print(chunk)
                    if chunk["done"]:
                        response = {"response": "\n"}
                        await self.write_message(json.dumps(response))
                    else:
                        content = chunk['message']['content']
                        # print(content)
                        # print(chunk['message']['content'], end='', flush=True)
                        response = {"response": content}
                        await self.write_message(json.dumps(response))
            else:
                for chunk in mode_api.ollama_response_steam_once(
                        "从下面是团队信息，选取的其中匹配的一个团队。输出团队名称、负责人和主要研究方向:" + team_list):
                    # print(chunk)
                    if chunk["done"]:
                        response = {"response": "\n"}
                        await self.write_message(json.dumps(response))
                    else:
                        content = chunk['message']['content']
                        # print(content)
                        # print(chunk['message']['content'], end='', flush=True)
                        response = {"response": content}
                        await self.write_message(json.dumps(response))
        else:
            # 正常聊天
            if "history" in messages:
                for chunk in mode_api.ollama_response_steam_once(
                        messages["content"] + "如果是问的岗位，则只回答岗位所需求的知识、前沿方向、研究课题和课程学习路线。"
                                              "如果不是,则按照一下提示回答："+messages["history"]):
                    # print(chunk)
                    if chunk["done"]:
                        response = {"response": "\n"}
                        await self.write_message(json.dumps(response))
                    else:
                        content = chunk['message']['content']
                        # print(content)
                        # print(chunk['message']['content'], end='', flush=True)
                        response = {"response": content}
                        await self.write_message(json.dumps(response))
            else:
                for chunk in mode_api.ollama_response_steam_once(
                        messages[
                            "content"] + "如果是问的岗位，则只回答岗位所需求的知识、前沿方向、研究课题和课程学习路线。"):
                    # print(chunk)
                    if chunk["done"]:
                        response = {"response": "\n"}
                        await self.write_message(json.dumps(response))
                    else:
                        content = chunk['message']['content']
                        # print(content)
                        # print(chunk['message']['content'], end='', flush=True)
                        response = {"response": content}
                        await self.write_message(json.dumps(response))

    async def on_close(self):
        print("WebSocket closed")

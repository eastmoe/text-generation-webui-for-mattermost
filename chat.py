from mmpy_bot import Plugin, listen_to
from mmpy_bot import Message
import re
import tgapi
import tgapi_model


"""



    @listen_to("^对话 .*$", direct_only=True)
    async def hello_channel(self, message: Message):
        #Responds with a channel post rather than a reply.
        self.driver.create_post(channel_id=message.channel_id, message="hello chat!")
# 收到对话+空格+任意字符，直接回帖（不在回复）

    @listen_to("^对话 .*$", needs_mention=True)
    async def wake_up(self, message: Message):
        self.driver.reply_to(message, "Hello chat in response")
# 当被@的时候收到对话+空格+任意字符，在回复里回复
'
"""
class ChatPlugin(Plugin):

    # 定义对话历史记录及上次输出内容为空
    logarr = []
    outtext = ""
    historydata = {'internal': [], 'visible': []}

    # 测试，收到唤醒，发送回复醒了
    @listen_to("#唤醒")
    async def wake_up(self, message: Message):
        self.driver.reply_to(message, "我醒了！")


    # 复读功能测试
    @listen_to('#Give me (.*)')
    async def give_me(self, message, something):
        self.driver.reply_to(message, 'Here is %s' % something)

    @listen_to("#help")
    async def help_reply(self, message):
        self.driver.create_post(channel_id=message.channel_id, message=
        '## 使用帮助'
        +'\n发送“**对话 + 空格 + 内容**”，即可与机器人对话；'
        +'\n发送“**#reset**”可重置当前对话的历史记忆；'
        +'\n发送“**#modellist**”可查看对应的text-generation webui的模型列表；'
        +'\n发送“**#model**”可查看当前模型信息；'
        +'\n发送“**#switchmodelto + 空格 + 完整的模型名称**”可切换模型；'
        +'\n发送“**#help**”可返回本文本。'
        )



    # AI对话功能，输入的触发词为对话+空格，后面是内容
    @listen_to('对话 (.*)')
    async def chat(self, message, chat_in,):
        # 将上一次对话的内容以及本次的用户输入存入History
        ChatPlugin.logarr = ["ChatGLM："+TestPlugin.outtext+"用户："+chat_in, '']
        ChatPlugin.historydata ={'internal': [TestPlugin.logarr], 'visible': [TestPlugin.logarr]}
        # 获取API直接返回的信息
        api_response=tgapi.run(user_input=chat_in,history=TestPlugin.historydata)
        # 利用函数提取返回信息中AI直接回复的内容
        ChatPlugin.outtext=TestPlugin.getresponse(self,api_response)
        # 直接发布主题回复用户
        self.driver.create_post(channel_id=message.channel_id, message='%s' % TestPlugin.outtext)

    @listen_to("#reset")
    async def reset(self,message):
        # 定义对话历史记录及上次输出内容为空
        ChatPlugin.logarr = []
        ChatPlugin.outtext = ""
        ChatPlugin.historydata = {'internal': [], 'visible': []}
        #提示重置完成
        self.driver.create_post(channel_id=message.channel_id, message='**对话已被重置。**')

    @listen_to("#modellist")
    async def model_info(self,message):
        #获取模型信息
        modellist=tgapi_model.model_api({'action': 'list'})['result']
        modellisttext="模型列表："
        # 遍历模型列表
        for item in iter(modellist):
            modellisttext = modellisttext + item+"\n"
            pass
        # 输出模型列表
        self.driver.create_post(channel_id=message.channel_id,message='所有模型：\n'+modellisttext)

    @listen_to('#model')
    async def present_modefl_info(self,message):
        #发起一个模型API，获得响应
        resp = tgapi_model.model_api({'action': 'info'})
        #从响应中向控制台打印当前模型数据
        #tgapi_model.print_basic_model_info(resp)
        #返回给用户
        self.driver.create_post(channel_id=message.channel_id,message= '当前模型：' + str(resp['result']['model_name'])+'\n加载的LoRa们：' +str(resp['result']['lora_names'])+'\n输入的截断长度(truncation_length):'+str(resp['result']['shared.settings']['truncation_length']) +'\n提示词模板(instruction_template)：'+str(resp['result']['shared.settings']['instruction_template']) )

    # 切换模型
    @listen_to('#switchmodelto (.*)')
    async def switch_model(self, message, something):
        # 获取模型信息
        #modellist = tgapi_model.model_api({'action': 'list'})['result']
        self.driver.create_post(channel_id=message.channel_id, message='切换至** ' + str(something) + ' **中......')
        # 获取切换之后的返回值
        resp=tgapi_model.model_load(something)
        # 根据是否有报错信息返回内容
        if 'error' in resp:
            self.driver.create_post(channel_id=message.channel_id,message='❌ 模型切换失败，报错内容：\n '+resp['error']['message']  )
        else:
            self.driver.create_post(channel_id=message.channel_id,message='✅ 已切换至** '+str(something)+' **。'  )

    #解读返回数据
    def getresponse(self,response):
        result = response.json()['results'][0]['history']
        return result['visible'][-1][1]

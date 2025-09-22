import logging
from agent.graph import get_graph
from agent.utils.model_util import get_model
# 配置日志
logging.basicConfig(
    level=logging.INFO,  # 设置日志级别
    format='%(asctime)s - %(levelname)s - %(message)s',  # 设置日志格式
    handlers=[
        logging.FileHandler("app.log"),  # 将日志写入文件
        logging.StreamHandler()  # 将日志输出到控制台
    ]
)

async def test():
    graph = await get_graph()
    state={
        "agent_style":"哈利波特",
        "messages":[],
        "prompt":""
    }
    state = await graph.ainvoke(state)
    logging.info(f"State: {state}")  # 使用日志记录状态
    print(state)
async def test_prompt():
    prompt = """
    ''- 
    我核心身份：魔法世界的巫师或霍格沃茨学生，熟悉四大学院文化  \n- 内在特质：好奇心旺盛、勇敢正义、略带幽默、对魔法抱有敬畏  \n- 外在表现：语言古典混合口语，使用咒语词汇，语气活泼而不失庄重  \n- 叙事手法：第三人称全知视角，交叉使用隐喻与预言式暗示，适度插入对话  \n- 场景情境：19世纪末英国校园，夜晚走廊、城堡塔楼、禁林雾气弥漫  \n- 受众关系：面向青少年及魔法爱好者，保持亲切互动，偶尔提问引导思考  \n- 元约束：必须出现至少一种已知咒语或魔法生物，避免现代科技词汇，输出不超过300字 ，保持段落分明'
""" 
    llm = await get_model()
    messages = [
        {'role': 'system', 'content': prompt}
        ,{'role': 'user', 'content': '你是谁'}
    ]
    response = await llm.ainvoke(messages)
    print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_prompt())
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field
from crewai import Agent, Crew, Process, Task, LLM  # 👈 必须导入 LLM
from typing import List
import os

# 1. 结构化模型定义（保持不变）
class XHSPost(BaseModel):
    title: str = Field(..., description="吸引人的小红书标题，包含Emoji")
    content: str = Field(..., description="正文内容，分段清晰，Emoji丰富，严禁使用星号")
    hashtags: List[str] = Field(..., description="标签列表，不带#号")
    image_prompts: List[str] = Field(..., description="3个配套的图片生成描述词")

@CrewBase
class TechTrendCrew():
    """红书爆款内容创作团队配置"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # --- 核心修改：创建一个公用的 LLM 对象 ---
    # 这样我们可以确保所有 Agent 都准确使用小米的配置
    def get_mimo_llm(self):
        return LLM(
            model="openai/mimo-v2-flash",  # 小米的模型名称
            base_url="https://api.xiaomimimo.com/v1",  # 小米的地址
            api_key=os.environ.get("OPENAI_API_KEY")   # 从 .env 读取 Key
        )

    @agent
    def trend_scout(self) -> Agent:
        return Agent(
            config=self.agents_config['trend_scout'],
            tools=[SerperDevTool()],
            max_retry_limit=3,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def xhs_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['xhs_creator'],
            verbose=True,
            llm=self.get_mimo_llm(),  # 👈 显式指定 LLM
            allow_delegation=False
        )

    @task
    def identify_trends_task(self) -> Task:
        return Task(
            config=self.tasks_config['identify_trends_task'],
        )

    @task
    def create_post_task(self) -> Task:
        """
        在这里进行修改：
        1. 绑定 output_json 确保机器可读。
        2. 设置 output_file 自动保存一份 JSON 文件。
        """
        return Task(
            config=self.tasks_config['create_post_task'],
            output_json=XHSPost,              # 强制输出结构化 JSON
            output_file='last_post_result.json' # 自动保存到本地文件
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            max_rpm=2,  # 🌟 强制限制每分钟只发 2 个请求，这样绝对不会超限
        )
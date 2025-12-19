import os
import time


# --- 更新后的代理配置 ---
proxy_url = "http://127.0.0.1:17249"

os.environ["http_proxy"] = proxy_url
os.environ["https_proxy"] = proxy_url
os.environ["HTTP_PROXY"] = proxy_url
os.environ["HTTPS_PROXY"] = proxy_url

# 如果你是 Windows 环境，有时强制关闭 SSL 验证能解决握手失败
os.environ["PYTHONHTTPSVERIFY"] = "0"

import sys
# ⚠️ 注意：下面的 RedNoteCrew 必须和你 crew.py 里的 class 类名完全一致！
# 如果 crew.py 里写的是 class TechTrendCrew():，这里就改成 from red_note.crew import TechTrendCrew
from red_note.crew import TechTrendCrew


def run():
    """
    运行 Crew 团队，包含自动重试逻辑以应对 API 频率限制 (429)。
    """
    inputs = {
        'domains': '纯欲穿搭'
    }

    max_retries = 3  # 最大重试次数
    retry_delay = 30  # 触发 429 后的等待秒数

    for attempt in range(max_retries):
        try:
            # 启动团队
            result = TechTrendCrew().crew().kickoff(inputs=inputs)

            # --- 成功后的输出处理 ---
            print("\n" + "=" * 30)
            print("✨ 任务执行成功！")
            print("=" * 30)

            # 1. 获取给人类看的“原始文案”
            print("\n--- 人类阅读版 ---")
            print(result.raw)

            # 2. 获取给机器看的“结构化数据”
            print("\n--- 结构化数据 (JSON) ---")
            print(result.json_dict)

            # 3. 直接操作特定字段
            if result.pydantic:
                print("\n--- 关键字段提取 ---")
                print(f"标题：{result.pydantic.title}")
                print(f"标签数：{len(result.pydantic.hashtags)}")

            # 成功后跳出循环
            break

        except Exception as e:
            # 检查是否为频率限制错误 (429)
            error_msg = str(e)
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                if attempt < max_retries - 1:
                    print(f"\n⚠️ 触发 API 频率限制。正在等待 {retry_delay} 秒后进行第 {attempt + 2} 次重试...")
                    time.sleep(retry_delay)
                    continue
                else:
                    print("\n❌ 已达到最大重试次数，请稍后再运行或检查 API 配额。")
                    raise e
            else:
                # 如果是其他类型的错误（如代码错误、网络断开），直接抛出
                print(f"\n❌ 运行出错: {e}")
                raise e


# 下面的函数是用于训练和测试的，暂时可以不动
def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'domains': 'Makeup Trends'
    }
    try:
        TechTrendCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        TechTrendCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'domains': 'Makeup Trends'
    }
    try:
        TechTrendCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
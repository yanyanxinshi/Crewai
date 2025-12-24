import sys
import os
import re  # 导入正则模块，用于清洗文件名
import json  # 导入json模块，用于手动保存
from dotenv import load_dotenv

# 1. 加载环境变量 (必须在最前面)
load_dotenv()

# 2. 路径修复
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.append(src_dir)

from red_note.crew import TechTrendCrew


def run():
    """
    运行 Crew 团队，包含结果美化和动态文件保存功能。
    """
    inputs = {
        'domains': 'Coquette Aesthetic'  # 你可以随时改这个主题
    }

    print(f"🚀 正在启动 Crew，生成主题：{inputs['domains']}...")

    try:
        # 启动团队
        result = TechTrendCrew().crew().kickoff(inputs=inputs)

        # 获取结构化数据对象
        pydantic_output = result.pydantic

        if pydantic_output:
            # ==================================================
            # 🎨 功能 1：控制台美化输出 (解决 \n 看着乱的问题)
            # ==================================================
            print("\n" + "=" * 40)
            print("📱 --- 小红书文案预览 --- 📱")
            print("=" * 40)

            print(f"【标题】：\n{pydantic_output.title}\n")

            # 核心：把 \n 替换成真正的换行，并去掉首尾空格
            pretty_content = pydantic_output.content.replace(r"\n", "\n").strip()
            print(f"【正文】：\n{pretty_content}\n")

            # 处理标签
            tags = " ".join([f"#{tag}" for tag in pydantic_output.hashtags])
            print(f"【标签】：\n{tags}\n")

            print("-" * 20)
            print("【AI 配图指令】：")
            for i, prompt in enumerate(pydantic_output.image_prompts, 1):
                print(f"{i}. {prompt}")

            # ==================================================
            # 💾 功能 2：以标题命名并保存 JSON 文件
            # ==================================================

            # 1. 获取标题
            raw_title = pydantic_output.title

            # 2. 清洗文件名 (Windows 不允许文件名包含 \ / : * ? " < > |)
            # 我们用正则把这些符号替换为空
            safe_filename = re.sub(r'[\\/*?:"<>|]', "", raw_title)

            # 3. 截断文件名 (防止标题太长报错，限制前50个字)
            safe_filename = safe_filename[:50].strip()

            # 4. 拼接最终路径
            output_dir = "output"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            file_path = os.path.join(output_dir, f"{safe_filename}.json")

            # 5. 手动保存
            # result.json_dict 包含了所有数据
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(result.json_dict, f, ensure_ascii=False, indent=4)

            print("\n" + "=" * 40)
            print(f"✅ 文件已保存为：{file_path}")
            print("=" * 40)

        else:
            print("\n⚠️ 未检测到结构化输出，显示原始结果：")
            print(result.raw)

    except Exception as e:
        print(f"\n❌ 运行出错: {e}")
        raise e


if __name__ == "__main__":
    run()
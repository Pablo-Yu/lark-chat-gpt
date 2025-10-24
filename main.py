from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# 从 Secrets 中获取你的 OpenAI 密钥
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 新增一个 GET 路由，用于 Render 的健康检查（或 Lark 的 Verification Token 校验）
@app.route("/", methods=["GET"])
def index():
    return "Lark ChatGPT PDF Service is running."

@app.route("/", methods=["POST"])
def analyze_pdf_text():
    data = request.json
    content = data.get("text", "")

    if not content:
        return jsonify({"error": "No text provided"}), 400

    # 发送给 ChatGPT 分析文本内容
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "你是一位文献分析专家，请用中文整理用户提交的文献内容"},
            {"role": "user", "content": content}
        ]
    )

    reply = response.choices[0].message.content
    return jsonify({"result": reply})

# 启动 Flask 服务
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
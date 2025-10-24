from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# 设置 OpenAI 密钥
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["POST"])
def handle_lark_request():
    data = request.json

    # ✅ 如果是 URL 验证请求（来自 Lark 开发者平台）
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})

    # ✅ 如果是普通的消息/数据请求
    content = data.get("text", "")

    if not content:
        return jsonify({"error": "No text provided"}), 400

    # 调用 OpenAI 分析文本
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "你是一位文献分析专家，请用中文整理用户提交的文献内容"},
            {"role": "user", "content": content}
        ]
    )

    reply = response["choices"][0]["message"]["content"]
    return jsonify({"result": reply})


# 启动 Flask 服务
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

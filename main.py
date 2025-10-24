from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# 设置你的 OpenAI 密钥
openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ 回调接口 - 处理验证与正常请求
@app.route("/", methods=["POST"])
def handle_callback():
    data = request.get_json()

    # ⚠️ 检查 challenge 是否存在，处理 Lark 的验证请求
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})

    # 否则正常处理 text 字段
    content = data.get("text", "")
    if not content:
        return jsonify({"error": "No text provided"}), 400

    # 调用 ChatGPT 分析文本
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "你是一位文献分析专家，请用中文整理用户提交的文献内容"},
            {"role": "user", "content": content}
        ]
    )

    reply = response["choices"][0]["message"]["content"]
    return jsonify({"result": reply})

# ✅ Render 健康检查 GET 路由
@app.route("/", methods=["GET"])
def health_check():
    return "OK", 200

# 启动 Flask 应用
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

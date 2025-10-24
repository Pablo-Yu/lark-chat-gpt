from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# 设置 OpenAI API 密钥
openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ Lark 回调验证接口（POST方式）
@app.route("/", methods=["POST"])
def handle_lark_event():
    data = request.json

    # Lark URL 验证（带 challenge 字段）
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})

    # 正常文本分析逻辑
    content = data.get("text", "")
    if not content:
        return jsonify({"error": "No text provided"}), 400

    # 调用 OpenAI 进行分析
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "你是一位文献分析专家，请用中文整理用户提交的文献内容"},
            {"role": "user", "content": content}
        ]
    )
    reply = response["choices"][0]["message"]["content"]
    return jsonify({"result": reply})

# ✅ Render 健康检查用的 GET 路由（可选）
@app.route("/", methods=["GET"])
def health_check():
    return "OK", 200

# 启动 Flask 应用
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

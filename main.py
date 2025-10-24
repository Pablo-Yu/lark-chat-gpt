from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# 设置 OpenAI API 密钥（从环境变量中读取）
openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ GET 路由：健康检查（Render 会调用）
@app.route("/", methods=["GET"])
def health_check():
    return "OK", 200

# ✅ POST 路由：接收 Lark 验证和用户请求
@app.route("/", methods=["POST"])
def lark_callback():
    data = request.get_json()

    # ⚠️ 如果是 Lark 的初始验证请求，返回 challenge 字段
    if data and "challenge" in data:
        return jsonify({"challenge": data["challenge"]})

    # ✅ 处理用户发来的 text 字段内容（分析 PDF 文本）
    content = data.get("text", "")
    if not content:
        return jsonify({"error": "No text provided"}), 400

    # 调用 ChatGPT API
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "你是一位文献分析专家，请用中文整理用户提交的文献内容"},
                {"role": "user", "content": content}
            ]
        )
        reply = response["choices"][0]["message"]["content"]
        return jsonify({"result": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 启动 Flask 服务
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

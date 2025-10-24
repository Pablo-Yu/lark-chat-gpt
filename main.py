from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# 获取 OpenAI 的 API 密钥（从环境变量中）
openai.api_key = os.getenv("OPENAI_API_KEY")

# 支持 GET + POST 方法的主路由
@app.route("/", methods=["GET", "POST"])
def handle_request():
    # GET 请求用于 Lark 验证回调地址
    if request.method == "GET":
        return "OK", 200

    # POST 请求处理文本分析
    data = request.get_json()
    content = data.get("text", "")

    if not content:
        return jsonify({"error": "No text provided"}), 400

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

# 启动 Flask 应用（Render 要求使用 5000 端口）
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

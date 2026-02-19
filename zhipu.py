from openai import OpenAI

client = OpenAI(
    # base_url="https://api.z.ai/api/coding/paas/v4",   # 国际域名
    base_url="https://open.bigmodel.cn/api/coding/paas/v4",  # 国内更快
    api_key="a1cd8c131bb2496097d662a2feeeb6c4.a1q8aDi7PDQiJSKC"
)

response = client.chat.completions.create(
    model="glm-4.7",          # 或 glm-5（Max/Pro 计划才支持）
    messages=[{"role": "user", "content": "你好，你是什么模型？"}],
    stream=True
)

for chunk in response:
    print(chunk.choices[0].delta.content or "", end="")
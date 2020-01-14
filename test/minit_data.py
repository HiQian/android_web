import json
from mitmproxy import ctx


def save_to_file(text):
    with open('books.txt', 'a') as f:
        f.write(json.dumps(text, ensure_ascii=False) + '\n')
        f.close()


def response(flow):
    url = 'https://api.weibo.cn/2/searchall?'
    # 如果发送的请求是类似上面分析出的url就进行处理
    if url in flow.request.url:
        # 这两句话是一样的，都是返回返回的结果
        # print(flow.response.text)  # print(flow.response.get_text()
        text = flow.response.text
        # 把str转换为字典处理
        save_to_file(text)
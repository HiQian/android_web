import json
from mitmproxy import ctx
# from mitmproxy import flow


def save_to_file(text):
    with open('books.txt', 'a') as f:
        f.write(json.dumps(text,ensure_ascii=True) + '\n')
        f.close()


def response(flow):
    url = 'https://api.weibo.cn/2/searchall?'
    # 如果发送的请求是类似上面分析出的url就进行处理
    if flow.request.url.startswith(url):
        text = json.loads(flow.response.text)
        datas = text.get('cards')

        ctx.log.warn(str(datas))
        save_to_file(datas)
    # if url in flow.request.url:
    #     # 这两句话是一样的，都是返回返回的结果
    #     # print(flow.response.text)  # print(flow.response.get_text()
    #     text = flow.response.text
    #     # 把str转换为字典处理
    #     data = json.loads(text)
    #     books = data.get('data')
    #     for book in books:
    #         # 在cmd中用颜色输出一下书的信息
    #         ctx.log.warn(str(book))
    #         data = {
    #             'title': book.get('title'),
    #             'author': book.get('author'),
    #             'cover': book.get('cover'),
    #             'tags': book.get('tags')
    #         }
    #         # 存入txt中
    #         save_to_file(data)
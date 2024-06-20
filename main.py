import uvicorn
from fastapi import FastAPI
from tools.searxng import *
from concurrent.futures import ThreadPoolExecutor, as_completed
from concurrent.futures._base import TimeoutError

app = FastAPI()


@app.get("/")
async def index():
   return {"message": "Hello World"}

@app.get("/search")
async def search(query: str, num_results: int = 5):
    print("== query:", query)
    results = get_searx_search_results(query, num_results)
    all_content = ''

    # extract text from html with multi-threading, and get the return value
    with ThreadPoolExecutor(max_workers=len(results)) as executor:
        futures = {executor.submit(extract_text_from_html, result['link']): result for result in results if 'link' in result}

        for future in as_completed(futures):
            try:
                content = future.result()
                if content:
                    all_content += content
            except TimeoutError:
                print(f"抓取超时: {futures[future]['link']}")
                future.cancel()
            except Exception as e:
                print(f"抓取出错: {futures[future]['link']}, 错误: {e}")
                future.cancel()

    # 截取超过7000个字符的部分
    if len(all_content) > 7000:
        all_content = all_content[:7000]

    print("抓取完成")
    return {'content': all_content}


if __name__ == "__main__":
   uvicorn.run("main:app", host="0.0.0.0", port=8300, reload=True)
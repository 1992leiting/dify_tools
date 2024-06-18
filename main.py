import uvicorn
from fastapi import FastAPI
from tools.searxng import *
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

app = FastAPI()


@app.get("/")
async def index():
   return {"message": "Hello World"}

@app.get("/search")
async def search(query: str, num_results: int = 5):
    results = get_searx_search_results(query, num_results)
    all_content = ''

    # extract text from html with multi-threading, and get the return value
    with ThreadPoolExecutor(max_workers=10) as executor:
        for result in results:
            if 'link' not in result:
                continue
            futures = [executor.submit(extract_text_from_html3, result['link'])]
            for future in as_completed(futures):
                content = future.result()
                if content:
                    all_content += content

    if len(all_content) > 7000:
            all_content = all_content[:7000]

    return {'content': all_content}


if __name__ == "__main__":
   uvicorn.run("main:app", host="0.0.0.0", port=8300, reload=True)
from langchain_community.utilities import SearxSearchWrapper
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import trafilatura


search = SearxSearchWrapper(searx_host="http://oracle.leiting6.cn:8080")

def get_searx_search_results(query: str, num_results: int = 5, categories: str = "general") -> list:
    """
    Search the web using Searx and return the results.
    """
    results = search.results(
        query,
        num_results=num_results,
        categories=categories
    )

    return results

def extract_text_from_html3(url: str) -> str:
    try:
        download = trafilatura.fetch_url(url)
        result = trafilatura.extract(download, include_comments=False)
        if not result:
            return None
        blocks = result.split("\n")
        result = "".join([block for block in blocks if len(block) > 20])
        return result
    except:
        return None


# 测试
if __name__ == "__main__":
    results = search.results(
        "小米SU7评价",
        num_results=5,
        categories="science",
        time_range="year",
    )
    
    all_content = ''
    with ThreadPoolExecutor(max_workers=10) as executor:
        for result in results:
            print('-------------------------')
            print(result['title'])
            futures = [executor.submit(extract_text_from_html3, result['link'])]
            for future in as_completed(futures):
                content = future.result()
                if content:
                    all_content += content

    print('****************')
    print(all_content)

    print(len(all_content))

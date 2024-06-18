本项目包含我自己常用的dify工具（已通过fastapi封装成http服务供dify调用）和常用的dify工作流。
# 启动tool server
直接通过main.py启动服务即可
```
pip install -r requirements.txt
python main.py
```
注意：
- 搜索api调用searxng搜索服务，tools/searxng.py中有默认的地址可以使用（不保证长期稳定可用），如果自己已经搭建了searxng服务，也可以进行修改。
# 导入dify工具
Todo
# 导入dify工作流
Todo
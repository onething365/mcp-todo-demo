from typing import Dict, List
import httpx
from mcp.server.fastmcp import FastMCP
from datetime import datetime, timedelta

# 初始化 FastMCP server
mcp = FastMCP(name="todo", host='0.0.0.0', description="获取用户待办事项列表")

# 修改为调用本地FastAPI服务的URL
BASE_URL = "http://localhost:8001/"

def getTodoList(length: int = 5) -> List[Dict[str, str | int]]:
    """
    获取用户待办事项列表
    :param length: 返回的待办事项数量，默认为5
    """
    todo_url = BASE_URL + "todo/list"
    with httpx.Client() as client:
        try:
            # 调用待办列表接口
            response = client.get(todo_url, params={'length': length})
            response.raise_for_status()
            
            # 解析响应
            todo_data = response.json()
            print(f"待办列表响应: {todo_data}")
            return todo_data["data"]
        except httpx.HTTPStatusError as e:
            print(f"HTTP错误: {e}")
            return []
        except httpx.RequestError as e:
            print(f"请求错误: {e}")
            return []
        except Exception as e:
            print(f"其他错误: {e}")
            return []

def addTodoItem(name: str, priority: str = "medium") -> Dict[str, str | int]:
    """
    新增待办事项
    :param name: 待办事项的名称
    :param priority: 优先级，默认为medium
    :return: 新增待办事项的响应数据
    """
    add_todo_url = BASE_URL + "todo/add"
    with httpx.Client() as client:
        try:
            # 调用新增待办事项接口
            response = client.post(add_todo_url, json={'name': name, 'priority': priority})
            response.raise_for_status()
            
            # 解析响应
            add_data = response.json()
            print(f"新增待办事项响应: {add_data}")
            return add_data['data']
        except httpx.HTTPStatusError as e:
            print(f"HTTP错误: {e}")
            return {"error": f"HTTP error: {e}"}
        except httpx.RequestError as e:
            print(f"请求错误: {e}")
            return {"error": f"Request error: {e}"}
        except Exception as e:
            print(f"其他错误: {e}")
            return {"error": f"Other error: {e}"}

@mcp.tool("新增待办事项")
def add_todo(name: str, priority: str = "medium") -> Dict[str, str | int]:
    """
    新增一个待办事项
    :param name: 待办事项的名称
    :param priority: 优先级，可选值为high/medium/low，默认为medium
    """
    return addTodoItem(name, priority)

@mcp.tool("获取用户待办事项列表")
def get_todo_list(length: int = 5) -> List[Dict[str, str | int]]:
    """
    获取待办事项列表
    :param length: 返回的待办事项数量，默认为5
    """
    return getTodoList(length)

@mcp.tool("获取用户超过三天没有完成的待办事项列表")
def get_overdue_todos() -> List[Dict[str, str | int]]:
    """
    获取创建时间超过三天的前五条待办事项
    """
    todo_list = getTodoList()
    
    # 计算3天前的日期时间
    three_days_ago = datetime.now() - timedelta(days=3)
    
    overdue_todos = []
    for todo in todo_list:
        created_time_str = todo.get('created_time')
        if not created_time_str:
            continue
            
        try:
            # 转换ISO格式字符串为datetime对象
            created_time = datetime.fromisoformat(created_time_str)
            if created_time < three_days_ago:
                overdue_todos.append(todo)
        except ValueError:
            continue
            
    # 返回前5条
    return overdue_todos[:5]

if __name__ == "__main__":
    # 初始化并运行服务器
    try:
        print("Starting server...")
        mcp.run(transport='sse')
    except Exception as e:
        print(f"Error: {e}")
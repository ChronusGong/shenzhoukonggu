import pandas as pd
import random
from tqdm import tqdm

df_route = pd.read_excel('data/可用路线.xlsx')
df_route = df_route.dropna()


# 邻接表
adjacency_dict = {}
# 以访问列表
visit_map = {}
start_cities = list(df_route['起始地'].unique())
terminal_cities = list(df_route['目的地'].unique())
# 生成邻接表
for city in start_cities:
    terminals = list(df_route.loc[df_route['起始地'] == city, '目的地'].values)
    adjacency_dict[city] = terminals
    visit_map[city] = 0

for city in terminal_cities:
    visit_map[city] = 0

# path = []
# result_path = []


def dfs(start, end, path, result_path):
    # 表示Start点已经访问过了
    visit_map[start] = 1
    # 访问过的点放入path列表
    path.append(start)
    # # 确保直发在结果集中
    # if end in adjacency_dict[city]:
    #     path.append(end)
    #     result_path.append(path[:])
    #     path.remove(path[-1])
    # 如果当前访问的点是终点，则加入resutl_path
    if start == end:
        result_path.append(path[:])
    else:
        random.shuffle(terminal_cities)
        for c in terminal_cities:
            if len(result_path) == 128:
                break
            if c in start_cities and visit_map[c] == 0 and c != start and c in adjacency_dict[start]:
                dfs(c, end, path, result_path)

    path.remove(path[-1])
    visit_map[start] = 0


def find_route(s, e):
    path = []
    result_path = []
    dfs(s, e, path, result_path)
    if e in adjacency_dict[s] and not [s, e] in result_path:
        result_path.remove(result_path[-1])
        result_path.append([s, e])

    results = []
    for items in result_path:
        routes = []
        for i in range(len(items) -1):
            routes.append(df_route[(df_route['起始地'] == items[i]) & (df_route['目的地'] == items[i + 1])]['线路编号'].values[0])
        results.append(routes)

    return results


def dfs_find_route():
    df_order = pd.read_excel('data/订单.xlsx')
    df_order = df_order.dropna()
    df_order = df_order.loc[~(df_order['起始城市'] == df_order['目的城市'])]
    df_order.reset_index(inplace=True)
    df_order = df_order[['订单号', '起始城市', '目的城市']]
    result_dict = {}
    for index in tqdm(range(len(df_order))):
        start = df_order['起始城市'][index]
        end = df_order['目的城市'][index]
        order_num = df_order['订单号'][index]
        result_path = find_route(start, end)
        result_dict[order_num] = result_path
    return result_dict










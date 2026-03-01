import os
import functools
import json
from link_rep import LinkId

DIRNOW = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIRNOW, "data")
AMPHICHEIRAL = os.path.join(DATA, "amphicheiral")
PD_CODE = os.path.join(DATA, "pd_code")

@functools.cache
def load_amphicheiral() -> set[str]:
    arr = []
    for filename in os.listdir(AMPHICHEIRAL):
        filepath = os.path.join(AMPHICHEIRAL, filename)
        for line in open(filepath, "r"):
            line = line.strip()
            if line == "":
                continue
            arr.append(line)
    return set(arr)

@functools.cache
def load_pd_code() -> dict[str, list[list[int]]]:
    ans = dict()
    for filename in os.listdir(PD_CODE):
        filepath = os.path.join(PD_CODE, filename)
        for line in open(filepath, "r"):
            line = line.strip()
            if line == "":
                continue
            lpart, rpart = line.split(":")
            lpart = lpart.strip()
            rpart = eval(rpart)

            if lpart[0] != "m":
                ans[lpart] = rpart

            else:
                raw_name = lpart[1:]

                # 跳过非手性扭结的镜像扭结
                if raw_name not in load_amphicheiral():
                    ans[lpart] = rpart
    return ans

# 用于获取素扭结排序依据
@functools.cache
def get_link_name_sort_index(link_name:str) -> tuple:
    link_id = LinkId.get_link_id_from_string(link_name)
    return (
        link_id.crossing_num,
        link_id.knot_or_link,
        link_id.alter_or_nonalter,
        link_id.inner_index,
        link_id.mirror,
    )

# 用于给素扭结序列排序
def sort_link_name_list(link_name_list: list[str]) -> list[str]:
    return sorted([
        link_name
        for link_name in link_name_list
    ], key=lambda link_name: get_link_name_sort_index(link_name))

@functools.cache
def get_all_prime_under10() -> list[str]:
    return sort_link_name_list([
        item
        for item in load_pd_code()
    ])

def dfs(
    last_pos:int, 
    cur_cross:int, 
    arr:list[str], 
    sol:list[list[str]], 
    all_knots:list[str], 
    total_crossing:int):

    if cur_cross > total_crossing: # 超过限制了
        return
    
    if len(arr) != 0:
        sol.append(json.loads(json.dumps(arr)))
    
    if cur_cross < total_crossing:
        for i in range(last_pos, len(all_knots)): # 可以重复使用相同的链环
            arr.append(all_knots[i])
            new_crs = int(LinkId.get_link_id_from_string(all_knots[i]).crossing_num)
            dfs(i, cur_cross + new_crs, arr, sol, all_knots, total_crossing)
            arr.pop()
    
# 计算所有组合方案（不考虑顺序）
def get_all_combination(total_crossing:int) -> list[list[str]]:
    all_knots = get_all_prime_under10()
    sol = []
    arr = []
    last_pos =  0 # 上一个被选中的素分量，在所有素分量中的位置
    cur_cross = 0 # 目前已经有多少个交叉点了
    dfs(last_pos,cur_cross, arr, sol, all_knots, total_crossing)
    return sol


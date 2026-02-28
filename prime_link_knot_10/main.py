import os
import functools
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

@functools.cache
def get_all_prime_under10() -> list[str]:
    def get_sort_tuple(link_name:str) -> tuple:
        link_id = LinkId.get_link_id_from_string(link_name)
        return (
            link_id.crossing_num,
            link_id.knot_or_link,
            link_id.alter_or_nonalter,
            link_id.inner_index,
            link_id.mirror,
        )

    return sorted([
        item
        for item in load_pd_code()
    ], key=lambda link_name: get_sort_tuple(link_name))

if __name__ == "__main__":
    for line in get_all_prime_under10():
        print(line)

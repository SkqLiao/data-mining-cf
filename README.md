# CF Statistics for Data Mining

## 功能 1

Codeforces 指定用户集合过题数目Top K（可以设置筛选题目的rating下限）

- `handles.txt` ：用户名集合，当前为某年CNOI国家集训队
- `data/{handle}.json` ：`handle` 用户的过题信息（来自`api.codeforces.com`）
- `top_k_problem{datetime}.txt`：筛选题目信息，按照过题次数排序，显示题目rating

Codeforces API使用说明：https://codeforces.com/apiHelp/objects#ProblemStatistics


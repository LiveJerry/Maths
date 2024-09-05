import numpy as np
from scipy.stats import binom

# 参数设定
n = 1000  # 抽样数量
p_nominal = 0.1  # 次品率标称值
confidence_95_reject = 0.95  # 95%置信水平下认定次品率超过标称值
confidence_90_accept = 0.90  # 90%置信水平下认定次品率不超过标称值

# 寻找95%置信水平下的临界值，即在实际次品率超过标称值时拒绝的概率
def find_critical_value_to_reject(confidence, n, p):
    for x in range(n + 1):
        if binom.cdf(x, n, p) < confidence:
            continue
        else:
            return x - 1
    return n

# 寻找90%置信水平下的临界值，即在实际次品率不超过标称值时接受的概率
def find_critical_value_to_accept(confidence, n, p):
    for x in range(n + 1):
        if binom.cdf(x, n, p) >= confidence:
            return x
    return n

# 计算临界值
critical_value_reject = find_critical_value_to_reject(confidence_95_reject, n, p_nominal)
critical_value_accept = find_critical_value_to_accept(confidence_90_accept, n, p_nominal)

# 输出结果
print(f"在95%的置信水平下，如果在1000份样本中检测到的次品数大于{critical_value_reject}，则认为次品率超过标称值10%，应当拒收这批零配件。")
print(f"在90%的置信水平下，如果在1000份样本中检测到的次品数不大于{critical_value_accept}，则认为次品率不超过标称值10%，应当接收这批零配件。")
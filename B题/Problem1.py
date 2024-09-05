import scipy.stats as stats

def calculate_critical_values(max_sample_size, p0, confidence_level, increment=1000):
    results = []
    for n in range(increment, max_sample_size + 1, increment):
        # 使用二项分布的PPF函数来确定临界值
        # 注意：对于95%置信水平下的拒绝次品率超过标称值，我们取1 - 0.05 = 0.95的下限
        # 对于90%置信水平下的接受次品率不超过标称值，我们取0.90的下限
        k = stats.binom.ppf(confidence_level, n, p0)
        results.append((n, k))
    return results

# 给定的参数
p0 = 0.10  # 声明的次品率
max_sample_size = 10000  # 最大样本量
increment = 1000  # 每次增加的样本量

# 计算95%置信水平下的样本大小和临界值（用于拒绝次品率超过标称值）
critical_values_95_reject = calculate_critical_values(max_sample_size, p0, 0.95, increment)

# 计算90%置信水平下的样本大小和临界值（用于接受次品率不超过标称值）
critical_values_90_accept = calculate_critical_values(max_sample_size, p0, 0.90, increment)

print("在95%的置信水平下（拒绝次品率超过标称值）：")
for n, k in critical_values_95_reject:
    print(f"样本大小 {n}，临界值 {k}")

print("\n在90%的置信水平下（接受次品率不超过标称值）：")
for n, k in critical_values_90_accept:
    print(f"样本大小 {n}，临界值 {k}")
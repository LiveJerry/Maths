import numpy as np
from scipy.stats import binom

# 参数设置
claimed_defect_rate = 0.1  # 标称次品率
confidence_95 = 0.95  # 95%信度
confidence_90 = 0.90  # 90%信度
max_sample_size = 10000  # 最大样本量
true_defect_rate = 0.1  # 假设实际次品率为标称值
num_simulations = 100000  # 增加模拟次数以减少随机性的影响


# 蒙特卡洛模拟函数
def monte_carlo_simulation(defect_rate, confidence_level, max_sample_size, num_simulations):
    sample_sizes = np.arange(1, max_sample_size + 1)
    results = []
    min_sample_size = None
    min_exceed_ratio = None

    for sample_size in sample_sizes:
        # 模拟num_simulations次
        simulations = binom.rvs(sample_size, defect_rate, size=num_simulations)
        # 计算样本中次品数量超过预期的次数
        exceed_count = np.sum(simulations > binom.ppf(confidence_level, sample_size, claimed_defect_rate))
        exceed_ratio = exceed_count / num_simulations

        # 如果超过预期的次数占总次数的比例大于1-置信水平，则该样本大小足以做出判断
        if exceed_ratio >= 1 - confidence_level:
            if min_sample_size is None or sample_size < min_sample_size:
                min_sample_size = sample_size
                min_exceed_ratio = exceed_ratio
                # 只记录最小样本大小
                results.clear()
                results.append((sample_size, exceed_ratio))
            elif sample_size == min_sample_size:
                results.append((sample_size, exceed_ratio))
            else:
                break

    return results, min_sample_size, min_exceed_ratio


# 多次运行并取平均
num_runs = 100  # 运行次数
min_sample_sizes_95 = []
min_sample_sizes_90 = []

for _ in range(num_runs):
    # 95%信度下的模拟
    results_95, min_sample_size_95, min_exceed_ratio_95 = monte_carlo_simulation(true_defect_rate, 1 - confidence_95,
                                                                                 max_sample_size, num_simulations)
    min_sample_sizes_95.append(min_sample_size_95)

    # 90%信度下的模拟
    results_90, min_sample_size_90, min_exceed_ratio_90 = monte_carlo_simulation(true_defect_rate, 1 - confidence_90,
                                                                                 max_sample_size, num_simulations)
    min_sample_sizes_90.append(min_sample_size_90)

# 输出结果
print("在95%信度下:")
print(f"多次运行得到的最小样本量: {min_sample_sizes_95}")
print(f"平均最小样本量: {np.mean(min_sample_sizes_95)}")

print("\n在90%信度下:")
print(f"多次运行得到的最小样本量: {min_sample_sizes_90}")
print(f"平均最小样本量: {np.mean(min_sample_sizes_90)}")
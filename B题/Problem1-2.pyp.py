from scipy.stats import binom

claimed_defect_rate = 0.1  # 标称次品率
sample_size_95 = 150  # 样本大小
alpha_95 = 0.05  # 1 - 信度水平
sample_size_90 = 146  # 样本大小
alpha_90 = 0.10  # 1 - 信度水平

critical_value_95 = binom.ppf(1 - alpha_95, sample_size_95, claimed_defect_rate)
critical_value_90 = binom.ppf(1 - alpha_90, sample_size_90, claimed_defect_rate)

print(f"在95%信度下，临界值为：{critical_value_95}")
print(f"在90%信度下，临界值为：{critical_value_90}")
import numpy as np

# 表1数据结构化
data = [
    {
        'situation': 1,
        'p1': 0.1, 'c1': 4, 'd1': 2,  # 零配件1次品率、购买单价、检测成本
        'p2': 0.1, 'c2': 18, 'd2': 3,  # 零配件2次品率、购买单价、检测成本
        'pf': 0.1, 'af': 6, 'df': 3,  # 成品次品率、装配成本、检测成本
        'ms': 56,  # 市场售价
        'tl': 6, 'dc': 5  # 调换损失、拆解费用
    },
    {
        'situation': 2,
        'p1': 0.2, 'c1': 4, 'd1': 2,
        'p2': 0.2, 'c2': 18, 'd2': 3,
        'pf': 0.2, 'af': 6, 'df': 3,
        'ms': 56,
        'tl': 6, 'dc': 5
    },
    {
        'situation': 3,
        'p1': 0.1, 'c1': 4, 'd1': 2,
        'p2': 0.1, 'c2': 18, 'd2': 3,
        'pf': 0.1, 'af': 6, 'df': 3,
        'ms': 56,
        'tl': 30, 'dc': 5
    },
    {
        'situation': 4,
        'p1': 0.2, 'c1': 4, 'd1': 1,
        'p2': 0.2, 'c2': 18, 'd2': 1,
        'pf': 0.2, 'af': 6, 'df': 2,
        'ms': 56,
        'tl': 30, 'dc': 5
    },
    {
        'situation': 5,
        'p1': 0.1, 'c1': 4, 'd1': 8,
        'p2': 0.2, 'c2': 18, 'd2': 1,
        'pf': 0.1, 'af': 6, 'df': 2,
        'ms': 56,
        'tl': 10, 'dc': 5
    },
    {
        'situation': 6,
        'p1': 0.05, 'c1': 4, 'd1': 2,
        'p2': 0.05, 'c2': 18, 'd2': 3,
        'pf': 0.05, 'af': 6, 'df': 3,
        'ms': 56,
        'tl': 10, 'dc': 40
    }
]

# 取第一条数据
situation_data = data[0]
p1, c1, d1 = situation_data['p1'], situation_data['c1'], situation_data['d1']
p2, c2, d2 = situation_data['p2'], situation_data['c2'], situation_data['d2']
pf, af, df = situation_data['pf'], situation_data['af'], situation_data['df']
ms, tl, dc = situation_data['ms'], situation_data['tl'], situation_data['dc']

# 假设购买数量
num_p1 = num_p2 = 100

# 动态规划表
dp = np.zeros((2, 2, 2))  # 2状态: 检测/不检测, 2个零配件, 2种成品状态(合格/不合格)


def dynamic_programming(inspect_p1, inspect_p2, inspect_final, num_p1, num_p2):
    # 计算每个状态下的期望成本和收益
    # 零配件1的成本
    cost_p1 = num_p1 * c1
    if inspect_p1:
        cost_p1 += num_p1 * d1
        num_p1_good = num_p1 * (1 - p1)  # 合格数量
    else:
        num_p1_good = num_p1 * (1 - p1)  # 如果不检测，只算合格的数量

    # 零配件2的成本
    cost_p2 = num_p2 * c2
    if inspect_p2:
        cost_p2 += num_p2 * d2
        num_p2_good = num_p2 * (1 - p2)  # 合格数量
    else:
        num_p2_good = num_p2 * (1 - p2)  # 如果不检测，只算合格的数量

    # 只有当两个零配件都是合格的才能装配成品
    num_good_pairs = min(num_p1_good, num_p2_good)

    # 使用期望装配数量
    expected_assembly = int(num_good_pairs)  # 取整数部分

    # 装配成本
    assembly_cost = expected_assembly * af

    # 成品检测成本
    detection_cost = expected_assembly * df * inspect_final

    # 销售收益
    sale_revenue = expected_assembly * (1 - pf) * ms

    # 调换损失和拆解成本
    replacement_loss = expected_assembly * pf * tl
    disassembly_cost = expected_assembly * pf * dc * (1 if inspect_final else 0)

    # 如果拆解成品，重置零配件数量
    if inspect_final == 1:
        num_p1 = expected_assembly * pf
        num_p2 = expected_assembly * pf

        # 递归调用动态规划函数
        new_profit = dynamic_programming(inspect_p1, inspect_p2, inspect_final, num_p1, num_p2)
        return new_profit

    # 总成本
    total_cost = cost_p1 + cost_p2 + assembly_cost + detection_cost + replacement_loss + disassembly_cost
    # 总收益
    total_revenue = sale_revenue

    # 利润
    profit = total_revenue - total_cost

    # 更新动态规划表
    dp[inspect_p1][inspect_p2][inspect_final] = profit

    return profit


# 动态规划递推公式
for inspect_p1 in [0, 1]:  # 零配件1是否检测
    for inspect_p2 in [0, 1]:  # 零配件2是否检测
        for inspect_final in [0, 1]:  # 成品是否检测
            # 调用动态规划函数
            final_profit = dynamic_programming(inspect_p1, inspect_p2, inspect_final, num_p1, num_p2)

# 根据最终状态获取最优解
optimal_decision = np.unravel_index(np.argmax(dp), dp.shape)
print("最优决策:", optimal_decision)
print("最大利润:", np.max(dp))
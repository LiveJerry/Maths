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
    }
]

# 定义数据结构
class Scenario:
    def __init__(self, situation, p1, c1, d1, p2, c2, d2, pf, af, df, ms, tl, dc):
        self.situation = situation
        self.p1 = p1  # 零配件1次品率
        self.c1 = c1  # 零配件1购买单价
        self.d1 = d1  # 零配件1检测成本
        self.p2 = p2  # 零配件2次品率
        self.c2 = c2  # 零配件2购买单价
        self.d2 = d2  # 零配件2检测成本
        self.pf = pf  # 成品次品率
        self.af = af  # 装配成本
        self.df = df  # 成品检测成本
        self.ms = ms  # 市场售价
        self.tl = tl  # 调换损失
        self.dc = dc  # 拆解费用


# 动态规划函数

# 动态规划函数
import numpy as np

# 数据结构保持不变
data = [
    {
        'situation': 1,
        'p1': 0.1, 'c1': 4, 'd1': 2,  # 零配件1次品率、购买单价、检测成本
        'p2': 0.1, 'c2': 18, 'd2': 3,  # 零配件2次品率、购买单价、检测成本
        'pf': 0.1, 'af': 6, 'df': 3,  # 成品次品率、装配成本、检测成本
        'ms': 56,  # 市场售价
        'tl': 6, 'dc': 5  # 调换损失、拆解费用
    }
]

class Scenario:
    def __init__(self, situation, p1, c1, d1, p2, c2, d2, pf, af, df, ms, tl, dc):
        self.situation = situation
        self.p1 = p1  # 零配件1次品率
        self.c1 = c1  # 零配件1购买单价
        self.d1 = d1  # 零配件1检测成本
        self.p2 = p2  # 零配件2次品率
        self.c2 = c2  # 零配件2购买单价
        self.d2 = d2  # 零配件2检测成本
        self.pf = pf  # 成品次品率
        self.af = af  # 装配成本
        self.df = df  # 成品检测成本
        self.ms = ms  # 市场售价
        self.tl = tl  # 调换损失
        self.dc = dc  # 拆解费用

# 动态规划函数
def dp_decision(scenario):
    n = 100  # 假设零配件的数量为100
    # 状态转移矩阵，新增了拆解后的状态
    dp = np.zeros((2, 2, 2, 2, 2, 2))

    # 初始化
    dp[0][0][0][0][0][0] = -np.inf  # 不检测任何零件和成品的情况初始化为负无穷
    tests_p1 = 0;
    tests_p2 = 0;
    test_ff = 0;
    # 判断是否检测零件
    more_profit = n * scenario.p2 * (1 - scenario.p1) * scenario.ms
    if scenario.af > min((scenario.d1 / scenario.p1), (scenario.d2 / scenario.p2)):
        if (scenario.d1 / scenario.p1) > (scenario.d2 / scenario.p2):
            if (more_profit - 2 * n * (1 - scenario.p2) * scenario.af):
                test_p1 = 1
                test_p2 = 1
                # 删除不合格零件
                af_n = n - max(n * scenario.p1, n * scenario.p2)
                scenario.p1 = 0
                scenario.p2 = 0
            else:
                #选择单独检测零件2
                test_p1 = 0
                test_p2 = 1
                af_n = n - n * scenario.p2
                scenario.p2 = 0
        else:
            if more_profit - n * scenario.d2 + (scenario.p1 - scenario.p2) * n * scenario.af:
                test_p1 = 1
                test_p2 = 1
                # 删除不合格零件
                af_n = n - max(n * scenario.p1, n * scenario.p2)
                scenario.p1 = 0
                scenario.p2 = 0
            else:
                #选择单独检测零件1
                test_p1 = 1
                test_p2 = 0
                af_n = n - n*scenario.p1
                scenario.p1 = 0
    else:
        #都不选和都选的比较
        if more_profit - ((scenario.d1 + scenario.d2) * n + scenario.p2 * scenario.af):
            test_p1 = 1
            test_p2 = 1
            # 删除不合格零件
            af_n = n - max(n * scenario.p1, n * scenario.p2)
            scenario.p1 = 0
            scenario.p2 = 0
        else:
            test_p1 = 0
            test_p2 = 0

    # 对于每种是否检测成品的情况
    for test_f in range(2):  # 是否检测成品
        # 计算期望收益
        exp_good_p1 = af_n * (1 - scenario.p1)
        exp_good_p2 = af_n * (1 - scenario.p2)

        # 只有当两个零配件都是好的时候，成品才可能是好的
        if test_p1 == 1 and test_p2 == 1:
            # exp_f为制作的所有成品的数量
            exp_f = af_n
            exp_good_f = exp_f * (1 - scenario.pf)
        else:
            exp_f = af_n * (1 - scenario.p1) * (1 - scenario.p2)
            exp_good_f = exp_f * (1 - scenario.pf)

        # 总成本包括购买成本、检测零配件成本、检测成品成本、装配成本
        total_cost =  n * (scenario.c1 + scenario.c2) + \
                      (test_p1 * scenario.d1 + test_p2 * scenario.d2) * n + \
                     (test_f * scenario.df) * exp_f + \
                     scenario.af * exp_f

        # 总收入
        revenue = scenario.ms * exp_good_f

        # 期望收益
        exp_profit = revenue - total_cost

        # 检测是否需要拆解
        if test_f:
            # 重置零配件1的数量以及次品率
            exp_bad = af_n - exp_good_f
            aft_n1 = exp_bad - (af_n * scenario.p1)
            aft_n2 = exp_bad - (af_n * scenario.p2)
            aft_n = min(aft_n1, aft_n2)
            p1_new = 1 - aft_n1 / exp_bad
            p2_new = 1 - aft_n2 / exp_bad
            aft_cost = 0

            # 重新检测决策一
            more_profit = (exp_bad - aft_n1) * scenario.p2 * (1 - scenario.p1) * scenario.ms
            if test_p1 == 1 and test_p2 == 1:
                continue
            elif scenario.af > min((scenario.d1 / p1_new), (scenario.d2 / p2_new)):
                if (scenario.d1 / p1_new) > (scenario.d2 / p2_new) and test_p2 != 0:
                    if (more_profit - 2 * n * (1 - scenario.p2) * scenario.af) and test_p1 != 0:
                        tests_p1 = 1
                        tests_p2 = 1
                    else:
                        # 选择单独检测零件2
                        tests_p1 = 0
                        tests_p2 = 1
                else:
                    if more_profit - n * scenario.d2 + (scenario.p1 - scenario.p2) * n * scenario.af and test_p2 != 0:
                        tests_p1 = 1
                        tests_p2 = 1
                    else  :
                        # 选择单独检测零件1
                        tests_p1 = 1
                        tests_p2 = 0
            else:
                # 都不选和都选的比较
                if more_profit - ((scenario.d1 + scenario.d2) * n + scenario.p2 * scenario.af) and test_p1 != 0 and test_p2 != 0:
                    tests_p1 = 1
                    tests_p2 = 1
                else:
                    tests_p1 = 0
                    tests_p2 = 0

            # 重新成品是否检测
            for test_ff in range(2):
                if tests_p1 == 1 and tests_p2 == 1:
                    # exp_ff为制作的所有成品的数量
                    exp_ff = exp_bad - aft_n1
                    exp_good_ff = exp_ff * (1 - scenario.pf)
                else:
                    exp_ff = exp_bad * (1 - p1_new) * (1 - p2_new)
                    exp_good_ff = exp_ff * (1 - scenario.pf)
                # 检测成品成本 + 装配成本 + 检测零件成本 + 拆解成本
                aft_cost = (test_ff * scenario.df) * exp_ff + \
                           scenario.af * exp_good_ff + \
                          tests_p1 * scenario.d1 * aft_n1 + tests_p2 * scenario.d2 * aft_n2 + \
                          exp_bad * scenario.dc

                exp_profit = min(exp_profit + exp_good_ff * scenario.ms - aft_cost, exp_profit)

        # 更新dp矩阵
        dp[test_p1][test_p2][test_f][tests_p1][tests_p2][test_ff] = exp_profit

    # 返回最优决策
    return np.unravel_index(np.argmax(dp), dp.shape), np.max(dp)

# 将数据转换为Scenario对象
scenarios = [Scenario(**datum) for datum in data]

# 运行决策函数
for s in scenarios:
    print(f"Situation {s.situation}:")
    opt_policy, max_profit = dp_decision(s)
    print(f"Optimal policy is to test P1={opt_policy[0]}, test P2={opt_policy[1]}, test F={opt_policy[2]},")
    print(f"After disassembly test P1={opt_policy[3]}, test P2={opt_policy[4]}, test F={opt_policy[5]}")
    print(f"Maximum expected profit: {max_profit:.2f} 元")

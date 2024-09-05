from itertools import product

# 表 1 中的数据
situations = [
    {'situation': 1, 'defect_rate_1': 0.10, 'purchase_price_1': 4, 'inspection_cost_1': 2,
     'defect_rate_2': 0.10, 'purchase_price_2': 18, 'inspection_cost_2': 3,
     'defect_rate_product': 0.10, 'assembly_cost': 6, 'inspection_cost_product': 3,
     'market_price': 56, 'replacement_loss': 6, 'disassembly_cost': 5},
    {'situation': 2, 'defect_rate_1': 0.20, 'purchase_price_1': 4, 'inspection_cost_1': 2,
     'defect_rate_2': 0.20, 'purchase_price_2': 18, 'inspection_cost_2': 3,
     'defect_rate_product': 0.20, 'assembly_cost': 6, 'inspection_cost_product': 3,
     'market_price': 56, 'replacement_loss': 6, 'disassembly_cost': 5},
    {'situation': 3, 'defect_rate_1': 0.10, 'purchase_price_1': 4, 'inspection_cost_1': 2,
     'defect_rate_2': 0.10, 'purchase_price_2': 18, 'inspection_cost_2': 3,
     'defect_rate_product': 0.10, 'assembly_cost': 6, 'inspection_cost_product': 3,
     'market_price': 56, 'replacement_loss': 30, 'disassembly_cost': 5},
    {'situation': 4, 'defect_rate_1': 0.20, 'purchase_price_1': 4, 'inspection_cost_1': 1,
     'defect_rate_2': 0.20, 'purchase_price_2': 18, 'inspection_cost_2': 1,
     'defect_rate_product': 0.20, 'assembly_cost': 6, 'inspection_cost_product': 2,
     'market_price': 56, 'replacement_loss': 30, 'disassembly_cost': 5},
    {'situation': 5, 'defect_rate_1': 0.10, 'purchase_price_1': 4, 'inspection_cost_1': 8,
     'defect_rate_2': 0.20, 'purchase_price_2': 18, 'inspection_cost_2': 1,
     'defect_rate_product': 0.10, 'assembly_cost': 6, 'inspection_cost_product': 2,
     'market_price': 56, 'replacement_loss': 10, 'disassembly_cost': 5},
    {'situation': 6, 'defect_rate_1': 0.05, 'purchase_price_1': 4, 'inspection_cost_1': 2,
     'defect_rate_2': 0.05, 'purchase_price_2': 18, 'inspection_cost_2': 3,
     'defect_rate_product': 0.05, 'assembly_cost': 6, 'inspection_cost_product': 3,
     'market_price': 56, 'replacement_loss': 10, 'disassembly_cost': 40}
]


# 生成所有可能的决策组合
def generate_decisions():
    options = [True, False]
    all_combinations = list(product(options, repeat=4))  # 生成所有组合
    decisions = []
    for combination in all_combinations:
        decision = {
            'inspect_part_1': combination[0],
            'inspect_part_2': combination[1],
            'inspect_product': combination[2],
            'disassemble_defective_product': combination[3]
        }
        decisions.append(decision)
    return decisions


# 计算总成本
def calculate_total_costs(situation, decision):
    inspection_cost_1 = situation['inspection_cost_1'] if decision['inspect_part_1'] else 0
    inspection_cost_2 = situation['inspection_cost_2'] if decision['inspect_part_2'] else 0
    inspection_cost_product = situation['inspection_cost_product'] if decision['inspect_product'] else 0
    disassembly_cost = situation['disassembly_cost'] if decision['disassemble_defective_product'] else 0

    total_costs = (
            situation['purchase_price_1'] + inspection_cost_1 +
            situation['purchase_price_2'] + inspection_cost_2 +
            situation['assembly_cost'] + inspection_cost_product +
            disassembly_cost + situation['replacement_loss']
    )

    return total_costs


# 计算利润
def calculate_profit(situation, total_costs):
    return situation['market_price'] - total_costs


# 输出决策结果和效益对比
all_decisions = generate_decisions()

for situation in situations:
    best_profit = float('-inf')
    best_decision = None

    for decision in all_decisions:
        total_costs = calculate_total_costs(situation, decision)
        profit = calculate_profit(situation, total_costs)

        if profit > best_profit:
            best_profit = profit
            best_decision = decision

        print(f"决策: {decision}")
        print(f"总成本: {total_costs:.2f}")
        print(f"利润: {profit:.2f}\n")

    print(f"最佳决策: {best_decision}")
    print(f"最大利润: {best_profit:.2f}\n")
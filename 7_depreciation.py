"""固定资产折旧计算脚本（直线法）

直线法（平均年限法）每年折旧额计算公式：
    残值 = 原值 × 残值率
    每年折旧额 = (原值 - 残值) / 使用年限
              = 原值 × (1 - 残值率) / 使用年限
"""


def get_positive_float(prompt: str) -> float:
    """读取一个大于 0 的浮点数，输入非法时提示重新输入。"""
    while True:
        value = input(prompt).strip()
        try:
            number = float(value)
        except ValueError:
            print("输入无效，请输入数字。")
            continue
        if number <= 0:
            print("输入无效，请输入大于 0 的数字。")
            continue
        return number


def get_rate(prompt: str) -> float:
    """读取残值率，取值范围 [0, 100)，表示百分比。"""
    while True:
        value = input(prompt).strip()
        try:
            rate = float(value)
        except ValueError:
            print("输入无效，请输入数字。")
            continue
        if rate < 0 or rate >= 100:
            print("输入无效，残值率应在 0（含）到 100（不含）之间。")
            continue
        return rate


def straight_line_depreciation(cost: float, residual_rate: float, life_years: float) -> float:
    """按直线法计算每年折旧额。

    Args:
        cost: 固定资产原值。
        residual_rate: 残值率（百分比，如 5 表示 5%）。
        life_years: 使用年限（年）。

    Returns:
        每年折旧额。
    """
    residual_value = cost * residual_rate / 100.0
    annual_depreciation = (cost - residual_value) / life_years
    return annual_depreciation


def main() -> None:
    print("=== 固定资产折旧计算（直线法） ===")

    cost = get_positive_float("请输入固定资产原值：")
    residual_rate = get_rate("请输入残值率（%，例如 5 表示 5%）：")
    life_years = get_positive_float("请输入使用年限（年）：")

    residual_value = cost * residual_rate / 100.0
    annual_depreciation = straight_line_depreciation(cost, residual_rate, life_years)

    print("\n=== 计算结果 ===")
    print(f"固定资产原值：{cost:,.2f}")
    print(f"残值率：{residual_rate:.2f}%")
    print(f"预计净残值：{residual_value:,.2f}")
    print(f"使用年限：{life_years:.2f} 年")
    print(f"每年折旧额：{annual_depreciation:,.2f}")


if __name__ == "__main__":
    main()

"""被动收入追踪器"""

from datetime import datetime
import json


class IncomeStream:
    """收入流记录，追踪单个被动收入来源的详细信息。"""

    def __init__(self, name: str, stream_type: str, monthly: float,
                 setup_cost: float, hours_per_month: float = 0):
        """初始化收入流。

        Args:
            name: 收入流名称，如"电子书销售"
            stream_type: 收入类型，如"数字产品"、"投资收益"
            monthly: 月收入金额（元）
            setup_cost: 初期投入成本（元）
            hours_per_month: 每月维护投入时间（小时）
        """
        self.name = name
        self.type = stream_type
        self.monthly = monthly
        self.setup_cost = setup_cost
        self.hours = hours_per_month

    @property
    def hourly_rate(self) -> float:
        """计算有效时薪，即每小时投入产生的收入。

        Returns:
            有效时薪（元/小时），无投入时返回无穷大
        """
        return self.monthly / self.hours if self.hours > 0 else float("inf")

    @property
    def roi_months(self) -> float:
        """计算回本周期，即投入成本收回所需月数。

        Returns:
            回本月数，月收入为零时返回无穷大
        """
        return self.setup_cost / self.monthly if self.monthly > 0 else float("inf")


class IncomeTracker:
    """被动收入追踪器，汇总多个收入流并生成统计报告。"""

    STREAM_TYPES = {
        "数字产品": "高",
        "投资收益": "高",
        "广告收入": "中",
        "联盟营销": "中",
        "课程收入": "中",
        "咨询服务": "低",
    }

    def __init__(self):
        """初始化追踪器，创建空收入流列表。"""
        self.streams = []

    def add(self, stream: IncomeStream):
        """添加一个收入流到追踪器。

        Args:
            stream: IncomeStream 实例

        Returns:
            返回自身以支持链式调用
        """
        self.streams.append(stream)
        return self

    def total_monthly(self) -> float:
        """计算所有收入流的月收入总和。

        Returns:
            月收入总额（元）
        """
        return sum(s.monthly for s in self.streams)

    def total_hours(self) -> float:
        """计算所有收入流的月投入时间总和。

        Returns:
            月投入总时间（小时）
        """
        return sum(s.hours for s in self.streams)

    def summary(self) -> str:
        """生成收入流统计报告。

        Returns:
            格式化的文本报告，包含收入明细、时薪、回本周期等
        """
        lines = [
            f"被动收入追踪 — {datetime.now().strftime('%Y-%m')}",
            f"{'='*50}",
            f"月收入流: {len(self.streams)} 条",
            f"被动总收入: ¥{self.total_monthly():.0f}/月",
            f"月投入: {self.total_hours():.0f} 小时",
            f"有效时薪: ¥{self.total_monthly() / max(self.total_hours(), 1):.0f}/h",
            "",
            "收入明细:",
        ]
        for s in sorted(self.streams, key=lambda x: -x.monthly):
            passive_label = "🟢" if s.hours < 5 else "🟡" if s.hours < 20 else "🔴"
            lines.append(f"  {passive_label} {s.name:20s} ¥{s.monthly:>6.0f}/月 | "
                         f"投入{s.hours:.0f}h/月 | 回本周{s.roi_months:.0f}月")
        return "\n".join(lines)


if __name__ == "__main__":
    tracker = IncomeTracker()
    tracker \
        .add(IncomeStream("电子书销售", "数字产品", 3000, 20000, 5)) \
        .add(IncomeStream("在线课程", "数字产品", 5000, 30000, 15)) \
        .add(IncomeStream("基金分红", "投资收益", 1500, 100000, 0.5)) \
        .add(IncomeStream("广告联盟", "广告收入", 2000, 0, 10))
    print(tracker.summary())

from datetime import datetime

class TimingTriggerUtils():
    def __init__(self, **kwargs):
        """
        初始化 TimingTriggerUtils 實例。

        參數：
        - triggers_per_hour (int): 每小時觸發點的次數。
        - deviation_second (int): 時間的偏差值（以秒為單位）。
        - another_property (Any): 一個額外的屬性，用於...

        返回：
        - None
        """
        self._triggers_per_hour = kwargs.get('triggers_per_hour', 4)
        self._deviation_second = kwargs.get('deviation_second', 2)

    @property
    def triggers_per_hour(self):
        return self._triggers_per_hour

    @triggers_per_hour.setter
    def triggers_per_hour(self, value):
        self._triggers_per_hour = value

    @property
    def deviation_second(self):
        return self._deviation_second

    @deviation_second.setter
    def deviation_second(self, value):
        self._deviation_second = value

    def get_seconds_until_next_hourly_trigger(self, current_time):
        current_minute = current_time.minute
        current_second = current_time.second

        # 計算離下一個按小時觸發點的時間，並加上偏差
        seconds_until_next_hourly_trigger = (
            (60 - current_minute % (60 / self.triggers_per_hour)) /
            (60 / self.triggers_per_hour) * 60 - current_second + self.deviation_second
        ) % (60 * 60)

        return seconds_until_next_hourly_trigger

def format_datetime(timestamp):
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
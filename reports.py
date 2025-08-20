from abc import ABC, abstractmethod
class Report(ABC):
    def __init__(self, data):
        self.data = data

    @abstractmethod
    def generate(self):
        raise NotImplementedError("Метод generate должен быть реализован в подклассах.")

class AverageResponseTimeReport(Report):
    def generate(self):
        report_rows = []
        for endpoint, data in self.data.items():
            count = data['count']
            total_time = data['total_time']
            avg_time = total_time / count if count > 0 else 0
            report_rows.append([endpoint, count, f"{avg_time:.3f}"])
        headers = ['Endpoint', 'Number of Requests', 'Average Response Time (s)']
        return headers, report_rows

class CountRequestsReport(Report):
    def generate(self):
        report_rows = []
        for endpoint, data in self.data.items():
            count = data['count']
            report_rows.append([endpoint, count])
        headers = ['Endpoint', 'Number of Requests']
        return headers, report_rows

class UserAgentReport(Report):
    def generate(self):
        from collections import defaultdict
        user_agents_count = defaultdict(int)
        for entry in self.data:
            ua = entry.get('http_user_agent', 'Unknown')
            user_agents_count[ua] += 1
        report_rows = [[ua, count] for ua, count in user_agents_count.items()]
        headers = ['User-Agent', 'Count']
        return headers, report_rows
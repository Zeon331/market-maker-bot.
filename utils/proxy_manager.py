import random

class ProxyManager:
    def __init__(self, proxy_list=None):
        self.proxy_list = proxy_list or []
        self.current_proxy = None
    
    def get_proxy(self):
        if not self.proxy_list:
            return None
        self.current_proxy = random.choice(self.proxy_list)
        return {
            "http": f"http://{self.current_proxy}",
            "https": f"http://{self.current_proxy}"
        }
    
    def report_bad_proxy(self):
        if self.current_proxy in self.proxy_list:
            self.proxy_list.remove(self.current_proxy)
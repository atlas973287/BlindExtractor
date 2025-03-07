class AbstractStrategy:
    def send_payload(self, payload, timeout=10):
        """Send the payload and return True/False based on the result"""
        raise NotImplementedError("Subclasses must implement this method")
    
    def create_length_check_payload(self, cmd, length):
        """Create a payload to check if output length is >= length"""
        raise NotImplementedError("Subclasses must implement this method")
    
    def create_char_check_payload(self, cmd, position, char_value):
        """Create a payload to check if character at position equals char_value"""
        raise NotImplementedError("Subclasses must implement this method")
    
    def create_char_less_than_payload(self, cmd, position, char_value):
        """Create a payload to check if character at position is less than char_value"""
        raise NotImplementedError("Subclasses must implement this method")
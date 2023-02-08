
class ErrorResponse:

    def __init__(self, data):
        self.data = data

    def check_which_error(self):
        print(self.data)
        error_keys = [k for k, v in self.data.items() if v == False]
        print(error_keys)
        return error_keys
    
    def prepare_error_response(self, VALID_TYPE_OF_ENDPOINT):
        error_response = {}
        error_keys = self.check_which_error()
        for key in error_keys:
            if key == "INPUT_VALIDATION_FAILED":
                error_response["INPUT_VALIDATION_FAILED"] = f'Failed for keys {self.data["INPUT_VALIDATION_FAILED"]}'
            if key == "TYPE_OF_ENDPOINT_ALLOWED":
                error_response["TYPE_OF_ENDPOINT_ALLOWED"] = f'Allowed endpoint type is {VALID_TYPE_OF_ENDPOINT}'
            if key == "EVENT_CONTRACT":
                error_response["EVENT_CONTRACT"] = "Event contract is empty"
        return error_response
            

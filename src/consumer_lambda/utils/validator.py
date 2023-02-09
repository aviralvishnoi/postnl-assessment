class Validator:

    def __init__(self, data, valid_type_of_endpoint):
        self.data = data
        self.valid_type_of_endpoint = valid_type_of_endpoint

    def validate_type_of_endpoint(self):
        endpoint_type = self.data.get("type_of_endpoint", None)
        if endpoint_type not in self.valid_type_of_endpoint:
            return self.valid_type_of_endpoint
        else:
            return True

    def validate_data(self):
        empty_keys = [k for k, v in self.data.items() if v == ""]
        if empty_keys:
            return empty_keys
        else:
            return True

    def validate_event_contract(self):
        event_contract = self.data.get("event_contract", None)
        if event_contract:
            return True
        else:
            return False

    def validate_subscription_type(self, valid_subscription_type: list):
        subscription_type = self.data.get("subscription_type", None)
        if subscription_type not in valid_subscription_type:
            return valid_subscription_type
        else:
            return True
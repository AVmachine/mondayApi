class CarKeys:
    def __init__(self):
        self.__access_key = "AKIAJ7CJ3O4LKM4OZOYA"  # private attribute
        self.__secret_key = "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"  # private attribute
        self.__role_creds = "arn:aws:iam::820223306190:role/Alexa_Lambda"

    def get_access_key(self):
        return self.__access_key

    def get_secret_key(self):
        return self.__secret_key

    def get_role_creds(self):
        return self.__role_creds
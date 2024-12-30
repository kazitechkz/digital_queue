import re


class AppValidationConstants:
    EMAIL_REGEX_STR = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    TWELVE_DIGITS_REGEX_STR = r"^\d{12}$"
    BIN_REGEX_STR = r"^\d{12}$"
    IIN_REGEX_STR = r"^\d{12}$"
    KZ_MOBILE_REGEX_STR = r"^\+77\d{9}$"
    CAR_NUMBER_REGEX_STR = r"^\d{3}[A-Za-z]{2,3}\d{2}$"

    def __init__(self):
        self.EMAIL_REGEX = re.compile(self.EMAIL_REGEX_STR)
        self.TWELVE_DIGITS_REGEX = re.compile(self.TWELVE_DIGITS_REGEX_STR)
        self.KZ_MOBILE_REGEX = re.compile(self.KZ_MOBILE_REGEX_STR)
        self.BIN_REGEX = re.compile(self.BIN_REGEX_STR)
        self.IIN_REGEX = re.compile(self.IIN_REGEX_STR)
        self.CAR_NUMBER_REGEX = re.compile(self.CAR_NUMBER_REGEX_STR)


app_validation = AppValidationConstants()

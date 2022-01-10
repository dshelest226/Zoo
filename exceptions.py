class TooSmallNumber(Exception):
    def __init__(self, variable : str, value=0):
        self.message = f"Input number for variable {variable} is too small. Input number must be higher than {value}."
        super().__init__(self.message)

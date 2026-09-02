class BaseResponse:

    def __init__(self):
        self.status = True
        self.message = None
        self.data = None
        self.error = None

import datetime


class CustomMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        self.save_file(request, response)
        return response

    def save_file(self, response, request):
        with open("patient.log", "a+") as file:
            record = f"{request}{response}{datetime.datetime.now()}"
            file.write(record)

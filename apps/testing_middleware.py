class InjectTenantCompanyMiddleware:
    _tenant  = None
    _company = None

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.tenant  = self.__class__._tenant
        request.company = self.__class__._company
        return self.get_response(request)

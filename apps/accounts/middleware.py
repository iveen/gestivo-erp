from apps.accounts.models import UserCompanyRole, Company


class CompanyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.company = None
        request.user_role = None

        company_id = request.headers.get('X-Company-ID')

        if company_id and request.user.is_authenticated:
            try:
                ucr = UserCompanyRole.objects.select_related(
                    'company', 'role'
                ).get(
                    user=request.user,
                    company__id=company_id,
                    company__is_active=True,
                )
                request.company = ucr.company
                request.user_role = ucr.role
            except UserCompanyRole.DoesNotExist:
                pass

        return self.get_response(request)
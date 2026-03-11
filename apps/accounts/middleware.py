from apps.accounts.models import UserCompanyRole, Company
import jwt
from django.conf import settings


class CompanyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.company    = None
        request.user_role  = None
        company_id = request.headers.get('X-Company-ID')

        if company_id:
            # Decode JWT directly since DRF hasn't run yet
            auth_header = request.headers.get('Authorization', '')
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                try:
                    payload  = jwt.decode(
                        token,
                        settings.SECRET_KEY,
                        algorithms=['HS256']
                    )
                    user_id = payload.get('user_id')
                    if user_id:
                        try:
                            ucr = UserCompanyRole.objects.select_related(
                                'company', 'role'
                            ).get(
                                user__id=user_id,
                                company__id=company_id,
                                company__is_active=True,
                            )
                            request.company   = ucr.company
                            request.user_role = ucr.role
                        except UserCompanyRole.DoesNotExist:
                            # Fall back to just fetching the company
                            try:
                                request.company = Company.objects.get(
                                    id=company_id,
                                    is_active=True
                                )
                            except Company.DoesNotExist:
                                pass
                except Exception:
                    pass

        return self.get_response(request)
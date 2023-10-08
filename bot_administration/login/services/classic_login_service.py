from .all_service import get_auth_refresh_via_username
from ..models import BotUser
def login(domain, username, password, tg_id):
    status_code, auth_token, refresh = get_auth_refresh_via_username(domain, username, password)
    if status_code == 200:
         
        if not BotUser.objects.filter(tg_id=tg_id).exists():
            BotUser.objects.create(domain=domain, tg_id=tg_id, auth_type="Bearer", refresh_token=refresh)
        else:
            user = BotUser.objects.get(tg_id=tg_id)
            user.domain = domain
            user.auth_type = "Bearer"
            user.refresh_token = refresh
        return 200
    else: return 401
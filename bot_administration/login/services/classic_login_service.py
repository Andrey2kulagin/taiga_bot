from .all_service import get_auth_refresh_via_username, create_tg_user
from ..models import BotUser

def login(domain, username, password, tg_id):
    status_code, auth_token, refresh = get_auth_refresh_via_username(domain, username, password)
    if status_code == 200:
        create_tg_user(tg_id=tg_id, domain=domain,auth_type="Bearer", refresh=refresh)
        return 200
    else: return 401
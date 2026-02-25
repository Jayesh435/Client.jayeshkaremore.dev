from .models import Client


def sidebar_client_profile(request):
    if not request.user.is_authenticated:
        return {}

    try:
        client = request.user.client_profile
    except Client.DoesNotExist:
        client = None

    return {'sidebar_client_profile': client}

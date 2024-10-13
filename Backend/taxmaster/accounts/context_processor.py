from django.contrib.auth.models import Group

def user_groups(request):
    user = request.user
    return {
        'is_admin': user.is_authenticated and user.is_superuser,
        'is_taxadvisor': user.is_authenticated and user.groups.filter(name='Tax Advisor').exists(),
        'is_indivual_user': user.is_authenticated and user.groups.filter(name='Individual User').exists(),
    }
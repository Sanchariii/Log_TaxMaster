# from django.core.management.base import BaseCommand
# from django.contrib.auth.models import Group, Permission
# from django.contrib.contenttypes.models import ContentType
# from accounts.models import YourModel  # Replace with your model

# class Command(BaseCommand):
#     help = 'Create user groups with permissions'

#     def handle(self, *args, **kwargs):
#         # Define your groups
#         tax_advisor_group, created = Group.objects.get_or_create(name='TaxAdvisor')
#         individual_user_group, created = Group.objects.get_or_create(name='Individual User')

#         # Define permissions (replace YourModel with your model name)
#         content_type = ContentType.objects.get_for_model(YourModel)
        
#         view_permission = Permission.objects.get(codename='view_yourmodel', content_type=content_type)
#         add_permission = Permission.objects.get(codename='add_yourmodel', content_type=content_type)
#         change_permission = Permission.objects.get(codename='change_yourmodel', content_type=content_type)
#         delete_permission = Permission.objects.get(codename='delete_yourmodel', content_type=content_type)

#         # Assign permissions to the TaxAdvisor group
#         tax_advisor_group.permissions.add(view_permission, add_permission, change_permission)

#         # Assign view permission to Individual User group
#         individual_user_group.permissions.add(view_permission)

#         # Feedback for success
#         self.stdout.write(self.style.SUCCESS('Successfully created groups and assigned permissions'))

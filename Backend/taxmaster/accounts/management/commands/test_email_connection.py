# accounts/management/commands/test_email_connection.py

from django.core.management.base import BaseCommand
from django.core.mail import get_connection

class Command(BaseCommand):
    help = 'Test the connection to the email server'

    def handle(self, *args, **kwargs):
        try:
            connection = get_connection()
            connection.open()
            self.stdout.write(self.style.SUCCESS('Connection to the email server was successful.'))
            connection.close()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to connect to the email server: {e}'))

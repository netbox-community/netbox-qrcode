from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Command(BaseCommand):
    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@admin.local'
        password = 'admin'
        try:
            u = None
            if not User.objects.filter(username=username).exists() and not User.objects.filter(is_superuser=True).exists():
                print("admin user not found, creating one")

                u = User.objects.create_superuser(username, email, password)
                print(f"{bcolors.WARNING}===================================")
                print(f"{bcolors.WARNING}A superuser for NetBox / Django '{username}' was created with email '{email}' and password '{password}'")
                print(f"{bcolors.WARNING}===================================")
            else:
                print("admin user found. Skipping super user creation")
                print(u)
        except Exception as e:
            print(f"There was an error: {e}")
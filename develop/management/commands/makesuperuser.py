# This script creates the Django Super User which is also used for the first login to Netbox.
# This means that no user needs to be created in the development phase, as this is done when Docker-Compose is started. 
# The script is terminated prematurely if a user already exists.
# User name and password see parameters below "Username" and "password"
#
# This script must be located in the Django plugin path .../management/comands at development time.
# e.g.: Docker-Compose volumes: ../develop/management:/source/netbox_qrcode/management
# e.g.: Docker-Compose command: "python manage.py makesuperuser".

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()

class bcolors:
    PURPLE = '\033[95m'
    RED = '\033[91m'

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
                print(f"{bcolors.PURPLE}===================================")
                print(f"{bcolors.PURPLE}A superuser for NetBox / Django '{username}' was created with email '{email}' and password '{password}'")
                print(f"{bcolors.PURPLE}===================================")
            else:
                print(f"{bcolors.PURPLE}A superuser for NetBox / Django Admin user already exists or was created during the first Docker-Compose start.")
                print(u)
        except Exception as e:
            print(f"{bcolors.RED}There was an error: {e}")
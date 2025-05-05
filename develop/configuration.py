"""NetBox configuration file."""
import os

# For reference see http://netbox.readthedocs.io/en/latest/configuration/mandatory-settings/
# Based on https://github.com/digitalocean/netbox/blob/develop/netbox/netbox/configuration.example.py

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#########################
#                       #
#   Required settings   #
#                       #
#########################

# This is a list of valid fully-qualified domain names (FQDNs) for the NetBox server. NetBox will not permit write
# access to the server via any other hostnames. The first FQDN in the list will be treated as the preferred name.
#
# Example: ALLOWED_HOSTS = ['netbox.example.com', 'netbox.internal.local']
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(" ")

# PostgreSQL database configuration.
DATABASE = {
    "NAME": os.environ.get("DB_NAME", "netbox"),  # Database name
    "USER": os.environ.get("DB_USER", ""),  # PostgreSQL username
    "PASSWORD": os.environ.get("DB_PASSWORD", ""),
    # PostgreSQL password
    "HOST": os.environ.get("DB_HOST", "localhost"),  # Database server
    "PORT": os.environ.get("DB_PORT", ""),  # Database port (leave blank for default)
}

# This key is used for secure generation of random numbers and strings. It must never be exposed outside of this file.
# For optimal security, SECRET_KEY should be at least 50 characters in length and contain a mix of letters, numbers, and
# symbols. NetBox will not run without this defined. For more information, see
# https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SECRET_KEY
SECRET_KEY = os.environ.get("SECRET_KEY", "")

# Redis database settings. The Redis database is used for caching and background processing such as webhooks
# Seperate sections for webhooks and caching allow for connecting to seperate Redis instances/datbases if desired.
# Full connection details are required in both sections, even if they are the same.
REDIS = {
    "caching": {
        "HOST": os.environ.get("REDIS_HOST", "redis"),
        "PORT": int(os.environ.get("REDIS_PORT", 6379)),
        "PASSWORD": os.environ.get("REDIS_PASSWORD", ""),
        "DATABASE": 1,
        "DEFAULT_TIMEOUT": 300,
        "SSL": bool(os.environ.get("REDIS_SSL", False)),
    },
    "tasks": {
        "HOST": os.environ.get("REDIS_HOST", "redis"),
        "PORT": int(os.environ.get("REDIS_PORT", 6379)),
        "PASSWORD": os.environ.get("REDIS_PASSWORD", ""),
        "DATABASE": 0,
        "DEFAULT_TIMEOUT": 300,
        "SSL": bool(os.environ.get("REDIS_SSL", False)),
    },
}


#########################
#                       #
#   Optional settings   #
#                       #
#########################

# Specify one or more name and email address tuples representing NetBox administrators. These people will be notified of
# application errors (assuming correct email settings are provided).
ADMINS = [
    # ['John Doe', 'jdoe@example.com'],
]

# Optionally display a persistent banner at the top and/or bottom of every page. HTML is allowed. To display the same
# content in both banners, define BANNER_TOP and set BANNER_BOTTOM = BANNER_TOP.
BANNER_TOP = os.environ.get("BANNER_TOP", None)
BANNER_BOTTOM = os.environ.get("BANNER_BOTTOM", None)

# Text to include on the login page above the login form. HTML is allowed.
BANNER_LOGIN = os.environ.get("BANNER_LOGIN", "")

# Base URL path if accessing NetBox within a directory. For example, if installed at http://example.com/netbox/, set:
# BASE_PATH = 'netbox/'
BASE_PATH = os.environ.get("BASE_PATH", "")

# Maximum number of days to retain logged changes. Set to 0 to retain changes indefinitely. (Default: 90)
CHANGELOG_RETENTION = int(os.environ.get("CHANGELOG_RETENTION", 0))

# API Cross-Origin Resource Sharing (CORS) settings. If CORS_ORIGIN_ALLOW_ALL is set to True, all origins will be
# allowed. Otherwise, define a list of allowed origins using either CORS_ORIGIN_WHITELIST or
# CORS_ORIGIN_REGEX_WHITELIST. For more information, see https://github.com/ottoyiu/django-cors-headers
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = []
CORS_ORIGIN_REGEX_WHITELIST = []

# Set to True to enable server debugging. WARNING: Debugging introduces a substantial performance penalty and may reveal
# sensitive information about your installation. Only enable debugging while performing testing. Never enable debugging
# on a production system.
DEBUG = True
DEVELOPER = True

# Email settings
EMAIL = {
    "SERVER": "localhost",
    "PORT": 25,
    "USERNAME": "",
    "PASSWORD": "",
    "TIMEOUT": 10,
    "FROM_EMAIL": "",
}

# Enforcement of unique IP space can be toggled on a per-VRF basis.
# To enforce unique IP space within the global table (all prefixes and IP addresses not assigned to a VRF),
# set ENFORCE_GLOBAL_UNIQUE to True.
ENFORCE_GLOBAL_UNIQUE = False

# Enable custom logging. Please see the Django documentation for detailed guidance on configuring custom logs:
#   https://docs.djangoproject.com/en/1.11/topics/logging/
LOGGING = {}

# Setting this to True will permit only authenticated users to access any part of NetBox. By default, anonymous users
# are permitted to access most data in NetBox (excluding secrets) but not make any changes.
LOGIN_REQUIRED = False

# Base URL path if accessing NetBox within a directory. For example, if installed at http://example.com/netbox/, set:
# BASE_PATH = 'netbox/'
BASE_PATH = os.environ.get("BASE_PATH", "")

# Setting this to True will display a "maintenance mode" banner at the top of every page.
MAINTENANCE_MODE = os.environ.get("MAINTENANCE_MODE", False)

# An API consumer can request an arbitrary number of objects =by appending the "limit" parameter to the URL (e.g.
# "?limit=1000"). This setting defines the maximum limit. Setting it to 0 or None will allow an API consumer to request
# all objects by specifying "?limit=0".
MAX_PAGE_SIZE = int(os.environ.get("MAX_PAGE_SIZE", 1000))

# The file path where uploaded media such as image attachments are stored. A trailing slash is not needed. Note that
# the default value of this setting is derived from the installed location.
MEDIA_ROOT = os.environ.get("MEDIA_ROOT", os.path.join(BASE_DIR, "media"))

NAPALM_USERNAME = os.environ.get("NAPALM_USERNAME", "")
NAPALM_PASSWORD = os.environ.get("NAPALM_PASSWORD", "")

# NAPALM timeout (in seconds). (Default: 30)
NAPALM_TIMEOUT = os.environ.get("NAPALM_TIMEOUT", 30)

# NAPALM optional arguments (see http://napalm.readthedocs.io/en/latest/support/#optional-arguments). Arguments must
# be provided as a dictionary.
NAPALM_ARGS = {
    "secret": NAPALM_PASSWORD,
    # Include any additional args here
}

# Determine how many objects to display per page within a list. (Default: 50)
PAGINATE_COUNT = os.environ.get("PAGINATE_COUNT", 50)

# Enable installed plugins. Add the name of each plugin to the list.
PLUGINS = ["netbox_qrcode"]

# Plugins configuration settings. These settings are used by various plugins that the user may have installed.
# Each key in the dictionary is the name of an installed plugin and its value is a dictionary of settings.
PLUGINS_CONFIG = {

    'netbox_qrcode': {

        ## Example Template for Devices

        'device_2': {
            'title': 'Example 2 (Template for Device)',
            'text_template': '<div style="display: inline-block; height: 5mm; width: 15mm"><img src="{{ logo }}" style="width:100%; height:100%; object-fit:fill;""></div><br>{{ obj.name }}<br>Device: {{ obj.id|stringformat:"07d" }}',
            'font_size': '4mm',
            'label_qr_width': '20mm',
            'label_qr_height': '30mm',
            'label_qr_text_distance': '2mm',
            'label_width': '56mm',
            'label_height': '32mm',
            'label_edge_top': '0mm',
            'label_edge_left': '2mm',
            'label_edge_right': '2mm',
            'logo': '/media/image-attachments/Netbox_Icon_Example.png',
        },

        'device_3': {
            'title': 'Example 3 (Template for Device)',
            'font_size': '4mm',
            'label_qr_width': '15mm',
            'label_qr_height': '15mm',
            'label_qr_text_distance': '2mm',
            'label_width': '56mm',
            'label_height': '32mm',
            'label_edge_top': '0mm',
            'label_edge_left': '2mm',
            'label_edge_right': '2mm',
             'text_location': 'left',
        },

        'device_4': {
            'title': 'Example 4 (Template for Device)',
            'font_size': '4mm',
            'text_align_horizontal': 'center',
            'text_align_vertical': 'middle',
            'label_qr_width': '20mm',
            'label_qr_height': '20mm',
            'label_qr_text_distance': '0mm',
            'label_width': '56mm',
            'label_height': '32mm',
            'label_edge_top': '0mm',
            'label_edge_left': '0mm',
            'label_edge_right': '0mm',
            'with_text': True,
            'with_qr': False,
        },

        'device_5': {
            'title': 'Example 5 (Template for Device)',
            'font_size': '4mm',
            'text_align_horizontal': 'left',
            'text_align_vertical': 'middle',
            'label_qr_width': '20mm',
            'label_qr_height': '20mm',
            'label_qr_text_distance': '0mm',
            'label_width': '56mm',
            'label_height': '32mm',
            'label_edge_top': '0mm',
            'label_edge_left': '2mm',
            'label_edge_right': '0mm',
            'with_text': True,
            'with_qr': False,
        },

        'device_6': {
            'title': 'Example 6 (Template for Device)',
            'font_size': '4mm',
            'label_qr_width': '20mm',
            'label_qr_height': '20mm',
            'label_qr_text_distance': '0mm',
            'label_width': '56mm',
            'label_height': '32mm',
            'label_edge_top': '0mm',
            'label_edge_left': '0mm',
            'label_edge_right': '0mm',
            'with_text': False,
            'with_qr': True,
        },

        'device_7': {
            'title': 'Example 7 (Template for Device)',
            'font_size': '4mm',
            'label_qr_width': '20mm',
            'label_qr_height': '20mm',
            'label_qr_text_distance': '0mm',
            'label_width': '32mm',
            'label_height': '56mm',
            'label_edge_top': '2mm',
            'label_edge_left': '0mm',
            'label_edge_right': '0mm',
            'text_location': 'up',
            'text_align_horizontal': 'center',
            'text_align_vertical': 'top',
            'label_edge_bottom': '2mm',
        },

        'device_8': {
            'title': 'Example 8 (Template for Device)',
            'font_size': '4mm',
            'label_qr_width': '20mm',
            'label_qr_height': '20mm',
            'label_qr_text_distance': '2mm',
            'label_width': '32mm',
            'label_height': '56mm',
            'label_edge_top': '2mm',
            'label_edge_left': '0mm',
            'label_edge_right': '0mm',
            'text_location': 'down',
            'text_align_horizontal': 'center',
            'text_align_vertical': 'top',
        },

        'device_9': {
            'title': 'Example 9 (Template for Device)',
            'font_size': '1mm',
            'label_qr_width': '9mm',
            'label_qr_height': '9mm',
            'label_qr_text_distance': '1mm',
            'label_width': '25mm',
            'label_height': '10mm',
            'label_edge_top': '0.2mm',
            'label_edge_left': '0.2mm',
            'label_edge_right': '0mm',
        },

        'device_10': {
            'title': 'Example 10 (Template for Device)',
            'with_qr': False,
            'text_align_horizontal': 'center',
            'text_align_vertical': 'middle',
            'text_template': '<div style="display: inline-block; height: 8.65mm; width: 30mm"><img src="/media/image-attachments/Netbox_Icon_Example.png" style="width:100%; height:100%; object-fit:fill;"></div><br>'
                             '{{ obj.name }} <br>'
                             '<div style="display: inline-block; height: 10mm; width: 10mm"><img src="data:image/png;base64,{{qrCode}}" style="width:100%; height:100%; object-fit:fill;"/></div><br>' 
                             'Device: {{ obj.id|stringformat:"07d" }}'
                             '<p>&#128541; <font color="red"><b> My label design </b> </font> &#128541;</p>',
                             
            'label_width': '56mm',
            'label_height': '32mm',
            'label_edge_top': '0mm',
            'label_edge_left': '0mm',
            'label_edge_right': '0mm',
        },


        ## Example Template for Cables

        'cable': {
            'title': 'Example 1 (Template for Cable)',
            'with_qr': False,
            'label_edge_left': '0.00mm',
            'label_edge_right': '0.00mm',
            'label_edge_top': '0.00mm',
            'text_align_vertical': 'middle',
            'text_align_horizontal': 'center',
	        'text_template': '<span style="writing-mode: vertical-lr; transform: scale(-1);">'
                             '{{ obj.label }}</br>'
                             '{{ obj.label }}</br>'
                             '{{ obj.label }}</br>'
                             '{{ obj.label }}</br>'
                             '{{ obj.label }}</br>'
                             '{{ obj.label }}</br>'
                             '{{ obj.label }}</br>'
                             '{{ obj.label }}</br>'
                             '{{ obj.label }}</br>'
                             '{{ obj.label }}</br>'
                             '{{ obj.label }}</br>'
                             '{{ obj.label }}</br>'
                             '{{ obj.label }}</br>'
	                     '</span>'
        },

        'cable_2': {
            'title': 'Example 2 (Template for Cable)',
            'with_qr': False,
            'label_edge_left': '0.00mm',
            'label_edge_right': '0.00mm',
            'label_edge_top': '0.00mm',
            'text_align_vertical': 'middle',
            'text_align_horizontal': 'center',
            
            # QR-Code Image File
            'qr_version': 1,
            'qr_error_correction': 1,
            'qr_box_size': 2,
            'qr_border': 0,
            
	    'text_template': '<svg id="barcode"></svg>'
	                     '<svg id="barcode"></svg>'
	                     '<svg id="barcode"></svg>'
	                     '<svg id="barcode"></svg>'
	                     ''
	                     '<style>'
                             '   #barcode {'
                             '   max-width: 48mm;'
                             '   width: 100%;'
                             '   max-height: 6mm;'
                             '   height: 100%;'
                             '   }'
                             '</style>'
                             ''
                             '<script src="https://cdn.jsdelivr.net/npm/jsbarcode@3.11.0/dist/JsBarcode.all.min.js"></script>'
                             ''
                             '<script>'
                             '   JsBarcode("#barcode", "{{ obj.label }}", {'
                             '   background: "transparent",'
                             '   format: "CODE128",'
                             '   displayValue: true,'
                             '   margin: 0,'
                             '   height: 15'
                             '   });'
                             '</script>'
        }
    }
}

# When determining the primary IP address for a device, IPv6 is preferred over IPv4 by default. Set this to True to
# prefer IPv4 instead.
PREFER_IPV4 = os.environ.get("PREFER_IPV4", False)

# Remote authentication support
REMOTE_AUTH_ENABLED = False
#REMOTE_AUTH_BACKEND = "utilities.auth_backends.RemoteUserBackend"
REMOTE_AUTH_BACKEND = "netbox.authentication.RemoteUserBackend"
REMOTE_AUTH_HEADER = "HTTP_REMOTE_USER"
REMOTE_AUTH_AUTO_CREATE_USER = True
REMOTE_AUTH_DEFAULT_GROUPS = []
REMOTE_AUTH_DEFAULT_PERMISSIONS = []

# This determines how often the GitHub API is called to check the latest release of NetBox. Must be at least 1 hour.
RELEASE_CHECK_TIMEOUT = 24 * 3600

# This repository is used to check whether there is a new release of NetBox available. Set to None to disable the
# version check or use the URL below to check for release in the official NetBox repository.
RELEASE_CHECK_URL = None
# RELEASE_CHECK_URL = 'https://api.github.com/repos/netbox-community/netbox/releases'

SESSION_FILE_PATH = None

# The file path where custom reports will be stored. A trailing slash is not needed. Note that the default value of
# this setting is derived from the installed location.
REPORTS_ROOT = os.environ.get("REPORTS_ROOT", os.path.join(BASE_DIR, "reports"))

# Time zone (default: UTC)
TIME_ZONE = os.environ.get("TIME_ZONE", "UTC")

# Date/time formatting. See the following link for supported formats:
# https://docs.djangoproject.com/en/dev/ref/templates/builtins/#date
DATE_FORMAT = os.environ.get("DATE_FORMAT", "N j, Y")
SHORT_DATE_FORMAT = os.environ.get("SHORT_DATE_FORMAT", "Y-m-d")
TIME_FORMAT = os.environ.get("TIME_FORMAT", "g:i a")
SHORT_TIME_FORMAT = os.environ.get("SHORT_TIME_FORMAT", "H:i:s")
DATETIME_FORMAT = os.environ.get("DATETIME_FORMAT", "N j, Y g:i a")
SHORT_DATETIME_FORMAT = os.environ.get("SHORT_DATETIME_FORMAT", "Y-m-d H:i")
from .utilities import get_img_b64, get_qr
from django.template import engines

# ******************************************************************************************
# For better clarity, the sub-functions of template_content.py have been outsourced.
# ******************************************************************************************

##################################
# The configuration is taken and all fields that are module-specific (e.g. Device, Rack, etc.) are replaced.
# --------------------------------
# Parameter:
#   labelDesignNo: Which label design should be loaded.
#   parentSelf: Self from Parrent Function
def config_for_modul(parentSelf, labelDesignNo):

    # Copy so that the Runtime data is not changed.
    config = parentSelf.context['config'].copy() # From Netbox Config File

    # Create suffix to read the correct module configuration.
    confModulsufix = str() # None if the first standard label

    if(labelDesignNo >= 2):
            confModulsufix = '_' + str(labelDesignNo)

    # Collect the QR code plugin configuration for the specific object such as device, rack etc.
    # and overwrite the default configuration fields.
    obj_cfg = config.get(parentSelf.model.replace('dcim.', '') + confModulsufix) # get spezific object settings
    
    print(obj_cfg)

    if obj_cfg is None: 
        return '' # Abort if no config data. 

    config.update(obj_cfg) # Ovverride default confiv Values

    return config

##################################
# Create QR-Code
# --------------------------------
# Parameter:
#   text: Text for QR-Code
#   config: From the Netbox configuration file
def create_QRCode(text, config):

    # Collect the configuration entries that begin with "qr_.
    # These are required to generate the QR code.
    qr_args = {}
    for k, v in config.items():
        if k.startswith('qr_'):
            qr_args[k.replace('qr_', '')] = v

    # Create a QR code
    qrCode = get_qr(text, **qr_args)
    return get_img_b64(qrCode)


##################################
# Create URL for QR code
# --------------------------------
# Parameter:
#   config: From the Netbox configuration file
#   obj: Data from the model (e.g. device, rack, etc.)
#   request: HTML Request Information
def create_url(parentSelf, config, obj):

    request = parentSelf.context['request'] # HTML Request Informations

    if config.get('url_template'):
        # A user-defined design specification of the URL is provided in ninja2 format.
        django_engine = engines["django"]
        template = django_engine.from_string(config.get('url_template')) # Custom template for URL design.
        return template.render({'obj': obj}) # Replace placeholder
    else:
        return request.build_absolute_uri(obj.get_absolute_url()) # URL to the requested page

##################################
# Create text for label
# --------------------------------
# Parameter:
#   config: From the Netbox configuration file
#   obj: Data from the model (e.g. device, rack, etc.)
#   qrCode: QR-Code Image 
def create_text(config, obj, qrCode):

    text = str()

    if config.get('with_text'):
        if config.get('text_template'):
            return get_text_template(config, obj, qrCode) # Create text content based on the Ninja2 template from the user
        else:
            return get_text_fields(config, obj) # Use the list of variables from the Config.

##################################
# A user-defined design specification of the text is provided in ninja2 format.
# --------------------------------
# Parameter:
#   config: From the Netbox configuration file
#   obj: Data from the model (e.g. device, rack, etc.)
#   qrCode: QR-Code Image (To create a freely defined label with QR code.)
def get_text_template(config, obj, qrCode):

    django_engine = engines["django"]
    template = django_engine.from_string(config.get('text_template')) # Get Custom Template
    logo = config.get('logo')
    return template.render({'obj': obj, 
                            'logo': logo,
                            'qrCode': qrCode}) # Replace placeholder

##################################
# Retrieves all values from the object (e.g. device, rack, etc.)
# depending on the configuration parameter that are to be displayed in list form and prepares them.
# --------------------------------
# Parameter:
#   config: From the Netbox configuration file
#   obj: Data from the model (e.g. device, rack, etc.)
def get_text_fields(config, obj):

    text = []

    for text_field in config.get('text_fields', []):
        cfn = None
        if '.' in text_field:
            try:
                text_field, cfn = text_field.split('.')
            except ValueError:
                cfn = None
        if getattr(obj, text_field, None):
            if cfn:
                try:
                    if getattr(obj, text_field).get(cfn):
                        text.append('{}'.format(getattr(obj, text_field).get(cfn)))
                except AttributeError:
                    # fix for nb3.3: trying to get cable termination and device in same way as custom field
                    if type(getattr(obj, text_field)) is list:
                        first_element = next(iter(getattr(obj, text_field)), None)
                        if first_element and getattr(first_element, cfn, None):
                            text.append('{}'.format(getattr(first_element, cfn)))
            else:
                text.append('{}'.format(getattr(obj, text_field)))

    # Append user-defined text to the end.
    custom_text = config.get('custom_text')

    if custom_text:
        text.append(custom_text)

    # Convert text list to string with line breaks.
    return '<br>'.join(text)
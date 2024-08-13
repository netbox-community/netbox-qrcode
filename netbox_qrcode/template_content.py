from packaging import version
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from netbox.plugins import PluginTemplateExtension
from .template_content_functions import create_text, create_url, config_for_modul, create_QRCode

# ******************************************************************************************
# Contains the main functionalities of the plugin and thus creates the content for the 
# individual modules, e.g: Device, Rack etc.
# ******************************************************************************************

##################################
# Class for creating the plugin content
class QRCode(PluginTemplateExtension):

    ##################################          
    # Creates a plug-in view for a label.
    # --------------------------------
    # Parameter:
    #   labelDesignNo: Which label design should be loaded.
    def Create_SubPluginContent(self, labelDesignNo):
        
        thisSelf = self

        obj = self.context['object'] # An object of the type Device, Rack etc.

        # Config suitable for the module
        config = config_for_modul(thisSelf, labelDesignNo)

        # Abort if no config data. 
        if config is None: 
            return '' 

        # Get URL for QR code
        url = create_url(thisSelf, config, obj)

        # Create a QR code
        qrCode = create_QRCode(url, config)

        # Create the text for the label if required.
        text = create_text(config, obj, qrCode)

        # Create plugin using template
        try:
            if version.parse(settings.VERSION).major >= 3:

                render = self.render(
                    'netbox_qrcode/qrcode3.html', extra_context={
                                                                    'title': config.get('title'),
                                                                    'labelDesignNo': labelDesignNo,
                                                                    'qrCode': qrCode, 
                                                                    'with_text': config.get('with_text'),
                                                                    'text': text,
                                                                    'text_location': config.get('text_location'),
                                                                    'font': config.get('font'),
                                                                    'font_size': config.get('font_size'),
                                                                    'font_weight': config.get('font_weight'),
                                                                    'with_qr': config.get('with_qr'),
                                                                    'label_qr_width': config.get('label_qr_width'),
                                                                    'label_qr_height': config.get('label_qr_height'),
                                                                    'label_qr_text_distance': config.get('label_qr_text_distance'),
                                                                    'label_width': config.get('label_width'),
                                                                    'label_height': config.get('label_height'), 
                                                                    'label_edge_top': config.get('label_edge_top'),
                                                                    'label_edge_left': config.get('label_edge_left'),
                                                                    'label_edge_right': config.get('label_edge_right'),
                                                                    'label_edge_bottom': config.get('label_edge_bottom')
                                                                }
                )
            
                return render
            else:
                # Versions 1 and 2 are no longer supported.
                return self.render(
                    'netbox_qrcode/qrcode.html', extra_context={'image': qrCode}
                )
        except ObjectDoesNotExist:
            return ''

    ##################################
    # Create plugin content
    # - First, a plugin view is created for the first label.
    # - If there are further configuration entries for the object/model (e.g. device, rack etc.),
    #   further label views are also created as additional plugin views.
    def Create_PluginContent(self):

        # First Plugin Content
        pluginContent = QRCode.Create_SubPluginContent(self, 1) 

        # Check whether there is another configuration for the object, e.g. device, rack, etc.
        # Support up to 10 additional label configurations (objectName_2 to ..._10) per object (e.g. device, rack, etc.).

        config = self.context['config'] # Django configuration

        for i in range(2, 11):

            configName = self.model.replace('dcim.', '') + '_' + str(i)
            obj_cfg = config.get(configName) # Load configuration for additional label if possible.

            if(obj_cfg):
                pluginContent += QRCode.Create_SubPluginContent(self, i) # Add another plugin view
            else:
                break
        
        return pluginContent

##################################
# The following section serves to integrate the plugin into Netbox Core.
        
# Class for creating a QR code for the model: Device
class DeviceQRCode(QRCode):
    model = 'dcim.device' # Info for Netbox in which model the plugin should be integrated.

    def right_page(self):
        return self.Create_PluginContent()

# Class for creating a QR code for the model: Rack
class RackQRCode(QRCode):
    model = 'dcim.rack' # Info for Netbox in which model the plugin should be integrated.

    def right_page(self):
        return self.Create_PluginContent()

# Class for creating a QR code for the model: Cable
class CableQRCode(QRCode):
    model = 'dcim.cable' # Info for Netbox in which model the plugin should be integrated.

    def left_page(self):
        return self.Create_PluginContent()

# Class for creating a QR code for the model: Location
class LocationQRCode(QRCode):
    model = 'dcim.location' # Info for Netbox in which model the plugin should be integrated.

    def left_page(self):
        return self.Create_PluginContent()

# Class for creating a QR code for the model: Power Feed
class PowerFeedQRCode(QRCode):
    model = 'dcim.powerfeed' # Info for Netbox in which model the plugin should be integrated.

    def right_page(self):
        return self.Create_PluginContent()

# Class for creating a QR code for the model: Power Panel
class PowerPanelQRCode(QRCode):
    model = 'dcim.powerpanel' # Info for Netbox in which model the plugin should be integrated.

    def right_page(self):
        return self.Create_PluginContent()

# Connects Netbox Core with the plug-in classes
template_extensions = [DeviceQRCode, RackQRCode, CableQRCode, LocationQRCode, PowerFeedQRCode, PowerPanelQRCode]

import logging

from packaging import version
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from netbox.plugins import PluginTemplateExtension
from .template_content_functions import create_text, create_url, config_for_modul, create_QRCode, model_config_key

logger = logging.getLogger('netbox.plugins.netbox_qrcode')

# ******************************************************************************************
# Contains the main functionalities of the plugin and thus creates the content for the 
# individual modules, e.g: Device, Rack etc.
# ******************************************************************************************

# Check if netbox-inventory is available
try:
    import netbox_inventory
    INVENTORY_AVAILABLE = True
except ImportError:
    INVENTORY_AVAILABLE = False




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
            if version.parse(settings.RELEASE.version).major >= 3:

                render = self.render(
                    'netbox_qrcode/qrcode3.html', extra_context={
                                                                    'title': config.get('title'),
                                                                    'labelDesignNo': labelDesignNo,
                                                                    'qrCode': qrCode, 
                                                                    'with_text': config.get('with_text'),
                                                                    'text': text,
                                                                    'text_location': config.get('text_location'),
                                                                    'text_align_horizontal': config.get('text_align_horizontal'),
                                                                    'text_align_vertical': config.get('text_align_vertical'),
                                                                    'font': config.get('font'),
                                                                    'font_size': config.get('font_size'),
                                                                    'font_weight': config.get('font_weight'),
                                                                    'font_color': config.get('font_color'),
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
            logger.debug("Label design '%s' skipped: related object does not exist",
                         self.Config_Name(labelDesignNo))
            return ''

    ##################################
    # Returns the configuration key a label design is read from,
    # e.g. 'device' for the first label and 'device_2' for the second.
    # --------------------------------
    # Parameter:
    #   labelDesignNo: Which label design the key is for.
    def Config_Name(self, labelDesignNo):

        modelName = model_config_key(self.models)

        if labelDesignNo <= 1:
            return modelName

        return '{}_{}'.format(modelName, labelDesignNo)

    ##################################
    # Creates a placeholder for a label that could not be rendered, so that a single
    # broken configuration does not discard the object's other labels.
    # --------------------------------
    # Parameter:
    #   configName: The configuration key of the label that failed.
    #   error: The exception raised while rendering it.
    def Create_ErrorContent(self, configName, error):

        try:
            return self.render(
                'netbox_qrcode/qrcode_error.html', extra_context={
                                                                    'configName': configName,
                                                                    'error': repr(error)
                                                                }
            )
        except Exception:
            # Reporting a failure must never itself remove the remaining labels.
            return ''

    ##################################
    # Create plugin content
    # - First, a plugin view is created for the first label.
    # - If there are further configuration entries for the object/model (e.g. device, rack etc.),
    #   further label views are also created as additional plugin views.
    def Create_PluginContent(self):

        # Support up to 10 label configurations per object (e.g. device, rack, etc.):
        # the object's own configuration, plus objectName_2 to ..._10.

        config = self.context['config'] # Django configuration

        pluginContent = str()

        for i in range(1, 11):

            configName = self.Config_Name(i)

            # The numbering must be contiguous, so the first missing entry ends the chain.
            if i > 1 and not config.get(configName):
                break

            # Each label is rendered in isolation. Without this, an error in any one
            # design propagates out of the template extension and NetBox replaces the
            # plugin's entire output, discarding the labels that did render.
            try:
                pluginContent += QRCode.Create_SubPluginContent(self, i)
            except Exception as e:
                logger.warning("Label design '%s' could not be rendered: %r", configName, e)
                pluginContent += self.Create_ErrorContent(configName, e)

        return pluginContent

##################################
# The following section serves to integrate the plugin into Netbox Core.
        
# Class for creating a QR code for the model: Device
class DeviceQRCode(QRCode):
    models = ('dcim.device',)

    def right_page(self):
        return self.Create_PluginContent()

# Class for creating a QR code for the model: Rack
class RackQRCode(QRCode):
    models = ('dcim.rack',)

    def right_page(self):
        return self.Create_PluginContent()

# Class for creating a QR code for the model: Cable
class CableQRCode(QRCode):
    models = ('dcim.cable',)

    def left_page(self):
        return self.Create_PluginContent()

# Class for creating a QR code for the model: Location
class LocationQRCode(QRCode):
    models = ('dcim.location',)

    def left_page(self):
        return self.Create_PluginContent()

# Class for creating a QR code for the model: Power Feed
class PowerFeedQRCode(QRCode):
    models = ('dcim.powerfeed',)

    def right_page(self):
        return self.Create_PluginContent()

# Class for creating a QR code for the model: Power Panel
class PowerPanelQRCode(QRCode):
    models = ('dcim.powerpanel',)

    def right_page(self):
        return self.Create_PluginContent()

# Class for dcim.module
class ModuleQRCode(QRCode):
    models = ('dcim.module',)

    def right_page(self):
        return self.Create_PluginContent()
# Class for Netbox-Inventory Plugin
class AssetQRCode(QRCode):
    models = ('netbox_inventory.asset',)

    def right_page(self):
        return self.Create_PluginContent()

##################################
# Other plugins support

# Commenting out (for now) - make this work on core models first.
# Class for creating a QR code for the Plugin: Netbox-Inventory (https://github.com/ArnesSI/netbox-inventory)
#class Plugin_Netbox_Inventory(QRCode):
#    models = ()'netbox_inventory.asset' # Info for Netbox in which model the plugin should be integrated.
#
#    def right_page(self):
#        return self.Create_PluginContent()

# Connects Netbox Core with the plug-in classes
# Removed , Plugin_Netbox_Inventory]
template_extensions = [DeviceQRCode, ModuleQRCode, RackQRCode, CableQRCode, LocationQRCode, PowerFeedQRCode, PowerPanelQRCode]
if INVENTORY_AVAILABLE:
    template_extensions.append(AssetQRCode)

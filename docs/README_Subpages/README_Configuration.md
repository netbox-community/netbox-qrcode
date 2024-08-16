[<< Back to README start](/README.md)

# Configuration
The plugin is configured in the Netbox configuration file: configuration.py
If you have followed the standard installation of Netbox, the configuration file is located under: /opt/netbox/netbox/netbox/configuration.py

The following options are available:

## General Plugin

* `title`: 

    A title is displayed in the label window. This can be expanded with information. Useful if you want to provide several label variants for devices, for example.
    ```Python
    'title': '', #DEFAULT
    'title': 'My text extension in the plugin heading.',
    ```

## Text content

* `with_text`: 

    Text label will be added to QR code image if enabled.

    ```Python
    'with_text': True, # DEFAULT
    'with_text': False,
    ```

* `text_location`: 

    Where to render the text, relative to the QR code.  
    
    ```Python
    'text_location': 'right', # DEFAULT
    'text_location': 'left',
    'text_location': 'up',
    'text_location': 'down',
    'text_location': 'center', # Text in the center if no QR code is used.
    ```

    ### Text source (Option A)

* `text_fields`: 

    Text fields of an object that will be added as text label to QR image. It's possible to use custom field values.

    ```Python
    'text_fields': ['name', 'serial'], # DEFAULT
    'text_fields': ['name'],
    'text_fields': ['site',
                    'name',
                    'id']
    ```

* `custom_text`: Additional text label to QR code image (will be added after text_fields).
    ```Python
    'text_location': None, # DEFAULT
    'text_location': 'My Text',
    ```
    ### Text source (Option B)

* `text_template`: 

    [Jinja2](https://jinja.palletsprojects.com/) template with {{ obj }} as context for device, rack, etc., using it ignores `text_fields` and `custom_text`.

    **{{ obj.xyz }} :** 
    
    Value of the object/module (e.g. device, rack, etc.). Which values can be read depends on the Netbox module. Many names can be found during mass import, e.g. https://server/dcim/devices/import/, i.e. the “Field Options” names such as “status”, i.e. “obj.status”. Writing HTML text is permitted.

    ```Python
    # Example to output name and site in two lines with caption (See also screenshots below):

    'text_template': 'Name: {{ obj.name }}\nSite: {{ obj.site }}',
    ```

    ![Cable QR Code](/docs/img/qrcode_text_template.png)

    **{{ logo }}** : 
    
    The value stored in the logo parameter.

    ```Python
    <div style="display: inline-block; height: 5mm; width: 15mm"><img src="{{logo}}" height="100%" width="100%"/></div>```
    ```

    **{{ qrCode }}** : 
    
    The QR code is provided as a Base64 string.

    ```Python
    <div style="display: inline-block; height: 10mm; width: 10mm"><img src="data:image/png;base64,{{qrCode}}" height="100%" width="100%"/></div>
    ```



## Font

* `font`: 

    Font name for text label (All fonts supported by the browser are supported. [Web-Safe-Fonts](https://www.w3schools.com/cssref/css_websafe_fonts.php) are recommended as these are supported on all common systems without the need for subsequent installation.
    
    ```Python
    'font': 'TahomaBold' # DEFAULT
    'font': 'Arial',
    'font': 'Verdana',
    'font': 'Arial, Verdana', # If Arial is not available then Verdana.
    'font': '\'Trebuchet MS\'', # If blank character in font name.
    ```

* `font_size`: 

    Defines the height of the font.
    
    ```Python
    'font_size': '3.00mm', # DEFAULT
    'font_size': '0.11in', # For inches
    ```

* `font_weight`: 

    Determines how dense the font is.
    
    ```Python
    'font_weight': 'normal', # DEFAULT
    'font_weight': 'bold',
    'font_weight': 'lighter', 
    'font_weight': 'bolder', 
    ```

## QR-Code

* `with_qr`: 

    QR-Code label will be added to label if enabled.

    ```Python
    'with_qr': True, # DEFAULT
    'with_qr': False,
    ```

    ### QR-Code alternative source

    By default, the URL path to the object is used as the text for the QR code. Below is an alternative for defining your own QR code content.

* `url_template`: [Jinja2](https://jinja.palletsprojects.com/) template with {{ obj }} as context for device, rack, etc.

    ```Python
    # Example to output the object name and the ID in the QR code.
    (This means that information other than the Netbox URL can also be output in the QR code):

    'url_template': None, # DEFAULT
    'url_template': '{{ obj.name }} - Objekt ID: {{ obj.id }}',
    ```

    ### QR-Code Image File
    These parameters are used to create the QR code image file.

* `qr_version`: 

    For the image file: Parameter is an integer from 1 to 40 that controls the size of the QR Code (the smallest, version 1, is a 21x21 matrix). More Information see: [qrcode 3.0 Parameter "version"](https://pypi.org/project/qrcode/3.0/)

    Experience: The higher the number, the more often it appears as if the QR codes are repeated. The value 1 is recommended for beginners.

    ```Python
    'qr_version': 1, # DEFAULT 
    ```

* `qr_error_correction`: 

    For the image file: This value is used to create the QR code image file. Controls the error correction used for the QR Code. More Information see: [qrcode 3.0 Parameter "error_correction"](https://pypi.org/project/qrcode/3.0/)

    Experience: You can scratch x% off the QR code before it is no longer readable.

    ```Python
    'qr_error_correction': 0, # DEFAULT - About 15% or less errors can be corrected.
    'qr_error_correction': 1, # About 7% or less errors can be corrected.
    'qr_error_correction': 2, # About 30% or less errors can be corrected.
    'qr_error_correction': 3, # About 25% or less errors can be corrected.
    ```

* `qr_box_size`: 

    For the image file: This value is used to create the QR code image file. Controls how many pixels each "Black boxes within the QR code" of the QR code is. More Information see: [qrcode 3.0 Parameter "box_size"](https://pypi.org/project/qrcode/3.0/)

    Experience: The larger the value, the larger the QR code image file will be. It also takes longer to create the image file. If a value that is too small is used, the QR code may become unscaled if label_qr_width and label_qr_height have values that are too large.

    ```Python
    'qr_box_size': 4, # DEFAULT
    ```

* `qr_border`: 

    For the image file: This value is used to create the QR code image file. Defines the border width when rendering the QR code image file. More Information see: [qrcode 3.0 Parameter "qr_border"](https://pypi.org/project/qrcode/3.0/)

    Experience: Value 0, as the size of the QR code can be better influenced by 'label_qr_width', label_qr_height and the centered positioning creates a margin. The size of the QR code can therefore be better adjusted. However, there should be a border around the QR code on the label.

    ```Python
    'qr_border': 0, # DEFAULT.
    ```

* `Summery qr_... `: 

    This table should show a few combinations of qr_[parameter name] and their resulting QR code image file sizes. With the values in column 4 you can see that you already get a 4cm x 4cm QR code image file.

    |           | Test    | Test    | Test   | Test    |Test     | Test     |Test     |Test     |Test     | Test   |
    | ------------------- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
    | qr_version          | 1    | 1    | 1    | 1    | 1    | 1    | 2    | 4    | 6    | 40   |
    | qr_box_size         | 1    | 2    | 3    | 4    | 5    | 6    | 6    | 6    | 6    | 1    |
    | qr_error_correction | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
    | qr_border           | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    |
    | DPI                 | 72   | 72   | 72   | 72   | 72   | 72   | 72   | 72   | 72   | 72   |
    | cm (H/W)            | `1,02` | `2,05` | `3,07` | `4,09` | `5,12` | `6,14` | `6,14` | `6,99` | `8,68` | `6,24` |
    | Pixel (H/W)              | `29`   | `58`   | `87`   | `116`  | `145`  | `174`  | `174`  | `198`  | `246` | `177`  |
    
## Label Layout
The parameters that can be used to design the label are listed below.

### Label dimensions
* `label_width`: 

    Indicates how wide the physical label is.

    ```Python
    'label_width': '56mm', # DEFAULT
    'label_width': '2.20in', # For inch
    ```

* `label_height`: 

    Indicates how high the physical label is.

    ```Python
    'label_height': '32mm', # DEFAULT
    'label_height': '1.26in', # For inch
    ```

### Label edge
* `label_edge_top`: 

    Indicates how high the physical label is.

    ```Python
    'label_edge_top': '0mm', # DEFAULT
    'label_edge_top': '0in', # For inch
    ```

* `label_edge_left`: 

    Indicates how high the physical label is.

    ```Python
    'label_edge_left': '1.5mm', # DEFAULT
    'label_edge_left': '0.59in', # For inch
    ```

* `label_edge_right`: 

    Indicates how high the physical label is.

    ```Python
    'label_edge_right': '1.5mm', # DEFAULT
    'label_edge_right': '0.59in', # For inch
    ```

* `label_edge_bottom`: 

    Indicates how high the physical label is.

    ```Python
    'label_edge_bottom': '0mm', # DEFAULT
    'label_edge_bottom': '0in', # For inch
    ```

### Label QR code positioning
* `label_qr_width`: 

    Specifies how wide the QR code image should be displayed on the label.

    ```Python
    'label_qr_width': '12mm', # DEFAULT
    'label_qr_width': '0.47in', # For inch
    ```

* `label_qr_height`: 

    Specifies how high the QR code image should be displayed on the label.

    ```Python
    'label_qr_height': '12mm', # DEFAULT
    'label_qr_height': '0.47in', # For inch
    ```

* `label_qr_text_distance`: 

    Specifies how large the distance between the QR code and the text should be.

    ```Python
    'label_qr_text_distance': '1mm', # DEFAULT
    'label_qr_text_distance': '0.039in', # For inch
    ```

## LOGO / Image

* `logo`: 

    Enables a logo/image to be inserted in combination with the `text_template` parameter.

    **Image File size:**
    
    To keep the traffic and performance high, the image should be as small as necessary. An image with 1920x1200px and 30MB is nonsensical if it is to be 1.00x3.00cm in size at the end. The larger the image, the longer the Base64 text. If possible, the logo is completely black and not gray or colored, which makes it even smaller. (Sufficient for thermal transfer printers).

    Here are a few helpful online tools:
    Resize image online (in mm): https://image.pi7.org/resize-image-in-mm
    Image compression (e.g. 100kb to 2kb): https://tinypng.com/
    Convert image to Base64 string.: https://www.base64-image.de/

    Your image should have the following text format at the end.
    ```html
    data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABysAAAIDCA...
    ```

    Below is the Logo parameter for a Netbox logo. (Image specification: black/white,Background Transparent , 3,71KB, 202px x 57px, 71.26mm x 20.00mm)

    It is recommended to place the Logo entry at the end of the plugin configuration, as the Base64 string can be quite long. It is also recommended to place the PLUGINS_CONFIG = {} block in Configuration.py at the end of the file.

    ```Python
    'logo': 'data:image/png;base64,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',
    ```

    Below is how you can embed the logo in a text.
    It is an HTML block that contains the image {{ logo }} as well as the name {{ obj.name }} and the ID of the object {{ obj.id }} in 3 lines.

    ```Python
    'text_template': '<div style="display: inline-block; height: 20.00mm; width: 71.26mm"><img src="{{ logo }}" height="100%" width="100%"></div><br>{{ obj.name }}<br>Device: {{ obj.id }}<br>',
    ```

    If you pay attention to the proportional ratio, you can also adjust the size of the image. e.g. 5.00mm x 17.80mm. The size can also be specified in inches (in).
    ```Python
    'text_template': '<div style="display: inline-block; height: 5.00mm; width: 17.86mm"><img src="{{ logo }}" height="100%" width="100%"></div><br>{{ obj.name }}<br>Device: {{ obj.id }}<br>',
    ```

## Global Configuration
The following shows an example configuration of how to adjust parameters for all objects/modules (e.g. device, rack, etc.) at once. However, if there is a separate configuration for the device, for example, this has priority.

```Python
PLUGINS_CONFIG = {
    'netbox_qrcode': {
        ################################## 
		# General Plugin
        'title': 'My Text in headline',
        'font_size': '5.12mm', # DEFAULT
    }
}
```

## Module-dependent configuration
It is possible, for example, to overwrite the default values or the global settings from above for an (object/module) class such as Device. One or more parameters can also be overwritten here.

Example:

```Python
PLUGINS_CONFIG = {
    'netbox_qrcode': {
        ################################## 
		# General Plugin
        'title': 'My text for all headlines',
        'font_size': '5.12mm',
    }
    'device': {
        'title': 'My text for the headline Device',
        'font_size': '10mm',
    },
}
```

**Below are the default settings of the plugin.**

* `device`:

    Specific label customization for the calculated https://server/dcim/devices/

    ```Python
    'device': {
            'text_fields': ['name', 'serial'] # DEFAULT
        },
    ```

* `rack`:

    Specific label customization for the calculated https://server/dcim/racks/

    ```Python
    'rack': {
            'text_fields': ['name'] # DEFAULT
        },
    ```

* `cable`:

    Specific label customization for the calculated https://server/dcim/cables/

    ```Python
    'cable': {
            'text_fields': [
                '_termination_a_device',
                'termination_a',
                '_termination_b_device',
                'termination_b',
                'a_terminations.device',
                'a_terminations',
                'b_terminations.device',
                'b_terminations'
                ] # DEFAULT
        },
    ```

* `location`:

    Specific label customization for the calculated https://server/dcim/locations/

    ```Python
    'location': {
            'text_fields': ['name'] # DEFAULT
        },
    ```

* `powerfeed`:

    Specific label customization for the calculated https://server/dcim/locations/

    ```Python
    'powerfeed': {
            'text_fields': ['name'], # DEFAULT
        },
    ```
* `powerpanel`:

    Specific label customization for the calculated https://server/dcim/locations/

    ```Python
    'powerpanel': {
            'text_fields': ['name'], # DEFAULT
        },  
    ```

* `modul_X`:

    It is possible to store several label layouts for an object/module (e.g. device, rack, etc.). For example, for other label information or other label sizes. To do this, an increment starting with 2 to n must be specified at the end. No numbers may be skipped in the sequence. Example: device; device_2; device_3; device_5. “device_5” is not reached because 4 is missing.

    ```Python
    'device_2': {
        'title': 'My Litle Label',

        'label_width': '25mm',
        'label_height': '10mm',

        'font_size': '2mm',
        'font_weight': 'bold',

        'label_qr_width': '7.00mm',
        'label_qr_height': '9.00mm',
        'label_qr_text_distance': '0.4mm',

        'label_edge_left': '0.50mm',
        'label_edge_right': '0.00mm',

        'text_fields': ['name'],
    },
    ```
    ```Python
    'device_3': {
        ...
    },
    ```
    ```Python
    'rack_2': {
        ...
    },
    ```

# Example configuration:

This is a sample template of what a configuration can look like. But as I said, you do not have to specify all parameters.

```Python
PLUGINS_CONFIG = {
    'netbox_qrcode': {
        ################################## 
		# General Plugin
        'title': '',
        
        ################################## 
        # Text content
        'with_text': True,
        'text_location': 'right',
        
        # Text source (Option A)
        'text_fields': ['name', 'serial'],
        'custom_text': None,
        
        # Text source (Option B)
        'text_template': None,
        
        ################################## 
        # Font
        'font': 'TahomaBold',
        'font_size': '3mm',
        'font_weight': 'normal',
        
        ################################## 
        # QR-Code
        'with_qr': True,
        
        # QR-Code alternative source
        'url_template': None,
        
        # QR-Code Image File
        'qr_version': 1,
        'qr_error_correction': 0,
        'qr_box_size': 4,
        'qr_border': 0,
        
        ################################## 
        # Label Layout
        
        # Label dimensions
        'label_qr_width': '12mm',
        'label_qr_height': '12mm',
        
        # Label edge
        'label_edge_top': '0mm',
        'label_edge_left': '1.5mm',
        'label_edge_right': '1.5mm',
        'label_edge_bottom': '0mm',    
        
        # Label QR code positioning
        'label_width': '56mm',
        'label_height': '32mm',
        'label_qr_text_distance': '1mm',

        ################################## 
        # Module-dependent configuration

        'device': {
            'text_fields': ['name', 'serial']
        },

        'device_2': {
            'title': 'My Litle Label',

            'label_width': '25mm',
            'label_height': '10mm',

            'font_size': '2mm',
            'font_weight': 'bold',

            'label_qr_width': '7.00mm',
            'label_qr_height': '9.00mm',
            'label_qr_text_distance': '0.4mm',

            'label_edge_left': '0.50mm',
            'label_edge_right': '0.00mm',

            'text_fields': ['name'],
        },

        'rack': {
            'text_fields': ['name']
        },

        'cable': {
            'text_fields': [
                '_termination_a_device',
                'termination_a',
                '_termination_b_device',
                'termination_b',
                'a_terminations.device',
                'a_terminations',
                'b_terminations.device',
                'b_terminations'
                ]
        },

        'location': {
            'text_fields': ['name']
        },

        'powerfeed': {
            'text_fields': ['name']
        },

        'powerpanel': {
            'text_fields': ['name']
        },  

        'logo': '' 
    }
}
```

## Example label configurations
[Go to Example label configurations >>](docs/README_Subpages/README_Configuration_ExampleLabelConf.md)

![Cable QR Code](/docs/img/Configuration_Label_Example_10.png)

[<< Back to README start](/README.md)
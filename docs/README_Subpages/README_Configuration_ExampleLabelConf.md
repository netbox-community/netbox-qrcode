[<< Back to General Configuration](README_Configuration.md)

# Example label configurations

## Example 1 (Device) - Default
Standard label without customization

![Cable QR Code](/docs/img/Configuration_Label_Example_01.png) 

## Example 2 (Device)
QR code Higher than wide, with own logo Device name and Device ID filled with zeros.

![Cable QR Code](/docs/img/Configuration_Label_Example_02.png) 

```Python
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
```
## Example 3 (Device)
Text left QR code right with distance to the edge.

![Cable QR Code](/docs/img/Configuration_Label_Example_03.png) 

```Python
        'device_2': {
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
```

## Example 4 (Device)
Center text only

![Cable QR Code](/docs/img/Configuration_Label_Example_04.png) 

```Python
        'device_2': {
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
```

## Example 5 (Device)
Text links only

![Cable QR Code](/docs/img/Configuration_Label_Example_05.png) 

```Python
        'device_2': {
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
```

## Example 6 (Device)
QR code only

![Cable QR Code](/docs/img/Configuration_Label_Example_06.png) 

```Python
        'device_2': {
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
```

## Example 7 (Device)
Upright, large font with line break and serial number

![Cable QR Code](/docs/img/Configuration_Label_Example_07.png) 

```Python
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
```

## Example 8 (Device)
Upright, large font with line break and serial number

![Cable QR Code](/docs/img/Configuration_Label_Example_08.png) 

```Python
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
```

## Example 9 (Device)
Small label

![Cable QR Code](/docs/img/Configuration_Label_Example_09.png) 

```Python
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
```

## Example 10 (Device) - Completely self-designed

This way, many label design options should be possible. The design of the label content is completely specified by the user via this method.

![Cable QR Code](/docs/img/Configuration_Label_Example_10.png)

Save this Netbox icon as an example in the following Netbox folder:
/opt/netbox/netbox/media/image-attachments/Netbox_Icon_Example.png

![Cable QR Code](/docs/img/Netbox_Icon_Example.png)

```Python
        'device_10': {
            'title': 'Example 10 (Template for Device)',
            'with_qr': False,
            'text_align_horizontal': 'center',
            'text_align_vertical': 'middle',
            'title': 'Example',
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
```

## Example 1 (Cable) - Cable Label vertical writing.

This example shows how to write vertically, e.g. for cable labeling on a wide but not so high single label.

![Cable QR Code](/docs/img/Configuration_Label_Example_11.png)

```Python
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
```

## Example 2 (Cable) - Cable Label vertical writing.

This example shows the creation of a Cabel label with barcode 128. Please note that an online function is used here (internet may be necessary). Barcode 128 is not created on the Netbox server.

![Cable QR Code](/docs/img/Configuration_Label_Example_12.png)

```Python
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
```

[<< Back to General Configuration](README_Configuration.md)
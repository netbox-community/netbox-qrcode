# Example label configurations

## Example 1 - Default
Standard label without customization

![Cable QR Code](/docs/img/Configuration_Label_Example_01.png) 

## Example 2 
QR code Higher than wide, with own logo Device name and Device ID filled with zeros.

![Cable QR Code](/docs/img/Configuration_Label_Example_02.png) 

```Python
        'device_2': {
            'title': 'Example',
            'text_template': '<div style="display: inline-block; height: 5mm; width: 15mm"><img src="{{ logo }}" height="100%" width="100%"></div><br>{{ obj.name }}<br>Device: {{ obj.id|stringformat:"07d" }}',
            'font_size': '4mm',
            'label_qr_width': '20mm',
            'label_qr_height': '30mm',
            'label_qr_text_distance': '2mm',
            'label_width': '56mm',
            'label_height': '32mm',
            'label_edge_top': '0mm',
            'label_edge_left': '2mm',
            'label_edge_right': '2mm',
            'logo': 'data:image/png;base64,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',
        },
```
## Example 3 
Text left QR code right with distance to the edge.

![Cable QR Code](/docs/img/Configuration_Label_Example_03.png) 

```Python
        'device_2': {
            'title': 'Example',
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

## Example 4
Center text only

![Cable QR Code](/docs/img/Configuration_Label_Example_04.png) 

```Python
        'device_2': {
            'title': 'Example',
            'font_size': '4mm',
            'text_location': 'center',
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

## Example 5 
Text links only

![Cable QR Code](/docs/img/Configuration_Label_Example_05.png) 

```Python
        'device_2': {
            'title': 'Example',
            'font_size': '4mm',
            'text_location': 'left',
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

## Example 6 
QR code only

![Cable QR Code](/docs/img/Configuration_Label_Example_06.png) 

```Python
        'device_2': {
            'title': 'Example',
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

## Example 7 
Upright, large font with line break and serial number

![Cable QR Code](/docs/img/Configuration_Label_Example_07.png) 

```Python
        'device_2': {
            'title': 'Example',
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
            'label_edge_bottom': '2mm',
        },
```

## Example 8 
Upright, large font with line break and serial number

![Cable QR Code](/docs/img/Configuration_Label_Example_08.png) 

```Python
        'device_2': {
            'title': 'Example',
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
        },
```

## Example 9 
Small label

![Cable QR Code](/docs/img/Configuration_Label_Example_09.png) 

```Python
        'device_2': {
            'title': 'Example',
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
        },
```

## Example 10 - Completely self-designed

This way, many label design options should be possible. The design of the label content is completely specified by the user via this method.

![Cable QR Code](/docs/img/Configuration_Label_Example_10.png)

```Python
        'device_2': {
            'with_qr': False,
            'text_location': 'center',
            'title': 'Example',
            'text_template': '<div style="display: inline-block; height: 5mm; width: 15mm"><img src="/static/netbox_logo.svg" height="100%" width="100%"></div><br>'
                             '{{ obj.name }} <br>'
                             '<div style="display: inline-block; height: 10mm; width: 10mm"><img src="data:image/png;base64,{{qrCode}}" height="100%" width="100%"/></div><br>' 
                             'Device: {{ obj.id|stringformat:"07d" }}'
                             '<p>&#128541; <font color="red"><b> My label design </b> </font> &#128541;</p>',
                             
            'label_width': '56mm',
            'label_height': '32mm',
            'label_edge_top': '0mm',
            'label_edge_left': '0mm',
            'label_edge_right': '0mm',
        },
```
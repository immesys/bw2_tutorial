from client import get_client
import ipywidgets as widgets
import os

class Widgets():
    def __init__(self, url, bw_agent=None, bw_entity=None):
        self._url = url
       
        # init light bulb 
        img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../images")
        img_light_on_path = os.path.join(img_path, "light_on.png")
        img_light_off_path = os.path.join(img_path, "light_off.png")
        self._img_light_on = open(img_light_on_path, "rb").read()
        self._img_light_off = open(img_light_off_path, "rb").read()
        self._light = widgets.Image(
            value=self._img_light_off,
            format='png',
            width=75,
            height=120,
        )
       
        # init switch 
        self._switch = widgets.Button(
            value=False,
            description='Toggle',
            disabled=False,
            button_style='',
        )
        self._switch.on_click(self._switch_on_click)
        
        # init a box widget that contains both the switch and light     
        items = (self._switch, self._light)
        box_layout = widgets.Layout(
            display='flex',
            flex_flow='row',
            align_items='center',
            border='solid',
            width='25%',
        )
        self._box = widgets.Box(children=items, layout=box_layout)
    
        # init WAVE client
        self._bw_client = get_client(agent=bw_agent, entity=bw_entity)
        self._bw_client.subscribe(url, self._light_callback)

    def display(self):
        display(self._box)

    def _switch_on_click(self, b):
        self._bw_client.publish(self._url, (2,0,0,1), {'switch': "toggle"})
    
    def _light_callback(self, msg):
        # print "received: ", msg.payload
        if "switch" in msg.payload:
            if msg.payload['switch'] == "toggle":
                if self._light.value is self._img_light_on:
                    self._light.value = self._img_light_off
                elif self._light.value is self._img_light_off:
                    self._light.value = self._img_light_on
    

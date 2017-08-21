from client import get_client
import ipywidgets as widgets
import os

class Widgets():
    def __init__(self, namespace = None, switch_name = "switch0", light_name = "light0", switch_entity = "switch.ent", light_entity = "light.ent", bw_agent = None):
        if namespace is None:
            namespace = os.environ.get('NAMESPACE')
        if namespace is None:
            raise Exception("Need to provide a namespace or set NAMESPACE")

        self._switch_url = namespace + "/s.switch/" + switch_name + "/i.boolean/signal/state"
        self._light_url = namespace + "/s.light/" + light_name + "/i.boolean/slot/state"
       
        # init light bulb 
        img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
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
        self._switch = widgets.ToggleButtons(
            options=['Turn On', 'Turn Off'],
            disabled=False,
            button_style='',
            tooltips=['Turn on the light', 'Turn off the light']
        )
        self._switch.value = "Turn Off"
        self._switch.observe(self._switch_on_click, 'value')
        
        # init a box widget that contains both the switch and light     
        items = (self._switch, self._light)
        box_layout = widgets.Layout(
            display='flex',
            flex_flow='row',
            align_items='center',
            border='solid',
            width='30%',
        )
        self._box = widgets.Box(children=items, layout=box_layout)
    
        # init WAVE client
        self._switch_bw_client = get_client(agent=bw_agent, entity=switch_entity)

        self._light_bw_client = get_client(agent=bw_agent, entity=light_entity)
        self._light_bw_client.subscribe(self._light_url, self._light_callback)

    def display(self):
        display(self._box)

    def switch_url(self):
        return self._switch_url

    def light_url(self):
        return self._light_url

    def _switch_on_click(self, change):
        if change['new'] == "Turn On":
            self._switch_bw_client.publish(self._switch_url, (64,0,0,1), "true")
        elif change['new'] == "Turn Off":
            self._switch_bw_client.publish(self._switch_url, (64,0,0,1), "false")
    
    def _light_callback(self, msg):
        # print "received: ", msg.payload
        if msg.payload.lower() == "true":
            self._light.value = self._img_light_on
        elif msg.payload.lower() == "false":
            self._light.value = self._img_light_off
        elif msg.payload.lower() == "toggle":
            if self._light.value is self._img_light_off:
                self._light.value = self._img_light_on
            elif self._light.value is self._img_light_on:
                self._light.value = self._img_light_off
    

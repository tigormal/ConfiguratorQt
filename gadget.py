from pathlib import Path
import paho.mqtt.client as mqtt

class NetworkNode:

    icon_name = 'node'
    name = ''
    type = ''
    vendor = ''
    model = ''

    def __init__(self, dict: dict):
        self.name = dict.get("name")
        self.type = dict.get("type")
        self.vendor = dict.get("vendor")
        self.model = dict.get("model")

        if self.type is not None:
            self.icon_name = self.type


class Gadget(NetworkNode):

    tags = []
    icon_name = 'generic'
    dashboard_name = ''

    def __init__(self, dict: dict):
        
        super.__init__(dict)

        self.uuid = dict.get("uuid")
        self.icon_name = dict.get("icon")
        self.dashboard_name = dict.get("dashboard")
        self.description = dict.get("description")

        self.handle = Path('~/Gadgets/sink').expanduser()
        self.telemetry = []

    def tell(self, arg: str, ack = False):
        msg = self.uuid + '\n' + arg
        if ack :
            msg = msg + '\n' + 'ACK'
        msg = msg + '\n'
        with open(self.handle, "w") as f:
            print('have opened sink, commencing writing...')
            f.write(msg)


class MQTTGadget(Gadget):

    def __init__(self, dict: dict, host, port=1883):
        super.__init__(dict)

        self.handle = mqtt.Client(self.name)
        self.handle.connect(host, port=port)
        self.handle.on_message=self.on_message
        self.handle.loop_start()

        for topic in self.get_sources_list():
            self.handle.subscribe(topic)

    def get_sources_list(self):
        # TODO:
        '''Get list of telemetry sources to subscribe to. Return list'''
        self.dashboard_name
        return []

    def tell(self, arg: str, ack = False):
        args = arg.split(' ', 1)
        if args.count() < 2:
            raise ValueError('Given too little arguments. >2 needed.')
        else:
            payload = args[1]
            topic = args[0]
            if topic[0] == '/':
                topic = topic[1:]
            self.handle.publish(topic, payload)

    def on_message(self, client, userdata, message):
        print("message received " ,str(message.payload.decode("utf-8")))
        print("message topic=", message.topic)
        self.telemetry[message.topic] = str(message.payload.decode("utf-8"))

    def __del__(self):
        self.handle.loop_stop()

    

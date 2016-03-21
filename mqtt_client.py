import urlparse
import paho.mqtt.client as mqttc

class MqttClient(mqttc.Client):
    CA_CERTS_FILE = "/etc/ssl/certs/ca-certificates.crt"

    def __init__(self, mqtt_url):
        mqttc.Client.__init__(self, protocol=mqttc.MQTTv311)
        parsed_url = urlparse.urlparse(mqtt_url)
        self.scheme = parsed_url.scheme
        self.username = parsed_url.username
        self.password = parsed_url.password
        self.hostname = parsed_url.hostname
        self.port = parsed_url.port

        if self.scheme == 'mqtts':
            self.tls_set(MqttClient.CA_CERTS_FILE)

        self.username_pw_set(self.username, self.password)

    def connect(self):
        mqttc.Client.connect(self, self.hostname, self.port, 60)
 

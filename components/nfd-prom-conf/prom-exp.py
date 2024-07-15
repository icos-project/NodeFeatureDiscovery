import requests
import time
from prometheus_client import start_http_server, Gauge
from prometheus_client.core import REGISTRY
import prometheus_client as prom

prom.REGISTRY.unregister(prom.PROCESS_COLLECTOR)
prom.REGISTRY.unregister(prom.PLATFORM_COLLECTOR)
prom.REGISTRY.unregister(prom.GC_COLLECTOR)


APISERVER="kubernetes.default.svc"
SERVICEACCOUNT="/var/run/secrets/kubernetes.io/serviceaccount"
TOKEN_PATH="{}/token".format(SERVICEACCOUNT)
CACERT_PATH="{}/ca.crt".format(SERVICEACCOUNT)

TOKEN_FILE=open(TOKEN_PATH, "r")
TOKEN=TOKEN_FILE.read()

headers = {
    'Authorization': 'Bearer {}'.format(TOKEN)
}





class Collector:
    def __init__(self, ):
        self.metric_gauge = Gauge(
            'node_mounted', 'devices mounted', ['node_uid','device']
        )

        self.devs=[]

    def fetch_k8s_node_usb_devices(self,metric_gauge):

        try:
            response = requests.get('https://{}/api/v1/nodes'.format(APISERVER), headers=headers, verify=CACERT_PATH)
            response.raise_for_status()
            data = response.json()
            cur_devs=[]
            for node in data['items']:
                node_uid = node['metadata']['uid']
                labels = node['metadata']['labels']
                for label_name, label_value in labels.items():
                    if label_name.startswith('feature.node.kubernetes.io/usb-'):
                        label_name = label_name.replace('feature.node.kubernetes.io/','')
                        label_name = label_name.replace('.present','')
                        if('usb-08' in label_name):
                            label_name = label_name.replace('usb-08','usb-storage')
                            cur_devs.append(label_name)
                            if(label_name not in self.devs):
                                self.devs.append(label_name)

                        if('usb-03' in label_name):
                            label_name = label_name.replace('usb-03','usb-human-interface-dev')
                            cur_devs.append(label_name)
                            if(label_name not in self.devs):
                                self.devs.append(label_name)


                        if('usb-ff' in label_name):
                            label_name = label_name.replace('usb-ff','usb-video')
                            cur_devs.append(label_name)
                            if(label_name not in self.devs):
                                self.devs.append(label_name)

                _diff = [x for x in self.devs if x not in cur_devs ]

                for cd in cur_devs:
                    self.metric_gauge.labels(node_uid=node_uid,device=cd).set(1)

                for cd in _diff:
                    self.metric_gauge.labels(node_uid=node_uid,device=cd).set(0)



        except Exception as e:
            print(f"Failed to fetch Kubernetes node devices: {str(e)}")


    def collect_info(self, ):
        self.fetch_k8s_node_usb_devices(self.metric_gauge)



if __name__ == '__main__':
    start_http_server(8081)
    collector = Collector()

    while True:
        time.sleep(1)
        collector.collect_info()

# Node Feature Discovery  with Prometheus

  

This module discovers and publishes the presence of mounted usb devices.

  
  

## Installation & Usage

This version uses helm charts. Follow the instruction provided bellow:

  

- git clone https://production.eng.it/gitlab/icos/meta-kernel/observability/nodefeaturediscovery.git

- cd nodefeaturediscovery

- helm install nfd icos-nfd/

  

After the deployment is completed 2 pods are created:

- **nfd-prom-exporter**: Custom component which is exposes the metrics to port **8081**

- **device-plugin**: exposes the resource of a usb device
  

In order to check the available metrics:

  

- Usb devices must be mounted

- Retrieve the **pod ip** of the **nfd-prom-exporter** and run **curl http://pod-ip:8081/metrics**

# Legal
The Node Feauture Discovery is released under the Apache license.
Copyright © 2022-2024 NCSRD. All rights reserved.

🇪🇺 This work has received funding from the European Union's HORIZON research and innovation programme under grant agreement No. 101070177.



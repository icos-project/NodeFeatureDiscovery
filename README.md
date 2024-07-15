# Node Feature Discovery with Prometheus

  

A customized version of [Node Feature Discovery](https://kubernetes-sigs.github.io/node-feature-discovery/v0.14/get-started/) with an embeded prometheus exporter. Currently this module discovers and publishes the presence of mounted usb devices.

  
  

## Installation & Usage

This current version uses kustomization manifests. Follow the instruction provided bellow:

  

- git clone https://production.eng.it/gitlab/icos/meta-kernel/observability/nodefeaturediscovery.git

- cd nodefeaturediscovery

- kubectl apply -k deploy

  

After the deployment is completed 4 pods are created:

- **nfd-prom-exporter**: Custom component which is exposes the metrics to port **8081**

- **nfd-master**: Writes feauture labels to kubernetes-api

- **nfd-worker**: Discovers the features of the nodes
- **generic-device-plugin**: exposes the resource of a usb device
  

In order to check the available metrics:

  

- Usb devices must be mounted

- Retrieve the **pod ip** of the **nfd-prom-exporter** and run **curl http://pod-ip:8081/metrics**

# Legal
The Node Feauture Discovery is released under the Apache license.
Copyright © 2022-2024  ICOS Consortium. All rights reserved.

🇪🇺 This work has received funding from the European Union's HORIZON research and innovation programme under grant agreement No. 101070177.



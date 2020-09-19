# LinkStateVisual

![Render from above output](https://i.imgur.com/J62lLgw.png)

Parses Cisco IOS CLI output for "show ip ospf database router" (the OSPF LSDB) to YAML, then creates a Networkx graph, which is rendered with pyGraphViz (To PNG file)

Inspired by https://github.com/theclam/ospfcli2dot

Command FSM template sourced from https://github.com/networktocode/ntc-templates

## Requires

```sudo apt-get install python3-dev graphviz libgraphviz-dev pkg-config```

### pip3
* pygraphviz
* networkx
* textfsm 
* pyaml

*NOTE that textfsm WILL NOT work on Windows.*

## Current Styleguide

### Vertices (nodes)

* Circles - Discovered devices by LSID (Routers)
* Double-circle - Router the LSDB is collected from
* Rectangles - Pseudonodes for transit segments

### Edge Types

* Black edges - Transit network links
* Red edges - Stub network links
* Blue edges - Point-to-point network links

## Usage

```
$ ./lsv.py -h
usage: lsv.py [-h] [--out OUT] [--dump] input_cli

LSDB Visualiser

positional arguments:
  input_cli   Txt containing CLI output of "show ip ospf database router"

optional arguments:
  -h, --help  show this help message and exit
  --out OUT   Output file name, defaults to multi.png
  --dump      Will print LSDB object as Yaml to stdout
```

## Example
```
$ ./lsv.py simple-cli-output.txt --dump
Area: '0'
PID: '1'
RouterLSID:
  1.1.1.1:
  - AdvertisingRouter: R1
    Checksum: '0x17E7'
    ConnectedTo: a Stub Network
    LSAge: '194'
    LSID: 1.1.1.1
    LSSeqNo: '80000002'
    LSType: Router Links
    Length: '48'
    LinkData: 255.255.255.255
    LinkID: 1.1.1.1
    Options: No TOS-capability, DC
    TOS0Metrics: '1'
    TOSMetrics: '0'
  - AdvertisingRouter: R1
    Checksum: '0x17E7'
    ConnectedTo: a Transit Network
    LSAge: '194'
    LSID: 1.1.1.1
    LSSeqNo: '80000002'
    LSType: Router Links
    Length: '48'
    LinkData: 10.0.0.1
    LinkID: 10.0.0.1
    Options: No TOS-capability, DC
    TOS0Metrics: '1'
    TOSMetrics: '0'
  2.2.2.2:
  - AdvertisingRouter: R2
    Checksum: '0x7EA'
    ConnectedTo: a Stub Network
    LSAge: '196'
    LSID: 2.2.2.2
    LSSeqNo: '80000002'
    LSType: Router Links
    Length: '48'
    LinkData: 255.255.255.255
    LinkID: 2.2.2.2
    Options: No TOS-capability, DC
    TOS0Metrics: '1'
    TOSMetrics: '0'
  - AdvertisingRouter: R2
    Checksum: '0x7EA'
    ConnectedTo: a Transit Network
    LSAge: '196'
    LSID: 2.2.2.2
    LSSeqNo: '80000002'
    LSType: Router Links
    Length: '48'
    LinkData: 10.0.0.2
    LinkID: 10.0.0.1
    Options: No TOS-capability, DC
    TOS0Metrics: '1'
    TOSMetrics: '0'
  3.3.3.3:
  - AdvertisingRouter: R3
    Checksum: '0x3160'
    ConnectedTo: a Stub Network
    LSAge: '21'
    LSID: 3.3.3.3
    LSSeqNo: '80000005'
    LSType: Router Links
    Length: '72'
    LinkData: 255.255.255.255
    LinkID: 3.3.3.3
    Options: No TOS-capability, DC
    TOS0Metrics: '1'
    TOSMetrics: '0'
  - AdvertisingRouter: R3
    Checksum: '0x3160'
    ConnectedTo: another Router (point-to-point)
    LSAge: '21'
    LSID: 3.3.3.3
    LSSeqNo: '80000005'
    LSType: Router Links
    Length: '72'
    LinkData: 10.3.4.1
    LinkID: 4.4.4.4
    Options: No TOS-capability, DC
    TOS0Metrics: '1'
    TOSMetrics: '0'
  - AdvertisingRouter: R3
    Checksum: '0x3160'
    ConnectedTo: a Stub Network
    LSAge: '21'
    LSID: 3.3.3.3
    LSSeqNo: '80000005'
    LSType: Router Links
    Length: '72'
    LinkData: 255.255.255.252
    LinkID: 10.3.4.0
    Options: No TOS-capability, DC
    TOS0Metrics: '1'
    TOSMetrics: '0'
  - AdvertisingRouter: R3
    Checksum: '0x3160'
    ConnectedTo: a Transit Network
    LSAge: '21'
    LSID: 3.3.3.3
    LSSeqNo: '80000005'
    LSType: Router Links
    Length: '72'
    LinkData: 10.0.0.3
    LinkID: 10.0.0.1
    Options: No TOS-capability, DC
    TOS0Metrics: '1'
    TOSMetrics: '0'
  4.4.4.4:
  - AdvertisingRouter: R4
    Checksum: '0xCFE4'
    ConnectedTo: a Stub Network
    LSAge: '22'
    LSID: 4.4.4.4
    LSSeqNo: '80000001'
    LSType: Router Links
    Length: '60'
    LinkData: 255.255.255.255
    LinkID: 4.4.4.4
    Options: No TOS-capability, DC
    TOS0Metrics: '1'
    TOSMetrics: '0'
  - AdvertisingRouter: R4
    Checksum: '0xCFE4'
    ConnectedTo: another Router (point-to-point)
    LSAge: '22'
    LSID: 4.4.4.4
    LSSeqNo: '80000001'
    LSType: Router Links
    Length: '60'
    LinkData: 10.3.4.2
    LinkID: 3.3.3.3
    Options: No TOS-capability, DC
    TOS0Metrics: '1000'
    TOSMetrics: '0'
  - AdvertisingRouter: R4
    Checksum: '0xCFE4'
    ConnectedTo: a Stub Network
    LSAge: '22'
    LSID: 4.4.4.4
    LSSeqNo: '80000001'
    LSType: Router Links
    Length: '60'
    LinkData: 255.255.255.252
    LinkID: 10.3.4.0
    Options: No TOS-capability, DC
    TOS0Metrics: '1'
    TOSMetrics: '0'
ThisLSR: 4.4.4.4
```


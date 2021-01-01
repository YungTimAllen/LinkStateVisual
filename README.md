# LinkStateVisual

![Rendered topo](https://imgur.com/xuIgoUu.png)

Parses Cisco IOS CLI output for "show ip ospf database router" (the OSPF LSDB) to YAML, then creates a Networkx graph, which is rendered with pyGraphViz (To PNG file)

Inspired by https://github.com/theclam/ospfcli2dot

Command FSM template and CLITable code sourced from https://github.com/networktocode/ntc-templates

## Requires

```sudo apt-get install python3-dev graphviz libgraphviz-dev pkg-config```

### pip3
* pygraphviz
* networkx
* textfsm 
* pyaml

*NOTE that textfsm WILL NOT work on Windows, unless via WSL*

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
- area: '0'
  ls_link_data: 255.255.255.255
  ls_link_id: 1.1.1.1
  ls_link_type: a Stub Network
  ls_mtid_metrics: '0'
  ls_tos_0_metrics: '1'
  lsa_abr: ''
  lsa_adv_router: R1
  lsa_age: '194'
  lsa_asbr: ''
  lsa_checksum: '0x17E7'
  lsa_id: 1.1.1.1
  lsa_length: '48'
  lsa_num_links: '2'
  lsa_options: No TOS-capability, DC
  lsa_seq_number: '80000002'
  lsa_type: Router Links
  process_id: '1'
  router_id: 4.4.4.4
- area: '0'
  ls_link_data: 10.0.0.1
  ls_link_id: 10.0.0.1
  ls_link_type: a Transit Network
  ls_mtid_metrics: '0'
  ls_tos_0_metrics: '1'
  lsa_abr: ''
  lsa_adv_router: R1
  lsa_age: '194'
  lsa_asbr: ''
  lsa_checksum: '0x17E7'
  lsa_id: 1.1.1.1
  lsa_length: '48'
  lsa_num_links: '2'
  lsa_options: No TOS-capability, DC
  lsa_seq_number: '80000002'
  lsa_type: Router Links
  process_id: '1'
  router_id: 4.4.4.4
- area: '0'
  ls_link_data: 255.255.255.255
  ls_link_id: 2.2.2.2
  ls_link_type: a Stub Network
  ls_mtid_metrics: '0'
  ls_tos_0_metrics: '1'
  lsa_abr: ''
  lsa_adv_router: R2
  lsa_age: '196'
  lsa_asbr: ''
  lsa_checksum: '0x7EA'
  lsa_id: 2.2.2.2
  lsa_length: '48'
  lsa_num_links: '2'
  lsa_options: No TOS-capability, DC
  lsa_seq_number: '80000002'
  lsa_type: Router Links
  process_id: '1'
  router_id: 4.4.4.4
- area: '0'
  ls_link_data: 10.0.0.2
  ls_link_id: 10.0.0.1
  ls_link_type: a Transit Network
  ls_mtid_metrics: '0'
  ls_tos_0_metrics: '1'
  lsa_abr: ''
  lsa_adv_router: R2
  lsa_age: '196'
  lsa_asbr: ''
  lsa_checksum: '0x7EA'
  lsa_id: 2.2.2.2
  lsa_length: '48'
  lsa_num_links: '2'
  lsa_options: No TOS-capability, DC
  lsa_seq_number: '80000002'
  lsa_type: Router Links
  process_id: '1'
  router_id: 4.4.4.4
- area: '0'
  ls_link_data: 255.255.255.255
  ls_link_id: 3.3.3.3
  ls_link_type: a Stub Network
  ls_mtid_metrics: '0'
  ls_tos_0_metrics: '1'
  lsa_abr: ''
  lsa_adv_router: R3
  lsa_age: '21'
  lsa_asbr: ''
  lsa_checksum: '0x3160'
  lsa_id: 3.3.3.3
  lsa_length: '72'
  lsa_num_links: '4'
  lsa_options: No TOS-capability, DC
  lsa_seq_number: '80000005'
  lsa_type: Router Links
  process_id: '1'
  router_id: 4.4.4.4
- area: '0'
  ls_link_data: 10.3.4.1
  ls_link_id: 4.4.4.4
  ls_link_type: another Router (point-to-point)
  ls_mtid_metrics: '0'
  ls_tos_0_metrics: '1'
  lsa_abr: ''
  lsa_adv_router: R3
  lsa_age: '21'
  lsa_asbr: ''
  lsa_checksum: '0x3160'
  lsa_id: 3.3.3.3
  lsa_length: '72'
  lsa_num_links: '4'
  lsa_options: No TOS-capability, DC
  lsa_seq_number: '80000005'
  lsa_type: Router Links
  process_id: '1'
  router_id: 4.4.4.4
- area: '0'
  ls_link_data: 255.255.255.252
  ls_link_id: 10.3.4.0
  ls_link_type: a Stub Network
  ls_mtid_metrics: '0'
  ls_tos_0_metrics: '1'
  lsa_abr: ''
  lsa_adv_router: R3
  lsa_age: '21'
  lsa_asbr: ''
  lsa_checksum: '0x3160'
  lsa_id: 3.3.3.3
  lsa_length: '72'
  lsa_num_links: '4'
  lsa_options: No TOS-capability, DC
  lsa_seq_number: '80000005'
  lsa_type: Router Links
  process_id: '1'
  router_id: 4.4.4.4
- area: '0'
  ls_link_data: 10.0.0.3
  ls_link_id: 10.0.0.1
  ls_link_type: a Transit Network
  ls_mtid_metrics: '0'
  ls_tos_0_metrics: '1'
  lsa_abr: ''
  lsa_adv_router: R3
  lsa_age: '21'
  lsa_asbr: ''
  lsa_checksum: '0x3160'
  lsa_id: 3.3.3.3
  lsa_length: '72'
  lsa_num_links: '4'
  lsa_options: No TOS-capability, DC
  lsa_seq_number: '80000005'
  lsa_type: Router Links
  process_id: '1'
  router_id: 4.4.4.4
- area: '0'
  ls_link_data: 255.255.255.255
  ls_link_id: 4.4.4.4
  ls_link_type: a Stub Network
  ls_mtid_metrics: '0'
  ls_tos_0_metrics: '1'
  lsa_abr: ''
  lsa_adv_router: R4
  lsa_age: '22'
  lsa_asbr: ''
  lsa_checksum: '0xCFE4'
  lsa_id: 4.4.4.4
  lsa_length: '60'
  lsa_num_links: '3'
  lsa_options: No TOS-capability, DC
  lsa_seq_number: '80000001'
  lsa_type: Router Links
  process_id: '1'
  router_id: 4.4.4.4
- area: '0'
  ls_link_data: 10.3.4.2
  ls_link_id: 3.3.3.3
  ls_link_type: another Router (point-to-point)
  ls_mtid_metrics: '0'
  ls_tos_0_metrics: '1000'
  lsa_abr: ''
  lsa_adv_router: R4
  lsa_age: '22'
  lsa_asbr: ''
  lsa_checksum: '0xCFE4'
  lsa_id: 4.4.4.4
  lsa_length: '60'
  lsa_num_links: '3'
  lsa_options: No TOS-capability, DC
  lsa_seq_number: '80000001'
  lsa_type: Router Links
  process_id: '1'
  router_id: 4.4.4.4
- area: '0'
  ls_link_data: 255.255.255.252
  ls_link_id: 10.3.4.0
  ls_link_type: a Stub Network
  ls_mtid_metrics: '0'
  ls_tos_0_metrics: '1'
  lsa_abr: ''
  lsa_adv_router: R4
  lsa_age: '22'
  lsa_asbr: ''
  lsa_checksum: '0xCFE4'
  lsa_id: 4.4.4.4
  lsa_length: '60'
  lsa_num_links: '3'
  lsa_options: No TOS-capability, DC
  lsa_seq_number: '80000001'
  lsa_type: Router Links
  process_id: '1'
  router_id: 4.4.4.4
```


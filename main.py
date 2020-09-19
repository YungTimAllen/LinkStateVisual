#!/usr/bin/env python3

# sudo apt-get install python3-dev graphviz libgraphviz-dev pkg-config
# sudo pip3 install pygraphviz
# sudo pip3 install networkx
# sudo pip3 install textfsm

import argparse
import networkx as nx
import textfsm
from networkx.drawing.nx_agraph import to_agraph
import re
import yaml


def main(args):

    fp = open(args.input_cli, 'r')
    lsdb = fsm_to_dict(fsm_parse(fp.read()))
    fp.close()

    if args.dump:
        print(yaml.dump(lsdb))

    build_nx_from_lsdb(lsdb)


def build_nx_from_lsdb(lsdb):

    g = nx.Graph()

    for lsr in lsdb["LSRs"]:
        for lsa in lsdb["LSRs"][lsr]:

            if "Stub" in lsa["ConnectedTo"]:
                g.add_edge(lsr, lsa["LinkID"], color='red')
                if "255.255.255.255" not in lsa["LinkData"]:
                    g.nodes[lsa["LinkID"]]["shape"] = 'rectangle'

            if "Transit" in lsa["ConnectedTo"]:
                g.add_edge(lsr, lsa["LinkID"])
                # https://graphviz.org/doc/info/shapes.html#polygon
                g.nodes[lsa["LinkID"]]["shape"] = 'rectangle'

            if "point-to-point" in lsa["ConnectedTo"]:
                g.add_edge(lsr, lsa["LinkID"], color='blue')

    for lsr in lsdb["LSRs"]:
        g.nodes[lsr]["shape"] = 'circle'

    g.nodes[lsdb["ThisLSR"]]["shape"] = 'doublecircle'

    A = to_agraph(g)
    A.layout('dot')
    A.draw('multi.png')


def fsm_to_dict(data):
    d = {}
    d["ThisLSR"] = data[0][0]
    d["PID"] = data[0][1]
    d["Area"] = data[0][2]
    d["LSRs"] = {}

    for line in data:
        d["LSRs"][line[6]] = []

    for line in data:
        t = {}
        t["LSAge"] = line[3]
        t["Options"] = line[4]
        t["LSType"] = line[5]
        t["LSID"] = line[6]
        t["AdvertisingRouter"] = line[7]
        t["LSSeqNo"] = line[8]
        t["Checksum"] = line[9]
        t["Length"] = line[10]
        t["ConnectedTo"] = line[14]
        t["LinkID"] = line[15]
        t["LinkData"] = line[16]
        t["TOSMetrics"] = line[17]
        t["TOS0Metrics"] = line[18]

        d["LSRs"][line[6]].append(t)

    return d


def fsm_parse(file):
    """Feeds CLI output to TextFSM file

    :param file: ml-string from file.read():
    :return: List of lists, parsed matches from TextFSM
    """
    with open("ios_show_ip_ospf_database_router.fsm") as fp_fsm:
        template = textfsm.TextFSM(fp_fsm)
    return template.ParseText(re.sub(r".*#.*\n", '', file))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='LSDB Visualiser')
    parser.add_argument("input_cli", help="Txt containing CLI output of \"show ip ospf database router\"")
    parser.add_argument("--dump", action='store_true', help="Will print LSDB object as Yaml to stdout")
    main(parser.parse_args())


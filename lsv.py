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

DEFAULT_OUTFILE = "multi.png"


def main(args):
    fp = open(args.input_cli, 'r')
    # Run input cli through TextFSM
    fsm_output = fsm_parse(fp.read())
    # Feed TextFSM output to parser (To DML)
    lsdb = fsm_to_dict(fsm_output)
    fp.close()

    # If Yaml dump switch set, make it so!
    if args.dump:
        print(yaml.dump(lsdb))

    # Create + draw (to png) nx MultiGraph from data-structure given by fsm_to_dict()
    draw_graphviz( build_nx_from_lsdb(lsdb), args.out if args.out else DEFAULT_OUTFILE)


def draw_graphviz(graph, output_file=DEFAULT_OUTFILE):
    # Weight labels
    for u, v, d in graph.edges(data=True):
        d['label'] = d.get('weight', '')

    A = to_agraph(graph)
    A.layout('dot')
    A.draw(output_file)


def build_nx_from_lsdb(lsdb):
    """
    Given DML, interprets LSDB as a MultiDiGraph

    :param lsdb:  Data structure of Dicts and Lists (DML-ready)
    :return:
    """
    g = nx.MultiDiGraph()

    for lsr in lsdb["RouterLSID"]:
        for lsa in lsdb["RouterLSID"][lsr]:

            if "Stub" in lsa["ConnectedTo"]:
                g.add_edge(lsr, lsa["LinkID"], color='red', weight=lsa["TOS0Metrics"])
                if "255.255.255.255" not in lsa["LinkData"]:
                    g.nodes[lsa["LinkID"]]["shape"] = 'rectangle'

            if "Transit" in lsa["ConnectedTo"]:
                g.add_edge(lsr, lsa["LinkID"], weight=lsa["TOS0Metrics"])
                # https://graphviz.org/doc/info/shapes.html#polygon
                g.nodes[lsa["LinkID"]]["shape"] = 'rectangle'

            if "point-to-point" in lsa["ConnectedTo"]:
                g.add_edge(lsr, lsa["LinkID"], color='blue', weight=lsa["TOS0Metrics"])

    # Set shape for all nodes to circle
    for lsr in lsdb["RouterLSID"]:
        g.nodes[lsr]["shape"] = 'circle'

    # LSDB originator gets a double-circle
    g.nodes[lsdb["ThisLSR"]]["shape"] = 'doublecircle'

    return g


def fsm_to_dict(data):
    """
    Given TextFSM data, parses into Dict of Dicts and Lists (DML-ready structure)

    :param data: TextFSM List of Lists, see return of fsm_parse()
    :return: Data structure of Dicts and Lists (DML-ready, print as Yaml by --dump)
    """
    d = {}
    d["ThisLSR"] = data[0][0]
    d["PID"] = data[0][1]
    d["Area"] = data[0][2]
    d["RouterLSID"] = {}

    for line in data:
        d["RouterLSID"][line[6]] = []

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

        d["RouterLSID"][line[6]].append(t)

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
    parser.add_argument("--out", help="Output file name, defaults to {}".format(DEFAULT_OUTFILE))
    parser.add_argument("--dump", action='store_true', help="Will print LSDB object as Yaml to stdout")
    main(parser.parse_args())


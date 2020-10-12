#!/usr/bin/env python3

# sudo pip3 install pygraphviz
# sudo pip3 install networkx
# sudo pip3 install textfsm

import argparse
import networkx as nx
from networkx.drawing.nx_agraph import to_agraph
from textfsm import clitable
import re
import yaml


DEFAULT_OUTFILE = "multi.png"


def main(args):
    with open(args.input_cli, 'r') as fp:
        # Run input cli through clitable
        fsm_output = fsm_parse(fp.read())

        # Parse LSDB to NetworkX object, then write to file
        LSV(fsm_output, args.out if args.out else DEFAULT_OUTFILE).run()

        # If Yaml dump switch set, make it so!
        if args.dump:
            print(yaml.dump(fsm_output))


def fsm_parse(mls, cmd="show ip ospf database router", platform="cisco_ios"):
    """
    Runs CLITable for given mls, using the given command, for the given platform
    :param mls: Multi-line string containing Cisco IOS CLI output for a command
    :param cmd: Command to run CLITable with
    :param platform: Platform to rune CLITable with
    :return: Structured Data (DML-Ready) return from CLITable
    """
    def clitable_to_dict(cli_tbl) -> list:
        """
        Sourced from github.com/ntc-templates
        :param cli_tbl: CLITable object
        :return: Structured Data (DML-Ready)
        """
        objs = []
        for row in cli_tbl:
            temp_dict = {}
            for index, element in enumerate(row):
                temp_dict[cli_tbl.header[index].lower()] = element
            objs.append(temp_dict)

        return objs

    # Index is a file that exists in the same directory as the FSMTemplate templates
    cli_table = clitable.CliTable("index", '.')
    attrs = {'Command': cmd, 'platform': platform}

    # Inline regex removes IOS shell prompt if seen on a line e.g. "hostname# "
    cli_table.ParseCmd(re.sub(r".*#.*\n", '', mls), attrs)

    return clitable_to_dict(cli_table)


class LSV:
    """
    Link-State Visualiser Class
    Requires:
    redhat: graphviz-devel python3-dev graphviz pkg-config
    debian: python3-dev graphviz libgraphviz-dev pkg-config
    Requires:
    import networkx as nx
    from networkx.drawing.nx_agraph import to_agraph
    """
    def __init__(self, lsdb, filename="output.png"):
        self.lsdb = lsdb
        self.filename = filename

    def run(self):
        """
        Calls build_nx_from_lsdb(self.lsdb) then draw_graphviz(g)
        i.e. Builds the nx graph object then writes to file + returns written path
        :return: str: Path to image file rendered
        """
        g = self.build_nx_from_lsdb(self.lsdb)
        return self.draw_graphviz(g)

    @staticmethod
    def build_nx_from_lsdb(lsdb):
        """
        Given structured data, interprets LSDB as a MultiDiGraph
        :param lsdb:  List of LSAs
        :return: networkx graph obj
        """
        g = nx.MultiDiGraph()

        for lsa in lsdb:


            if "Stub" in lsa["ls_link_type"]:
                g.add_edge(lsa["lsa_id"], lsa["ls_link_id"], color='red', weight=lsa["ls_tos_0_metrics"], area=lsa["area"])
                if "255.255.255.255" not in lsa["ls_link_data"]:
                    g.nodes[lsa["ls_link_id"]]["shape"] = 'rectangle'

            if "Transit" in lsa["ls_link_type"]:
                g.add_edge(lsa["lsa_id"], lsa["ls_link_id"], weight=lsa["ls_tos_0_metrics"], area=lsa["area"])
                g.nodes[lsa["ls_link_id"]]["shape"] = 'rectangle'

            if "point-to-point" in lsa["ls_link_type"]:
                g.add_edge(lsa["lsa_id"], lsa["ls_link_id"], color='blue', weight=lsa["ls_tos_0_metrics"], area=lsa["area"])

        # Set shape for all nodes to circle
        for lsa in lsdb:
            g.nodes[lsa["lsa_id"]]["shape"] = 'circle'

        # LSDB originator gets a double-circle
        g.nodes[lsdb[0]["router_id"]]["shape"] = 'doublecircle'

        # Weight labels
        for u, v, d in g.edges(data=True):
            d['label'] = f"Area: {d.get('area', '')} \nCost: {d.get('weight', '')}"

        return g

    def draw_graphviz(self, graph):
        """
        Given a nx graph object, prints (draws) to file and returns written filename
        :param graph: NetworkX Graph object
        :return:
        """
        g = to_agraph(graph)
        g.layout('dot')
        g.draw(self.filename)

        return self.filename


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='LSDB Visualiser')
    parser.add_argument("input_cli", help="Txt containing CLI output of \"show ip ospf database router\"")
    parser.add_argument("--out", help="Output file name, defaults to {}".format(DEFAULT_OUTFILE))
    parser.add_argument("--dump", action='store_true', help="Will print LSDB object as Yaml to stdout")
    main(parser.parse_args())

#!/usr/bin/python3

import MySQLdb as mdb
import networkx as nx
import argparse


class ModifiedPreorderTraversalTree:
    def __init__(self, graph):
        self.graph = graph
        self.left = {}
        self.right = {}

    def next(self, node=0, counter=0):
        counter += 1
        self.left[node] = counter

        for child_node in self.graph.neighbors(node):
            counter = self.next(child_node, counter)

        counter += 1
        self.right[node] = counter
        return counter

    def calc_left_right(self, root_node=0):
        self.next(root_node)
        return self.left, self.right


def get_connection_and_cursor(params):
    con = mdb.connect(
        host=params.host,
        user=params.user,
        passwd=params.password,
        db=params.database)

    cursor = con.cursor()
    return con, cursor


def get_graph(cursor):
    cursor.execute("select pid, id from Tags")
    return cursor.fetchall()


def write_left_right(cursor, left, right):
    for node in left:
        cursor.execute("update Tags set lft={}, rgt={} where id={}".format(left[node], right[node], node))


def build_graph(data):
    return nx.DiGraph(data)


def build_graph_debug():
    e = [(0, 1), (0, 2), (1, 3), (1, 4)]
    graph = nx.DiGraph(e)
    return graph


def build_modified_preorder_traversal_tree(G):
    mptt = ModifiedPreorderTraversalTree(G)
    mptt.next(0,1)
    return mptt.left, mptt.right


class ParamsDebug:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'dkuser'
        self.password = 'dkpasswd'
        self.database = 'digikam_devel_core'


class Params:
    def __init__(self):
        [self.host, self.user, self.password, self.database] = [None, None, None, None]
        self.parse_args()

    def parse_args(self):
        parser = argparse.ArgumentParser(description='Rebuild Digikam MYSQL Modified Preorder Traversal Tree')
        parser.add_argument('--host', default='localhost')
        parser.add_argument('-u', '--user', required=True)
        parser.add_argument('-p', '--password', required=True)
        parser.add_argument('-d', '--database', required=True)
        args = parser.parse_args()

        self.host = args.host
        self.user = args.user
        self.password = args.password
        self.database = args.database


def main():
    params = Params()

    connection, cursor = get_connection_and_cursor(params)
    data = get_graph(cursor)
    graph = build_graph(data)
    # graph = build_graph_debug()

    mptt = ModifiedPreorderTraversalTree(graph)
    left, right = mptt.calc_left_right(root_node=0)
    print(left)
    print(right)
    write_left_right(cursor, left, right)
    connection.commit()
    connection.close()


if __name__ == '__main__':
    main()

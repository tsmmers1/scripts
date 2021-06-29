import matplotlib
from matplotlib.pyplot import figure
import networkx as nx
import argparse
import os, sys
import itertools

def findnetworks(edges, network, nres):
        pos = len(network)
        for i in list(nres):
            if any(i in list(net) for net in network):
                continue
            else:
                network.append(set([i]))
                oldval = len(network[pos])
                newnetwork = findneighbors(edges, network[pos])
                while (len(newnetwork) - oldval) != 0:
                    oldval = len(newnetwork)
                    newnetwork = findneighbors(edges, newnetwork)
                    network[pos] = newnetwork
            pos = len(network)
        return network

def findneighbors(edges, network):
    for edge in edges:
        for node in edge:
            if node in network:
                network = network | set([i for i in edge])
    return network

def sortnodes(network, graph):
    network.sort(key = (lambda k: nres[k]))
    snetwork = []
    for node in network:
        neighbors = list(graph.neighbors(node))
        for i in neighbors:
            if i not in snetwork:
                snetwork.append(i)
    return snetwork


if __name__ == '__main__':
    """ Usage: python3 intermodel-network.py -s connectsets-compiled2.sif -o network.png """
    parser = argparse.ArgumentParser(description='Generate Network from sif files')
    parser.add_argument('-s', default='connectsets-compiled2.sif',help='SIF File')
    parser.add_argument('-o', default='network.png', help='Output Network PNG')
    parser.add_argument('-l', type=float, default=10.0, help='Figure vertial length')
    parser.add_argument('-w', type=float, default=10.0, help='Figure width')
    args = parser.parse_args()

    edges = []
    nres = {}
    with open(args.s, "r") as siffile:
        for line in siffile:
            if len(line.split()) != 3:
                print("Error: More code needed as non-3 SIF units exist.")
                sys.exit()
            edges.append((line.split()[0], line.split()[2]))
            if line.split()[0] not in nres:
                nres[line.split()[0]] = int(line.split()[0].split('_')[1].split('-')[0])
            if line.split()[2] not in nres:
                nres[line.split()[2]] = int(line.split()[2].split('_')[1].split('-')[0])

    #Identify isolate networks
    networks = []
    networks = findnetworks(edges, networks, nres)
    networks.sort(key=len, reverse = True)
    
    #Identify the Number of Levels and Start Position Counter
    minlevel = nres[min(nres.keys(), key=(lambda k: nres[k]))]
    levels = dict([(i,1) for i in range(nres[min(nres.keys(), key=(lambda k: nres[k]))], nres[max(nres.keys(), key=(lambda k: nres[k]))]+1)])
    
    #Identify the Width of the levels
    wlevels = dict([(k, len(list(l))) for k, l in itertools.groupby(sorted(nres.values()))])

    #Compute Network Positions
    length = args.l / (len(levels)+1)
    width = args.w
    pos = {}
    G=nx.Graph()
    G.add_edges_from(edges)
    for network in networks:
        snetwork = sortnodes(list(network), G)
        for node in snetwork:
            y = (nres[node] - minlevel + 1) * length
            x = (width / (wlevels[nres[node]]+1)) * levels[nres[node]]
            pos[node] = (x,y)
            levels[nres[node]]+=1

    color_map = []
    for node in G:
        if node.split("_")[0] == "res":
            color_map.append('blue')
        elif node.split("_")[0] == "qcombi":
            color_map.append('green')
        elif node.split("_")[0] == "dist":
            color_map.append('red')
        elif node.split("_")[0] == "trang":
            color_map.append('orange')

matplotlib.pyplot.figure(figsize=(args.l,args.w))
nx.draw(G, pos=pos, node_color = color_map, node_size=30)
matplotlib.pyplot.savefig('network.png')

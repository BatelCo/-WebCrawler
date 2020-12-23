# [[url_src1, url_dst1], [url_src2, url_dts2],...]
import random


def common_case():
    return random.randint(0, 100) < 85


def get_neighbour(random_node, list_of_pairs):
    adjacency_list = []
    for pair in list_of_pairs:
        if pair[0] == random_node:
            adjacency_list.append(pair[1])
    if len(adjacency_list) == 0:
        return None
    return adjacency_list[random.randint(0, len(adjacency_list) - 1)]


def add_to_dictionary(random_node, link_to_hits, j):
    if j == 0:
        if random_node in link_to_hits:
            link_to_hits[random_node] = [link_to_hits[random_node][0] + 1, 0]
        else:
            link_to_hits[random_node] = [1, 0]
    if j == 1:
        if random_node in link_to_hits:
            link_to_hits[random_node] = [link_to_hits[random_node][0], link_to_hits[random_node][0] + 1]
        else:
            link_to_hits[random_node] = [link_to_hits[random_node][0], 1]


def playerPagerank(listOfPairs):
    # [url] -> (first_hits, second_hits)
    link_to_hits = {}
    random_node = listOfPairs[random.randint(0, len(listOfPairs) - 1)][random.randint(0, 1)]
    current_node = random_node
    for j in range(2):
        for i in range(100000):
            add_to_dictionary(current_node, link_to_hits, j)
            if common_case():
                # follow a link
                neighbour = get_neighbour(current_node, listOfPairs)
                if neighbour is None:
                    continue
                else:
                    add_to_dictionary(neighbour, link_to_hits, j)
            else:
                current_node = listOfPairs[random.randint(0, len(listOfPairs) - 1)][random.randint(0, 1)]
    # Get Page Rank.
    for hits in link_to_hits.values():
        hits[0] /= 100000
        hits[1] /= 100000
    return link_to_hits

# go to random node

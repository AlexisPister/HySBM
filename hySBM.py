import networkx as nx
import random
import json
from collections import defaultdict, Counter

# This version has as parameters the number of nodes but also the number of hyperedges, so when p = q, we go back to the simple hypergraph random model



# Sample list of animal names
animal_names = [
    "cat", "dog", "elephant", "giraffe", "lion", "tiger", "panda", "koala", "kangaroo",
    "zebra", "hippo", "bear", "wolf", "fox", "rhino", "cheetah", "penguin", "dolphin",
    "whale", "shark", "eagle", "hawk", "falcon", "owl", "sparrow", "hummingbird", "parrot",
    "peacock", "duck", "swan", "goose", "rabbit", "squirrel", "deer", "moose", "gazelle",
    "monkey", "gorilla", "chimpanzee", "orangutan", "lemur", "hyena", "leopard", "panther",
    "crocodile", "alligator", "snake", "turtle", "frog", "lizard", "octopus", "squid", "crab",
    "lobster", "shrimp", "starfish", "jellyfish", "seahorse", "snail", "butterfly", "bee",
    "ant", "beetle", "ladybug", "spider", "scorpion", "tarantula", "hedgehog", "armadillo",
    "platypus", "kookaburra", "emu", "wombat", "tasmanian devil", "kiwi", "ostrich", "rhinoceros beetle",
    "buffalo", "moose", "raccoon", "skunk", "porcupine", "hedgehog", "polar bear", "walrus",
    "seal", "otters", "sloth", "anteater", "aardvark", "reindeer", "antelope", "caribou",
    "yak", "gnu", "hippopotamus", "hyena", "jackal", "elephant seal", "meerkat", "armadillo",
    "black bear", "chinchilla", "fennec fox", "lynx", "jaguar", "quokka", "tarsier", "anteater",
    "capybara", "okapi", "lemur", "leopard", "manatee", "numbat", "pangolin", "red panda",
    "serval", "tapir", "bongo", "bongo", "fossa", "gibbon", "saki monkey", "tit", "toucan",
    "star-nosed mole", "springhare", "armadillo girdled lizard", "numbat", "sugar glider", "wallaroo",
    "red-handed tamarin", "green basilisk", "glass frog", "flying dragon", "pufferfish", "blowfish",
    "lionfish", "scorpionfish", "mandarin fish", "blue tang", "parrotfish", "yellow tang",
    "flounder", "swordfish", "goblin shark", "hammerhead shark", "bull shark", "mako shark",
    "giant manta ray", "stingray", "sea turtle", "leatherback turtle", "box turtle",
    "green sea turtle", "giant panda", "red fox", "sea otter", "jaguar", "siberian tiger",
    "bald eagle", "harpy eagle", "humpback whale", "blue whale", "orca", "bottlenose dolphin",
    "gray wolf", "golden eagle", "african elephant", "indian elephant", "saltwater crocodile",
    "american alligator", "black rhinoceros", "white rhinoceros", "black mamba", "king cobra",
    "reticulated python", "green anaconda", "nile crocodile", "poison dart frog",
    "giant african millipede", "giant centipede", "tarantula", "giant desert hairy scorpion",
    "black widow spider", "african lion", "cheetah", "leopard", "giraffe", "african elephant",
    "grizzly bear", "polar bear", "red kangaroo", "blue whale", "bengal tiger", "siberian tiger",
    "american bison", "american flamingo", "african penguin", "african grey parrot",
    "green tree python", "chimpanzee", "koala", "arctic fox", "snow leopard", "red panda",
    "sloth", "raccoon", "meerkat", "black-footed ferret", "beaver", "giant panda", "honey badger",
    "prairie dog", "sea lion", "walrus", "gray whale", "elephant seal", "macaw", "scarlet macaw",
    "cockatoo", "hummingbird", "woodpecker", "kingfisher", "puffin", "hornbill", "horned owl",
    "barn owl", "peregrine falcon", "osprey", "buzzard", "red-tailed hawk", "harpy eagle",
    "bald eagle", "bearded vulture", "black vulture", "turkey vulture", "pheasant", "quail",
    "partridge", "guinea fowl", "dove", "pigeon", "stork", "crane", "flamingo", "pelican",
    "swan", "goose", "duck", "heron", "ibis", "egret", "spoonbill", "albatross", "seagull",
    "tern", "frigatebird", "penguin", "ostrich", "emu", "kiwi", "cassowary", "rhea", "toad",
    "frog", "salamander", "newt", "caecilian", "crocodile", "alligator", "gavial", "iguana",
    "chameleon", "komodo dragon", "gecko", "monitor lizard", "skink", "cobra", "viper",
    "rattlesnake", "black mamba", "king cobra", "anaconda", "python", "boa constrictor",
    "sea snake", "grass snake", "water snake", "garter snake", "hognose snake", "milk snake"]

def name_generator():
    random_animal = random.sample(animal_names, 1)[0]
    # animal_names.remove(random_animal)
    return random_animal
    # return ''.join(random.choice([chr(i) for i in range(ord('a'),ord('z'))]) for _ in range(6))


class Generator:
    def __init__(self, n_nodes: int = 100, n_hedges=100, n_coms=None, p_edge_intra: float = 0.20, p_edge_inter: float = 0.02, community_array: list[int] or None = None, sampling_strat="weighted"):
        self.n_nodes = n_nodes
        self.n_hedges = n_hedges if n_hedges else self.n_nodes
        self.n_coms = n_coms
        if not self.n_coms:
            self.n_coms = int(n_nodes / 30)

        self.p_edge_intra = p_edge_intra
        self.p_edge_inter = p_edge_inter
        self.community_array = community_array
        self.sampling_start = sampling_strat
        self.counter = 0

        self.node_type = "node"
        self.hyperedge_type = "hyperedge"

        if not self.community_array:
            # Random
            # self.community_array = [random.randint(0, self.n_coms - 1) for i in range(n_nodes)]

            # Same number of nodes per communities
            self.community_array = []
            for i in range(n_coms):
                self.community_array += [i for x in range(n_nodes // n_coms)]

        self.fixed_random_order = list(range(self.n_nodes))
        random.shuffle(self.fixed_random_order)

    def init_graph(self):
        self.G = nx.Graph()
        # self.node_to_com = {}
        self.all_nodes = []
        for idnode in range(self.n_nodes):
            name = self.new_name()
            community = self.community_array[idnode]
            self.G.add_node("p" + str(idnode), type=self.node_type, name=name, community=community)

    # O(n + m + m * n)
    def run(self, order_strat="random"):
        self.init_graph()

        for hedge in range(self.n_hedges):
            nodes = list(range(self.n_nodes))
            # random.shuffle(nodes)

            match order_strat:
                case "random":
                    random.shuffle(nodes)
                case "community-order":
                    # Nodes are grouped by their community
                    nodes = nodes
                case "fixed":
                    nodes = self.fixed_random_order

            # hyperedge = []
            first_node = random.choice(nodes)
            hyperedge = [first_node]
            
            for node in nodes:
                # add first node encountered in hyperedge for random order.
                # if order_strat == "random" and len(hyperedge) == 0:
                #     hyperedge.append(node)
                #     continue
                if node == first_node:
                    continue

                self.add_node_in_hyperedge(node, hyperedge)

            hid = self.create_hyperedge()
            for n in hyperedge:
                self.G.add_edge(hid, "p" + str(n))

    def add_node_in_hyperedge(self, node, hyperedge):
        if len(hyperedge) == 0:
            proba = self.p_edge_intra
            roll = random.random()
            if roll < proba:
                hyperedge.append(node)
            return
        
        if self.sampling_start == "first":
            self.add_node_firstproba(node, hyperedge)
        elif self.sampling_start == "weighted":
            self.add_weighted_proba(node, hyperedge)
        elif self.sampling_start == "frequent":
            self.add_node_mostfrequent_proba(node, hyperedge)
        elif self.sampling_start == "max":
            self.add_node_max_proba(node, hyperedge)
        elif self.sampling_start == "min":
            self.add_node_min_proba(node, hyperedge)

    def add_node_firstproba(self, node, hyperedge):
        com1 = self.community_array[node]
        com2 = self.community_array[hyperedge[0]]

        p = self.p_edge_intra if com1 == com2 else self.p_edge_inter
        roll = random.random()
        if roll < p:
            hyperedge.append(node)

    def add_weighted_proba(self, node, hyperedge):
        com = self.community_array[node]

        sum_p = 0
        for n in hyperedge:
            com2 = self.community_array[n]
            p = self.p_edge_intra if com == com2 else self.p_edge_inter
            sum_p += p
        weighted_proba = sum_p / len(hyperedge)
        
        roll = random.random()
        if roll < weighted_proba:
            hyperedge.append(node)

    def add_node_mostfrequent_proba(self, node, hyperedge):
        def most_frequent(List):
            return max(set(List), key=List.count)

        com = self.community_array[node]
        current_coms = [self.community_array[n] for n in hyperedge]
        most_frequent_com = most_frequent(current_coms)

        p = self.p_edge_intra if com == most_frequent_com else self.p_edge_inter
        roll = random.random()
        if roll < p:
            hyperedge.append(node)

    def add_node_max_proba(self, node, hyperedge):
        com = self.community_array[node]
        current_coms = [self.community_array[n] for n in hyperedge]

        same_com_present = False
        for com2 in current_coms:
            if com2 == com:
                same_com_present = True

        p = self.p_edge_intra if same_com_present else self.p_edge_inter
        roll = random.random()
        if roll < p:
            hyperedge.append(node)

    def add_node_min_proba(self, node, hyperedge):
        com = self.community_array[node]
        current_coms = [self.community_array[n] for n in hyperedge]

        other_com_present = False
        for com2 in current_coms:
            if com2 != com:
                other_com_present = True

        p = self.p_edge_inter if other_com_present else self.p_edge_intra
        roll = random.random()
        if roll < p:
            hyperedge.append(node)

    def run_fixed_size(self, node, hyperedge, nodes):
        hyperedge_created = False
        hyperedge_size = 1
        for i, node2 in enumerate(nodes):
            if node != node2:
                com1 = self.community_array[node]
                com2 = self.community_array[node2]

                p = self.p_edge_intra if com1 == com2 else self.p_edge_inter
                roll = random.random()
                if roll < p:
                    self.G.add_edge(hyperedge, "p" + str(node2))
                    hyperedge_size += 1
                    hyperedge_created = True

                if hyperedge_size == 3:
                    break

        return hyperedge_created

    def create_hyperedge(self):
        hyperedge = "h" + str(self.counter)
        self.counter += 1
        self.G.add_node(hyperedge, type=self.hyperedge_type)
        return hyperedge

    def degrees(self):
        nodes =  [node for node, attr in self.G.nodes(data=True) if attr["type"] == self.node_type]
        degrees = self.G.degree(nodes)
        return degrees

    def hyperedge_sizes(self):
        hedges =  [node for node, attr in self.G.nodes(data=True) if attr["type"] == self.hyperedge_type]
        degrees = self.G.degree(hedges)
        return degrees

    def hyperedges_composition(self):
        hedges_comp = []
        for hedge in [node for node, attr in self.G.nodes(data=True) if attr["type"] == self.hyperedge_type]:
            nodes = self.G[hedge]
            if len(nodes) == 0:
                continue
            
            coms = [self.G.nodes[n]["community"] for n in nodes]
            hedges_comp.append(coms)
        return hedges_comp

    # (max(n1, n2) / n1 + n2)
    def hyperedges_nmax(self):
        values = []
        for hedge in [node for node, attr in self.G.nodes(data=True) if attr["type"] == self.hyperedge_type]:
            nodes = self.G[hedge]
            
#             TODO: for now, remove empty hes
            if len(nodes) == 0:
                continue 
            
            coms = [self.G.nodes[n]["community"] for n in nodes]
            maxOccurrence = max(coms, key=coms.count)
            count = Counter(coms)
            maxCount = count[maxOccurrence]

            value = maxCount / len(coms)
            values.append(value)
        return values


    def ginis(self):
        ginis = []
        for hedge in [node for node, attr in self.G.nodes(data=True) if attr["type"] == self.hyperedge_type]:
            nodes = self.G[hedge]
            
#             TODO: for now, remove empty hes
            if len(nodes) == 0:
                continue 
            
            coms = [self.G.nodes[n]["community"] for n in nodes]
            count = Counter(coms)

            for i in range(self.n_coms):
                if not count[i]:
                    count[i] = 0

            gini = 0
            for i, (n_com, count_value) in enumerate(count.items()):
                for j, (n_com2, count_value2) in enumerate(count.items()):
                    # if j > i:
                        gini += abs(count_value - count_value2)

            xbar = 0
            for nc in count.values():
                xbar += nc / self.n_coms
                # xbar += nc / len(nodes)

            # gini = gini / ((self.n_coms ** 2) * xbar)
            # gini_norm = gini / ((self.n_coms - 1) / self.n_coms)

            gini = gini / (2 * (self.n_coms ** 2) * xbar)
            gini_norm = gini / (1 - 1/self.n_coms)

            ginis.append(gini_norm)
            # ginis.append(gini)

            self.G.nodes[hedge]["gini"] = gini_norm

        return ginis

    def ginis2(self):
        ginis = []
        for hedge in [node for node, attr in self.G.nodes(data=True) if attr["type"] == self.hyperedge_type]:
            nodes = self.G[hedge]

            if len(nodes) == 0:
                continue

            coms = [self.G.nodes[n]["community"] for n in nodes]

            # Avoid division by 0 later
            coms = sorted([com + 1 for com in coms])
            count = Counter(coms)

            t0 = 0
            t1 = 0

            for i, com in enumerate(coms):
                t0 += (i + 1) * com
                t1 += com

            gini = (2 * t0) / (len(nodes) * t1)
            gini = gini - (len(nodes) + 1) / len(nodes)

            ginis.append(gini)

        return ginis


    def mixed_he_fraction_to_count(self):
        edges_composition = self.hyperedges_composition()
        fraction_to_count = defaultdict(int)
        for he in edges_composition:
            n0 = he.count(0)
            fraction = round((n0 / len(he)) * 100, 3)
            fraction_to_count[fraction] += 1
        return fraction_to_count



    def hyperedges_types(self):
        hedges_comp = []
        for hedge in [node for node, attr in self.G.nodes(data=True) if attr["type"] == self.hyperedge_type]:
            nodes = self.G[hedge]
            coms = [self.G.nodes[n]["community"] for n in nodes]
            coms_set = set(coms)
            if len(coms_set) == 1:
                hedges_comp.append("pure")
            else:
                hedges_comp.append("mixed")
        return hedges_comp


    def new_name(self):
        name = name_generator()
        if name in dict(self.G.nodes(data="name")).values():
            name = name + "'"
        return name

    def to_json(self):
        graph_json = nx.node_link_data(self.G)
        graph_json["metadata"] = {
            "datasetName": "test",
            "edgeType": "type",
            "entityType": "type",
            "source_entity_type": self.hyperedge_type,
            "target_entity_type": self.node_type,
        }

        #         For Paohvis
        # graph_json["metadata"] = {
        #     "datasetName": "test",
        #     "edgeType": "label",
        #     "entityType": "label",
        #     "name": "name",
        #     "source_entity_type": "document",
        #     "target_entity_type": "person",
        #     "time_key": "time",
        #     "format": "2.1.0",
        #     "entity_type": "label",
        # }

        return graph_json

    def export(self):
        self.ginis()

        fp = f"hypergraphs_v2/{self.n_nodes}nodes_{self.p_edge_intra}p_{self.p_edge_inter}q_{self.sampling_start}.json"
        with open(fp, "w+") as path:
            json.dump(self.to_json(), path)

        with open("output.json", "w+") as path:
            json.dump(self.to_json(), path)

if __name__ == "__main__":
    RUN_SIM = False

    if RUN_SIM:
        sampling_strats = ["weighted", "max"]
        sizes = [60, 80, 100]
        # n_hedges = [60, 100, 300]
        n_coms = [2, 4, 6]

        for strat in sampling_strats:
            for size, n_com in zip(sizes, n_coms):
                print(size, n_com)
                gen = Generator(size, size, n_com, 0.20, 0.02, None, strat)
                gen.run()
                gen.export()


    # for q in [0.02, 0.005, 0.002, 0]:
    for q in [0.05, 0.02, 0.005, 0]:
        gen = Generator(80, 80, 4, 0.05, q, None, "frequent")
        gen.run()
        gen.export()


    # types = gen.hyperedges_types()
    # print(types)
    # print(gen.G)



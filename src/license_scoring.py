from abc import ABCMeta, abstractmethod
import pickle
import itertools
import pandas as pd

available_licenses = [
    'PD',
    'MIT',
    'BSD',
    'APACHE',
    'LGPL V2.1',
    'LGPL V2.1+',
    'LGPL V3+',
    'MPL 1.1',
    'GPL V2',
    'GPL V2+',
    'GPL V3+',
    'AGPL V3+']

class AbstractGnosis(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def train(cls, data_store):
        """
        Trains/De-dupes Gnosis from gnosis files, which should in the following json format:

        :param data_store: data store where various input gnosis files are stored
        :return: Gnosis object
        """
        return

    @abstractmethod
    def load(cls, data_store, filename):
        """
        Loads already saved Gnosis
        """
        return

    @abstractmethod
    def save(self, data_store, filename):
        """
        Saves the Gnosis in data_store
        """
        return

class LicenseVertex:
    def __init__(self, arg_list):
        self.id = arg_list[0]
        self.license_type = arg_list[1]
        self.adjacent = dict()

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

class GnosisLicense(AbstractGnosis):
    def __init__(self):
        self.vert_dict = dict()
        self.num_vertices = 0
        self.license_type_tuple = ('P', 'WP', 'SP', 'NP')

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        self.vert_dict[node.id] = node
        return node

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost=0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    def get_reachable_vertices(self, node):
        reachable_node_list = node.get_connections()
        for vertex in reachable_node_list:
            temp_list = vertex.get_connections()
            for temp_vertex in temp_list:
                if temp_vertex not in reachable_node_list:
                    reachable_node_list.append(temp_vertex)
        return [node] + reachable_node_list

    def get_license_vertex_by_id(self, id_name):
        for vertex in self.get_vertices():
            if vertex.id is id_name:
                return vertex
        return None

    def get_common_destination_license_vertex(self, list_of_licenses):
        reachable_vertex_list = None
        for i in xrange(0, len(list_of_licenses)):
            vertex = self.get_vertex(list_of_licenses[i])
            reachable_vertices = self.get_reachable_vertices(vertex)
            reachable_licenses = [x.id for x in reachable_vertices]
            if reachable_vertex_list is None:
                reachable_vertex_list = reachable_vertices
            else:
                reachable_vertex_list = [license_vertex for license_vertex in reachable_vertex_list if
                                         license_vertex.id in reachable_licenses]

        common_destination = None
        if len(reachable_vertex_list) > 0:
            for license_vertex in reachable_vertex_list:
                if license_vertex.id in list_of_licenses:
                    common_destination = [license_vertex]

            if common_destination is None:
                for license_type in self.license_type_tuple:
                    common_destination = [x for x in reachable_vertex_list if x.license_type is license_type]
                    if len(common_destination) > 0:
                        break
        return common_destination

    def train(cls, data_store):
        """
        Trains/De-dupes Gnosis from gnosis files, which should in the following json format:

        :param data_store: data store where various input gnosis files are stored
        :return: Gnosis object
        """
        return

    def load(cls, data_store, filename):
        """
        Loads already saved Gnosis
        """
        return

    def save(self, data_store, filename):
        """
        Saves the Gnosis in data_store
        """
        return

def create_license_graph():
    g = GnosisLicense()
    pd = LicenseVertex(['PD', 'P'])
    mit = LicenseVertex(['MIT', 'P'])
    bsd = LicenseVertex(['BSD', 'P'])
    apache = LicenseVertex(['APACHE', 'P'])
    lgpl2 = LicenseVertex(['LGPL V2.1', 'WP'])
    lgpl22 = LicenseVertex(['LGPL V2.1+', 'WP'])
    lgpl3 = LicenseVertex(['LGPL V3+', 'WP'])
    mpl = LicenseVertex(['MPL 1.1', 'WP'])
    gpl2 = LicenseVertex(['GPL V2', 'SP'])
    gpl22 = LicenseVertex(['GPL V2+', 'SP'])
    gpl3 = LicenseVertex(['GPL V3+', 'SP'])
    agpl3 = LicenseVertex(['AGPL V3+', 'NP'])

    g.add_vertex(pd)
    g.add_vertex(mit)
    g.add_vertex(bsd)
    g.add_vertex(apache)
    g.add_vertex(lgpl2)
    g.add_vertex(lgpl22)
    g.add_vertex(lgpl3)
    g.add_vertex(mpl)
    g.add_vertex(gpl2)
    g.add_vertex(gpl22)
    g.add_vertex(gpl3)
    g.add_vertex(agpl3)

    g.add_edge('PD', 'MIT')
    g.add_edge('MIT', 'BSD')
    g.add_edge('BSD', 'APACHE')
    g.add_edge('BSD', 'MPL 1.1')
    g.add_edge('BSD', 'LGPL V2.1')
    g.add_edge('BSD', 'LGPL V2.1+')
    g.add_edge('BSD', 'LGPL V3+')
    g.add_edge('APACHE', 'LGPL V3+')
    g.add_edge('LGPL V2.1+', 'LGPL V2.1')
    g.add_edge('LGPL V2.1+', 'LGPL V3+')
    g.add_edge('LGPL V2.1', 'GPL V2')
    g.add_edge('LGPL V2.1', 'GPL V2+')
    g.add_edge('LGPL V2.1+', 'GPL V2+')
    g.add_edge('LGPL V3+', 'GPL V3+')
    g.add_edge('GPL V2+', 'GPL V2')
    g.add_edge('GPL V2+', 'GPL V3+')
    g.add_edge('GPL V3+', 'AGPL V3+')

    return g

# This is the main function that does the scoring
def license_scoring(payload):
    payload_pd = create_df(payload)

    list_of_licenses = list(payload_pd.license)

    license_graph = create_license_graph()

    # Check if input licenses are present in license graph
    all_licenses_available_in_graph = licenses_avl(list_of_licenses)
    conflict_response = ""

    if all_licenses_available_in_graph == 1:
        # not all licenses are available
        s_license = ""
        conflict_licenses = ""

    else:

        stack_license = license_graph.get_common_destination_license_vertex(list_of_licenses)

        conflict_licenses = ""

        if stack_license is None:
            s_license = ''
            conflict_licenses = get_conflict_licenses(license_graph, list_of_licenses)
        else:
            s_license = [i.id for i in stack_license][0]

    # Create response object

    # Create response for conflict licenses
    
    if len(conflict_licenses) > 0:
        conflict_license_records = payload_pd[payload_pd.license.isin(conflict_licenses)].copy()
        conflict_license_records["pkg-ver"] = conflict_license_records.package + "-" + conflict_license_records.version
        conflict_response = conflict_license_records[["pkg-ver", "license"]].to_json(orient="records")

    response = {"stack_license": s_license, "conflict_license": conflict_response, "outlier_license": ""}

    return response

def get_conflict_licenses(license_graph, list_of_licenses):
    conflict_licenses = []

    for lic1, lic2 in itertools.combinations(list_of_licenses, 2):
        combination_license = license_graph.get_common_destination_license_vertex(list_of_licenses)

        if combination_license is None:
            conflict_licenses.append(lic1)
            conflict_licenses.append(lic2)

    return list(set(conflict_licenses))

def licenses_avl(list_of_licenses):
    license_diff = list(set(list_of_licenses) - set(available_licenses))
    if len(license_diff) > 0:
        print "The following licenses aren't available. Please check back later"
        print license_diff
        return 1
    else:
        return 0

def create_df(payload):
    df = pd.DataFrame({"package": [],
                       "version": [],
                       "license": []})

    for pkg in payload["packages"]:
        df_to_append = pd.DataFrame({"package": [pkg["package"]],
                                     "version": [pkg["version"]],
                                     "license": [pkg["license"][0]]})

        df = pd.concat([df, df_to_append], ignore_index=True)

    return df


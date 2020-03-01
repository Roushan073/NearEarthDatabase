from models import OrbitPath, NearEarthObject
import csv

class NEODatabase(object):
    """
    Object to hold Near Earth Objects and their orbits.

    To support optimized date searching, a dict mapping of all orbit date paths to the Near Earth Objects
    recorded on a given day is maintained. Additionally, all unique instances of a Near Earth Object
    are contained in a dict mapping the Near Earth Object name to the NearEarthObject instance.
    """

    def __init__(self, filename):
        """
        :param filename: str representing the pathway of the filename containing the Near Earth Object data
        """
        # TODO: What data structures will be needed to store the NearEarthObjects and OrbitPaths? -> dict
        # TODO: Add relevant instance variables for this.

        self.filename = filename
        self.date_neo_db = {} # Storing a dict of orbit date to list of NearEarthObject instances
        self.neo_object_db = {} # Storing a dict of the Near Earth Object name to the single instance of NearEarthObject

    def load_data(self, filename=None):
        """
        Loads data from a .csv file, instantiating Near Earth Objects and their OrbitPaths by:
           - Storing a dict of orbit date to list of NearEarthObject instances -> dict('orbitDate': List[NearEarthObject])
           - Storing a dict of the Near Earth Object name to the single instance of NearEarthObject -> dict('name': NearEarthObject)

        :param filename:
        :return: None
        """

        if not (filename or self.filename):
            raise Exception('Cannot load data, no filename provided')

        filename = filename or self.filename

        # TODO: Load data from csv file.
        # TODO: Where will the data be stored?

        """
        Reading neo_data.csv as dictionary and populating NearEarthObject and OrbitPath
        and initialising our two databases declared in __init__
        """
        with open(filename, 'r') as neo_data_file:
            reader = csv.DictReader(neo_data_file)
            for entry in reader:
                #print entry
                _orbit_date = entry["close_approach_date"]
                _neo_name = entry["name"]
                _neo_object = NearEarthObject(**entry)
                _orbit_path_object = OrbitPath(**entry)

                # Update date_orbit_db (Here storing neo_objects without orbit details)
                if _orbit_date in self.date_neo_db:
                    updated_neo_list = self.date_neo_db[_orbit_date] + [_neo_object]
                    self.date_neo_db[_orbit_date] = updated_neo_list
                else:
                    self.date_neo_db[_orbit_date] = [_neo_object]

                # Update neo_object_db (Here neo_objects are having orbit details)
                if _neo_name in self.neo_object_db:
                    curr_neo_obj = self.neo_object_db[_neo_name]
                    curr_neo_obj.update_orbits(_orbit_path_object, False)
                    self.neo_object_db[_neo_name] = curr_neo_obj
                else:
                    _neo_object.update_orbits(_orbit_path_object, False)
                    self.neo_object_db[_neo_name] = _neo_object

        return None
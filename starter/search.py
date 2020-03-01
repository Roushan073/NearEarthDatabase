from collections import namedtuple
from enum import Enum
from exceptions import UnsupportedFeature
from operator import *
from exceptions import *
from models import NearEarthObject, OrbitPath
from collections import defaultdict
from functools import reduce

class DateSearch(Enum):
    """
    Enum representing supported date search on Near Earth Objects.
    """
    between = 'between'
    equals = 'equals'

    @staticmethod
    def list():
        """
        :return: list of string representations of DateSearchType enums
        """
        return list(map(lambda output: output.value, DateSearch))

class Query(object):
    """
    Object representing the desired search query operation to build. The Query uses the Selectors
    to structure the query information into a format the NEOSearcher can use for date search.
    """

    Selectors = namedtuple('Selectors', ['date_search', 'number', 'filters', 'return_object'])
    DateSearch = namedtuple('DateSearch', ['type', 'values'])
    ReturnObjects = {'NEO': NearEarthObject, 'Path': OrbitPath}

    def __init__(self, **kwargs):
        """
        :param kwargs: dict of search query parameters to determine which SearchOperation query to use
        """
        # TODO: What instance variables will be useful for storing on the Query object?

        # number of output records
        self.output_count = None
        if "number" in kwargs:
            self.output_count = int(kwargs["number"])
        elif "n" in kwargs:
            self.output_count = int(kwargs["n"])

        # date
        self.date = None
        if "date" in kwargs:
            self.date = kwargs["date"]
        elif "d" in kwargs:
            self.date = kwargs["d"]

        # start_date
        self.start_date = None
        if "start_date" in kwargs:
            self.start_date = kwargs["start_date"]
        elif "s" in kwargs:
            self.start_date = kwargs["s"]

        # end_date
        self.end_date = None
        if "end_date" in kwargs:
            self.end_date = kwargs["end_date"]
        elif "e" in kwargs:
            self.end_date = kwargs["e"]

        # return_object
        self.return_object = "NEO"
        if "return_object" in kwargs:
            self.return_object = kwargs["return_object"]
        if self.return_object not in ["NEO", "Path"]:
            raise Exception("return_object: `{}` not found. Available return_objects: `{}`".
                            format(str(self.return_object), str(", ".join(["NEO", "Path"]))))

        # Filters
        self.filters = None
        if "filter" in kwargs:
            self.filters = kwargs["filter"]

    def build_query(self):
        """
        Transforms the provided query options, set upon initialization, into a set of Selectors that the NEOSearcher
        can use to perform the appropriate search functionality

        :return: QueryBuild.Selectors namedtuple that translates the dict of query options into a SearchOperation
        """
        # TODO: Translate the query parameters into a QueryBuild.Selectors object
        # Building DateSearch
        date_filter = []
        if self.date is None:
            date_filter += [Query.DateSearch(DateSearch.between, [self.start_date, self.end_date])]
        else:
            date_filter += [Query.DateSearch(DateSearch.equals, [self.date])]

        # Building Filters (diameter, distance, is_hazardous)
        neo_orbit_filters = []
        if self.filters is not None:
            filter_options = Filter.create_filter_options(self.filters) # defaultdict
            neo_filters = filter_options["NEO"]
            orbit_filters = filter_options["Path"]
            for neo_f in neo_filters:
                neo_orbit_filters += [Filter(neo_f.field, neo_f.object, neo_f.operation, neo_f.value)]
            for orbit_f in orbit_filters:
                neo_orbit_filters += [Filter(orbit_f.field, orbit_f.object, orbit_f.operation, orbit_f.value)]

        return Query.Selectors(date_filter, self.output_count, neo_orbit_filters, Query.ReturnObjects[self.return_object])


class Filter(object):
    """
    Object representing optional filter options to be used in the date search for Near Earth Objects.
    Each filter is one of Filter.Operators provided with a field to filter on a value.
    """
    Options = {
        # TODO: Create a dict of filter name to the NearEarthObject or OrbitalPath property
        "diameter": "NEO",
        "is_hazardous": "NEO",
        "distance": "Path"
    }

    Operators = {
        # TODO: Create a dict of operator symbol to an Operators method, see README Task 3 for hint
        ">": gt,
        ">=": ge,
        "=": eq,
        "<": lt,
        "<=": le
    }

    def __init__(self, field, object, operation, value):
        """
        :param field:  str representing field to filter on
        :param object:  str representing object to filter on
        :param operation: str representing filter operation to perform
        :param value: str representing value to filter for
        """
        self.field = field
        self.object = object
        self.operation = operation
        self.value = value

    def __str__(self):
        return "Field: {}, Object: {}, Operator: {}, Value: {}".format(str(self.field), str(self.object), str(self.operation), str(self.value))

    @staticmethod
    def create_filter_options(filter_options):

        """
        Class function that transforms filter options raw input into filters

        :param filter_options: list in format ["filter_option:operation:value_of_option", ...]
        :return: defaultdict with key of NearEarthObject or OrbitPath and value of empty list or list of Filters
        """
        def default_value():
            return []

        filter_list = defaultdict(default_value)
        neo_filters = []
        orbit_filters = []

        # TODO: return a defaultdict of filters with key of NearEarthObject or OrbitPath and value of empty list or list of Filters
        for _filter in filter_options:
            filter_str = _filter.split(":")
            _key = filter_str[0]
            if _key not in Filter.Options:
                raise Exception("Key: `{}` not found or Filter on key: `{}` is currently not supported. Available filter keys: `{}`".
                                format(str(_key), str(_key), str(", ".join(Filter.Options.keys()))))
            _object = Filter.Options[_key]
            _operation = Filter.Operators[filter_str[1]]
            _value = filter_str[2]
            if _object == "NEO":
                neo_filters.append(Filter(_key, _object, _operation, _value))
            elif _object == "Path":
                orbit_filters.append(Filter(_key, _object, _operation, _value))
            else:
                raise Exception('{} Object not supported for filtering'.format(str(_object)))

            filter_list["NEO"] = neo_filters
            filter_list["Path"] = orbit_filters

        return filter_list

    def apply(self, results):
        """
        Function that applies the filter operation onto a set of results

        :param results: List of Near Earth Object results
        :return: filtered list of Near Earth Object results
        """
        # TODO: Takes a list of NearEarthObjects and applies the value of its filter operation to the results
        if self.field == "diameter":
            return list(filter(lambda n: self.operation(n.diameter_min_km, float(self.value)), results))
        elif self.field == "is_hazardous":
            return list(filter(lambda n: self.operation(str(n.is_potentially_hazardous_asteroid).lower(), str(self.value).lower()), results))
        # Tricky Part
        elif self.field == "distance":
            updated_neo_results = []
            for neo in results:
                updated_neo_orbit = list(filter(lambda orbit: self.operation(orbit.miss_distance_kilometers, float(self.value)), neo.orbits))
                neo.update_orbits(updated_neo_orbit, True)
                if len(neo.orbits) > 0:
                    updated_neo_results.append(neo)
            return updated_neo_results
        else:
            raise Exception(
                "Key: `{}` not found or Filter on key: `{}` is currently not supported. Available filter keys: `{}`".
                format(str(self.field), str(self.field), str(", ".join(Filter.Options.keys()))))

class NEOSearcher(object):
    """
    Object with date search functionality on Near Earth Objects exposed by a generic
    search interface get_objects, which, based on the query specifications, determines
    how to perform the search.
    """

    def __init__(self, db):
        """
        :param db: NEODatabase holding the NearEarthObject instances and their OrbitPath instances
        """
        # TODO: What kind of an instance variable can we use to connect DateSearch to how we do search?
        self.db = db
        self.date_neo_db = db.date_neo_db
        self.neo_object_db = db.neo_object_db

    @staticmethod
    def apply_date_filter(data_set, date_filter):
        """
        :param data_set: input data_set on which date_filter to be applied
        :param date_filter: input date_filter
        :return: filtered data_set
        """
        # If date_filter is empty
        if not date_filter:
            return data_set
        else:
            filter_type = date_filter[0].type.value
            filter_values = date_filter[0].values

            if filter_type == "equals":
                neo_objects = dict(filter(lambda date: eq(date[0], filter_values[0]), data_set.items()))
            elif filter_type == "between":
                neo_objects = dict(filter(lambda date: ge(date[0], filter_values[0]) and le(date[0], filter_values[1]), data_set.items()))
            else:
                raise Exception("{} filter not supported for date".format(str(filter_type)))

            neo_names = set()
            for date in neo_objects:
                for neo in neo_objects[date]:
                    neo_names.add(neo.name)
            return list(neo_names)


    def get_objects(self, query):
        """
        Generic search interface that, depending on the details in the QueryBuilder (query) calls the
        appropriate instance search function, then applies any filters, with distance as the last filter.

        Once any filters provided are applied, return the number of requested objects in the query.return_object
        specified.

        :param query: Query.Selectors object with query information
        :return: Dataset of NearEarthObjects or OrbitalPaths
        """
        # TODO: This is a generic method that will need to understand, using DateSearch, how to implement search
        # TODO: Write instance methods that get_objects can use to implement the two types of DateSearch your project
        # TODO: needs to support that then your filters can be applied to. Remember to return the number specified in
        # TODO: the Query.Selectors as well as in the return_type from Query.Selectors

        # 1. Apply Date Filter
        # 2. Apply Filters (`NEO` and `ORBIT`)
        # 3. return_object (`NEO` or `ORBIT`) -> default = NEO
        # 4. number (output count)

        # unique NEO names list on/between some dates
        neo_names = NEOSearcher.apply_date_filter(self.date_neo_db, query.date_search)

        # unique NEO Objects list on/between some dates
        neo_objects = list(dict(filter(lambda neo: neo[0] in neo_names, self.neo_object_db.items())).values())

        # Handling extra filters, return_object and number
        if not query.filters:
            if query.return_object == NearEarthObject:
                return neo_objects[0:query.number]
            elif query.return_object == OrbitPath:
                orbits = map(lambda n: n.orbits, neo_objects)
                if not orbits:
                    return orbits[0:query.number]
                else:
                    return reduce(concat, orbits)[0:query.number]
            else:
                raise Exception("return_object: `{}` not found. Available return_objects: `{}`".
                                format(str(query.return_object), str(", ".join(["NEO", "Path"]))))
        else:
            neo_filters = filter(lambda f: f.object == "NEO", query.filters)
            orbit_filters = filter(lambda f: f.object == "Path", query.filters)

            # Adding Orbit Filter at last to filter with distance (object = ORBIT) at last
            all_filters = [*neo_filters, *orbit_filters]
            for _filter in all_filters:
                neo_objects = _filter.apply(neo_objects)

            if query.return_object == NearEarthObject:
                return list(neo_objects)[0:query.number]
            elif query.return_object == OrbitPath:
                orbits = map(lambda n: n.orbits, neo_objects)
                if not orbits:
                    return orbits[0:query.number]
                else:
                    return reduce(concat, orbits)[0:query.number]
            else:
                raise Exception("return_object: `{}` not found. Available return_objects: `{}`".
                                format(str(query.return_object), str(", ".join(["NEO", "Path"]))))
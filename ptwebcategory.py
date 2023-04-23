#!/usr/bin/python3

__version__ = "0.0.1"

import argparse
import sys
import logging

from halo import Halo
from typing import Callable
from ptlibs import ptjsonlib, ptmisclib
from CsvProvider import CsvProvider
from RequestCache import RequestCache
from classification.Clustering import Clustering
from classification.Dataset import Dataset
from exporting.JsonExporter import JsonExporter


class ptwebcategory:
    SHOW_EXPORT_PARAMETERS_ARG = "parameters"
    SHOW_EXPORT_AVERAGES_ARG = "averages"
    methods: dict[str, Callable[[Clustering], Callable]] = {
                'mean_shift': lambda classifier: classifier.mean_shift,
                'optics': lambda classifier: classifier.optics,
                'spectral_clustering': lambda classifier: classifier.spectral_clustering,
                'gaussian_mixture': lambda classifier: classifier.gaussian_mixture,
                'dbscan': lambda classifier: classifier.dbscan,
                'birch': lambda classifier: classifier.birch,
                'affinity_propagation': lambda classifier: classifier.affinity_propagation,
                'agglomerative_clustering': lambda classifier: classifier.agglomerative_clustering,
                'kmeans': lambda classifier: classifier.kmeans,
                'kmeans_mini_batch': lambda classifier: classifier.kmeans_mini_batch,
                'manual_clustering': lambda classifier: classifier.manual_clustering
            }
    
    def __init__(self, args):
        self.ptjsonlib = ptjsonlib.ptjsonlib(args.json)
        self.json_no = self.ptjsonlib.add_json("ptwebcategory")
        self.use_json = args.json
        self.args = args

    def run(self):
        if self.args.file:
            # Print file path
            print(self.args.file)
            # Initialize csv provider instance
            csv_provider = CsvProvider(self.args.file)
            # Check if evaluation only is enabled
            if not self.args.evaluation_only:
                # Request all loaded URLs and extract HTML, JavaScript, CSS and query parameters
                spinner = Halo(text="Requesting URLs...", spinner="dots", color = "white")
                spinner.start()
                RequestCache.request_parallel("GET", csv_provider.get_urls())
                spinner.stop()
                logging.info("Requesting URLs... Done")
                logging.info("Extracting HTML forms")
                csv_provider.extract_forms()
                logging.info("Extracting JavaScript")
                csv_provider.extract_javascript()
                logging.info("Extracting CSS")
                csv_provider.extract_css()
                logging.info("Extracting query parameters")
                csv_provider.extract_query()
                logging.info("Saving dataset CSV file")
                csv_provider.save_file()
            # Initialize dataset instance
            dataset = Dataset(csv_provider.rows_dict, start_from_col=2)
            # Initialize classifier instance
            classifier = Clustering(dataset)
            # Select clustering method name from args
            clustering_method_name = self.args.clustering_method
            # Get clustering method from methods dict
            clustrering_method = self.methods[clustering_method_name](classifier)
            logging.info(f"{clustering_method_name} clustering")
            classified_df = clustrering_method()
            logging.info(f"{clustering_method_name} clustering... Done")
            # Check if json output is enabled
            if self.args.json is not None:
                # Initialize json exporter instance
                exporter = JsonExporter(csv_provider.get_urls())
                # Set json exporter parameters
                exporter.export_with_parameters = self.SHOW_EXPORT_PARAMETERS_ARG in self.args.json
                # Set json exporter averages
                exporter.export_with_averages = self.SHOW_EXPORT_AVERAGES_ARG in self.args.json
                logging.info("Exporting to json file")
                # Export to json file
                exporter.export_to_file(classified_df, "export.json")
            # Wait for user confirmation
            input("Press enter to exit...")
        sys.exit(0)
        

def get_help():
    return [
        {"description": [
            "Target categorization tool for web application penetration testing"]},
        {"usage": ["ptwebcategory <options>"]},
        {"usage_example": [
            "ptwebcategory -f",
        ]},
        {"options": [
            ["-f", "--file", "<file path>", "Load urls from file"],
            ["-j", "--json", "", "Output in JSON format. Available options: parameters, averages"],
            ["-v", "--version", "", "Show script version and exit"],
            ["-h", "--help", "", "Show this help message and exit"],
            ["-e", "--evaluation-only", "", "Run only evaluation on already created dataset"],
            ["-m", "--clustering-method", "", "Clustering method to use. Default: kmeans. Available: mean_shift, optics, spectral_clustering, gaussian_mixture, dbscan, birch, affinity_propagation, agglomerative_clustering, kmeans, kmeans_mini_batch, manual_clustering"]
        ]
        }]


def parse_args():
    # Initialize argument parser
    parser = argparse.ArgumentParser(
        add_help=False, usage=f"{SCRIPTNAME} <options>")
    # Add arguments
    parser.add_argument("-f", "--file", type=str)
    parser.add_argument("-j", "--json", nargs="*", choices=[ptwebcategory.SHOW_EXPORT_PARAMETERS_ARG, ptwebcategory.SHOW_EXPORT_AVERAGES_ARG])
    parser.add_argument("-v", "--version", action="version",
                        version=f"%(prog)s {__version__}")
    parser.add_argument("-e", "--evaluation-only", action="store_true")
    parser.add_argument("-m", "--clustering-method", choices=list(ptwebcategory.methods.keys()), default="kmeans")
    # Check if no arguments were passed or help was requested
    if len(sys.argv) == 1 or "-h" in sys.argv or "--help" in sys.argv:
        ptmisclib.help_print(get_help(), SCRIPTNAME, __version__)
        sys.exit(0)
    # Parse arguments
    args = parser.parse_args()
    # Print banner
    ptmisclib.print_banner(SCRIPTNAME, __version__, args.json)
    # Return parsed arguments
    return args


def main():
    global SCRIPTNAME
    SCRIPTNAME = "ptwebcategory"
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    args = parse_args()
    script = ptwebcategory(args)
    script.run()


if __name__ == "__main__":
    main()
![penterepTools](https://www.penterep.com/external/penterepToolsLogo.png)


# PTCATEGORY
> Target categorization tool for web application penetration testing

## Installation
```
pip install -r requirements.txt
```

## Usage examples

```
ptcategory -f ./dataset-test.csv                   # Load dataset (CSV)
ptcategory -f ./dataset-test.csv -e                # Load dataset only for clustering
```

## Options
```
   -f   --file                <file>          Load dataset (CSV)
   -e   --evaluation-only                     Run only evaluation on already created dataset
   -j   --json                                Output in JSON format
   -v   --version                             Show script version and exit
   -h   --help                                Show this help message and exit
   -m   --clustering-method                   Clustering method to use. Default: kmeans. Available: mean_shift, optics, spectral_clustering, gaussian_mixture, dbscan, birch, affinity_propagation, agglomerative_clustering, kmeans, kmeans_mini_batch, manual_clustering
```

## Dependencies
- beautifulsoup4
- halo
- kneed
- matplotlib
- numpy
- pandas
- ptlibs
- ptthreads
- requests
- scikit_learn
- tldextract
- tqdm
- lxml

We use [ExifTool](https://exiftool.org/) to extract metadata.
Python 3.6+ is required.

## Version History
* 0.0.1
    * Alpha releases

## License

Copyright (c) 2022 Penterep Security s.r.o.

ptcategory is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

ptcategory is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with ptcategory.  If not, see <https://www.gnu.org/licenses/>.

## Warning

You are only allowed to run the tool against the websites which
you have been given permission to pentest. We do not accept any
responsibility for any damage/harm that this application causes to your
computer, or your network. Penterep is not responsible for any illegal
or malicious use of this code. Be Ethical!

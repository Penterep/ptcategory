![penterepTools](https://www.penterep.com/external/penterepToolsLogo.png)


# PTWEBCATEGORY
> Target categorization tool for web application penetration testing

## Usage examples

```
ptwebcategory -f ./dataset-test.csv                   # Load dataset (CSV)
ptwebcategory -f ./dataset-test.csv -e                # Load dataset only for clustering
```

## Options
```
   -f   --file                <file>          Load dataset (CSV)
   -e   --evaluation-only                     Run only evaluation on already created dataset
   -j   --json                                Output in JSON format
   -v   --version                             Show script version and exit
   -h   --help                                Show this help message and exit
```

## Dependencies
- ptlibs

We use [ExifTool](https://exiftool.org/) to extract metadata.
Python 3.6+ is required.

## Version History
* 0.0.1
    * Alpha releases

## License

Copyright (c) 2022 Penterep Security s.r.o.

ptwebcategory is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

ptwebcategory is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with ptwebcategory.  If not, see <https://www.gnu.org/licenses/>.

## Warning

You are only allowed to run the tool against the websites which
you have been given permission to pentest. We do not accept any
responsibility for any damage/harm that this application causes to your
computer, or your network. Penterep is not responsible for any illegal
or malicious use of this code. Be Ethical!

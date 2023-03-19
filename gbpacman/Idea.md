# GBPACMAN: Idea

## 


- Get the input from user as a commandline input
- Check in mys link and list the matching packages
- Show if no matching package found
- Download the zip file for the selected package and verify checksum
- unzip to the configured directory
- create the target directory structure if not present
- if the same filename exists : skip


## Critical

- cleanup imports : avoid cycles
## TODO

- function name refactoring
  - for filters : is_
  - for parsers: 
    - extract : returns soup
    - get : returns value / tuple
- check if network call is successful : returncode ✅


- dependencies
- zstd
- check env variable for installation folder


- log file 
  - cleaning it once in a while


- dependencies for a package



- zstd cleanup
  - dont download if already downloaded
  - unzip fn reuse

- list of installed packages

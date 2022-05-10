# Kayak Web Scrapper :airplane:

Don't know where to go this weekend ? Use this simple scrapper and let yourself be guided by the cheapest trips from your city.

## Installation 

To install the dependencies, just run : 

```bash 
make build-env
```


## Usage 

To use it, you have two options : with a little GUI or with a configuration file.

### 1. GUI

The graphical interface is obtained by running the following commands :

```bash 
$ source .venv/bin/activate
$ python3 main.py --timeout 10
```

### 2. Configuration file

Place your configuration files in *./configs/* with all the necessary information (maximum price, dates, departure airport) and run : 

```bash 
$ source .venv/bin/activate
$ python3 main.py --config "your_config_file.yaml" --timeout 10
```


**Remark:** If you have some errors, try to increase the timeout. 
Sometimes, it's just that the web page didn't have time to load.

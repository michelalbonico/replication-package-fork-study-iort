# Replication Package of Paper at SBCARS 2021

Our methodology consists of 3 main phases, as illustrated in the figure bellow. You can get aware of it by checking [our paper](https://nuvem.utfpr.edu.br/index.php/s/jWcSX4fDkBYdvnJ).

![MSR Methodology](./methodology.png)

## Data Analysis

Most of the process was automated by using shell scripts, as you will see in the sequence. We also provide the Python scripts that crawl the GitHub repositories. That was the first try, when we faced problems with more than 1000 repositories.

The scripts are organized as the following:
```
./scripts/
    |--- crawling/     		      Scripts in Python that automate GitHub crawling with Selenium.
         |--- setup.sh          Shell script that installs Selenium chromedriver.
         |--- requirements.txt  Python dependencies. Type "pip install -r requirements.txt".
         |--- keywords          List of terms to be searched.
         |--- getdata.py        Python script that crawls GitHub.
         |--- data/             SQlite dataset from the crawling.
    |--- git_api/       		    Shell scripts that automate the search with Git REST API.
         |--- extract.sh        Shell script that extracts GitHub content into JSON files.
         |--- run.sh            Shell script where the extract.sh parameters are set.
         |--- data              JSON files from the shell scripts.
```

1) 

1) Selecting the repositories that contain the proposed terms:
``
$ export terms=
$ export where=
$ export date=
$ export ii=
$ export dir=
$ export file=
$ export i=
$ curl -u $user:$hash "https://api.github.com/search/repositories?q=$terms+in:$where+created:$date&per_page=100&page=$ii"
-o $dir"/"$file"-"$i".json"
``
2) sdfsdf

You got here, so it seems that you are interested, right? Check out our data analysis [here](https://docs.google.com/spreadsheets/d/1CsLUjaCNy3LT6rFMImbM0fqySriKSE5gOBEp0ZMEQho/edit?usp=sharing)

If you either find inconsistencies or need some extra explanation, drop an email at [mailto](mailto:michelalbonico@utfpr.edu.br).

## Check our Presentation for SBCARS

The slides are available [here](#).

This is the recorded video.

## Selected Repositories

This work resulted in the following list of IoRT repositories.

![Selected Repositories](./selected-repos.png)

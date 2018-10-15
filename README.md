# AlmanacScraper
Scraper that scrapes weather data from almanac.com

## Steps to run the script

* Clone the repository using `git clone https://github.com/yashrsharma44/AlmanacScraper.git`
* Create a virtualenv `virtualenv --python=python3.5 venv`
* Type `. venv/bin/activate` to activate the virtualenv
* Install the dependencies `pip install requests` `pip install bs4` `pip install tqdm`.
* cd into the folder
* Run `python main.py`
* After use, deactivate the virtualenv using `deactivate`.

All list of data will be created, containing csv files of each states. By default, the starting and ending dates are 1st January 1998, and 2nd January 1998.

## Note 
For Parallel Processing, please use `sidpr.py`, `tapaaspr.py` and `biswapr.py`. Please set the value of PROCS, to reasonable number as you consider the value according to specs of computer.


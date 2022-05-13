# OpenX-Intern
A solution for two tasks. 



## How to run and test programs - Windows 

### 0. Download repository

There is need to install `git`.

Run ``cmd`` then type ``cd`` in order to find place where repository should be installed.

Next, download it by typing: 

``
git clone https://github.com/MatBar99/OpenX-Intern.git 
`` 




### 1. Create virtual environment in Python and install requirements:

Run ``cmd`` and install ``pip`` and ``virtualenv`` if necessary.


 - Create virtual environment, where you have downloaded repository and call it f.e. ``myenv``:

`` python3 -m venv myenv``

 - Run virtual environment: 

``myenv\Scripts\activate``

- Install given requirements:
``pip install -r requirements.txt``


### 2. In order to check first task, run ``task1.py``:

```
 python task1.py
```

### 3. In order to check second task, run ``find-available-slot.py`` (with example arguments):

```
 python find-available-slot.py --calendars "in" --duration-in-minutes 30 --minimum-people 2
```
For the first task, due to long time of execution and spontaneous errors (non existing websites, bad formatting of .json files etc.) I have decided to:
1. Save results of Supply Chain in `paths.txt` file.
2. Reduce the number of analyzed subsellers up to 20 per one seller.

For the second task, I have decided to create "reference date" according to .pdf file - 2022-07-01 09:00:00. 

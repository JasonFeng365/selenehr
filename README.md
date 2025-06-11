# SeleneHR: Selenium wrapper for HackerRank in Python

## Overview

SeleneHR and the sample CLI ~~sends files to an unpaid Jason's computer for him to upload~~ automates uploading problem data to HackerRank through Selenium, cause I was too lazy to manually upload SCPE content.

## Installation and Usage

SeleneHR requires `selenium` to be installed. The HackerRank CLI requires `argparse` and `dotenv`.

To use SeleneHR and the CLI, download the repository. You will need to edit `.env` and add your browser token to the `SESSION` field. To find this token, login to HackerRank and find the `_hrank_session` cookie under `www.hackerrank.com`. Copy the hexadecimal string in the `Content` field to the `.env` file.

## Files

Along with `selene_hr.py`, the actual Selenium wrapper, this repository has a small CLI to automate uploading problem information to HackerRank.

### selene_hr.py

`selene_hr.py` is the file containing the actual Selenium wrapper. It contains a `SeleneHR` class, which can be used elsewhere to automatically update or upload problems and testcases. See `hr_cli.py` for sample usage.

### hr_cli.py

This is a CLI I use for ease of editing problem statements and testcases, along with uploading them to HackerRank. It has commands for testcase generation, problem statement parsing, uploading new problems, and updating existing problems. Every command requires the directory of the problem to be passed in afterwards. Commands are as follows:

`tgen`/`tg`: Generate testcases from a template and generator file, by calling `gen.py` in the root directory.

`hr tg "sample\Euler's Multiples Redux"`

`tzip`/`tz`: Zip existing testcases within the problem's `testcases` directory into `testcases.zip`.

`hr tz "sample\Euler's Multiples Redux"`

`tbuild`/`tb`: Calls `tgen` and `tzip` sequentially.

`hr tb "sample\Euler's Multiples Redux"`

`tempty`/`te`: Create $n$ empty testcases within the problem's `testcases` directory. Files `input00.txt` through `input(n-1).txt` are created in `testcases/input`, and `output00.txt` through `output(n-1).txt` are created in `testcases/output`.

`hr tb "sample\Euler's Multiples Redux" 5`

`tupload`/`tu`: Upload existing testcases in the problem's `testcases.zip` file into HackerRank, using SeleneHR. Fails if the problem is missing a `hr_info/hr_pid.txt` file, as the problem needs to exist on HackerRank before testcases are uploaded.

`hr tu "sample\Euler's Multiples Redux"`

`mdparse`/`md`: Parse an existing Markdown file into `hr_info/statement.json`. Fields are `statement`, `inputFormat`, `constraints`, and `outputFormat`. Please edit `compileStatement.py` to make a custom parser.

`hr md "sample\Euler's Multiples Redux"`

`upload`: Upload a problem statement into HackerRank, using SeleneHR. If the problem is missing a `hr_info/hr_pid.txt` file, creates a new problem. Otherwise, updates the problem with HackerRank ID matching the ID inside the text file. Requires `hr_info/statement.json`.

`hr upload "sample\Euler's Multiples Redux"`

`push`: Calls `tbuild`, `mdparse`, `upload`, and `tupload` sequentially.

`hr push "sample\Euler's Multiples Redux"`

### Various .bat files

With the exception of `zip_tests.bat`, `.bat` files are wrappers for the individual `.py` files, allowing a user to simply type in the filename to the terminal on Windows. For example, instead of typing in `python hr_cli.py ...`, a user only has to type in `hr ...`.

`zip_tests.bat` generates a `.zip` file of the testcases of a directory. Later, I may change this to a Python file that accomplishes the same purpose.

With the exception of `zip_tests.bat`, all other `.bat` files can be safely removed.
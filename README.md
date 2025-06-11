# SeleneHR: Selenium wrapper for Python

---

## Overview

## Installation and Usage

## Files

### selene_hr.py

### hr_cli.py

This is a CLI I use for ease of editing problem statements and testcases, along with uploading them to HackerRank. It has commands for testcase generation, problem statement parsing, uploading new problems, and updating existing problems. Every command requires the directory of the problem to be passed in afterwards. Commands are as follows:

`tgen`/`tg`: Generate testcases from a template and generator file, by calling `gen.py` in the root directory.

`hr tg "sample\Euler's Multiples Redux"`

`tzip`/`tz`: Zip existing testcases within the problem's `testcases` directory into `testcases.zip`.

`hr tz "sample\Euler's Multiples Redux"`

`tbuild`/`tb`: Call `tgen` and `tzip` consecutively.

`hr tb "sample\Euler's Multiples Redux"`

`tempty`/`te`: Create $n$ empty testcases within the problem's `testcases` directory. Files `input00.txt` through `input(n-1).txt` are created in `testcases/input`, and `output00.txt` through `output(n-1).txt` are created in `testcases/output`.

`hr tb "sample\Euler's Multiples Redux" 5`

`tupload`/`tu`: Upload existing testcases in the problem's `testcases.zip` file into HackerRank, using SeleneHR. Fails if the problem is missing a `hr_info.hr_pid.txt` file, as the problem needs to exist on HackerRank before testcases are uploaded.

`hr tu "sample\Euler's Multiples Redux"`

`mdparse`/`md`: Parse an existing Markdown

`hr tu "sample\Euler's Multiples Redux"`

### Various .bat files

With the exception of `zip_tests.bat`, `.bat` files are wrappers for the individual `.py` files, allowing a user to simply type in the filename to the terminal on Windows. For example, instead of typing in `python hr_cli.py ...`, a user only has to type in `hr ...`.

`zip_tests.bat` generates a `.zip` file of the testcases of a directory. Later, I may change this to a Python file that accomplishes the same purpose.

With the exception of `zip_tests.bat`, all other `.bat` files can be safely removed.
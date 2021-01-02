## Table of contents
* [General info](#general-info)
* [Setup](#setup)

## General info
This project is code extracted from the question ["How to send email attachments?"](https://stackoverflow.com/questions/3362600/how-to-send-email-attachments)

## Setup
To build and install this package:

```
# Read code to see if it all looks legit
$ python setup.py build bdist_wheel
# copy vendor_packages folder to your code base
# Add vendor folder to PYTHONPATH
$ pip install vendor_packages/*.whl -t vendor
```
Don't push to pypi unless you put substantial effort into it, pypi is already full of junk.

Credits and License
-------------------
- martineau <https://stackoverflow.com/users/355230>
- BuZZ-dEE <https://stackoverflow.com/users/183704>
- Richard <https://stackoverflow.com/users/323332>
- AdrianBR <https://stackoverflow.com/users/1747405>
- Pinocchio <https://stackoverflow.com/users/3167448>
- Hinchy <https://stackoverflow.com/users/1520834>

# Web User Authentication Full Stack Simulator
The goal of this project is to demonstrate how passwords are securely stored on a backend, and how the frontend communicates with the backend. In order to accomplish this, I avoided using any frameworks, libaries, or external tools: the frontend for this project is developed using plain HTML, CSS, and JS, and the backend is developed using python standard libraries only. Thus, this project unboxes how libraries like Flask or Django actually work, and shows how something as simple as a SQLite3 database can be used to safely store user information. Python's `hashlib` (sha512 and scrypt, selectable by the user) was used in order to hash passwords and store them in a database using Modular Crypt Format (MCF).

## How to use
First, clone this repository
```
git clone https://github.com/mattbriggs04/web-user-auth.git
```
Ensure you have a recent verson of python installed (>= Python 3.9). Only the python standard library is used, so there are no additional requirements for everything to work. Run `app.py`.
```
python3 app.py
```
This will start a webserver on port 8020 by default.

## In Progress
- Add SSL (HTTPS). Since this is a simulator run locally, this is not a major issue. However, in deployment, it's essential that HTTPS is used for secure transmission of private data.

# License
This repository is under the MIT license. See `License.md` for more information.

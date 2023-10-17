# Sure App Backend Take Home Challenge

## Introduction

The following application implements a pricing algorithm for Acme Home Insurance.  It takes into account several key features of a potential customer's characteristics including:

- Coverage type
- State of residence
- Pet Ownership
- Interest in Flood Coverage

## Getting Started

### Requirements

To install the following application, the user needs Python, Pip, and a shell they are comfortable working with.  I recommend bash or zsh.

- Python >= 3.11
- Pip >= 23.2.1

### Installation
1. Clone the git repository to your working directory
```
$ git clone https://github.com/tselwitz/sure-app-challenge.git 
```
2. Navigate to the working directory
```
$ pwd
${WORKING_DIR}/sure-app-challenge
```

3. The following step is optional, but recommended. This creates a virtual environment for dependency isolation.
```
$ python3 -m venv .env
$ source ./.env/bin/activate
```

4. Install dependencies
```
$ pip3 install -r req.txt
```

5. Start the application
```
$ cd acme_insurance
$ python3 manage.py runserver
```
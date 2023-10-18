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

### Teardown

To exit the python virtual environment:
```
$ deactivate
```

## Testing

Note: all of these steps require the python virtual environment to be activated.
### To run the automated test suite:
```
$ cd sure-app-challenge/acme-insurance
$ python3 manage.py test
```

### To test via the exposed REST API:

While typically frowned upon, I have checked in my SQLite Database containing the data described in the problem statement.  This allows for easy testing.

**Note: that all string and id based query parameters in this exercise are case sensitive.**

After starting the application, to submit a quote for rating, use the following request:
```
POST localhost:8000/home/quote/
```
With the following body:
```json
{
    "name": "Test Case 4", # Can be any string
    "coverage": "Basic", # "Premium" is also valid
    "state": "Texas", # "California" and "New York" are valid
    "has_pet": false, # true or false
    "has_flood_coverage": true # true or false
}
```
You will recieve a response with the ID and other relevant query information:
```json
{
    "id": "6c85fcd7-b1a9-4d2a-9c93-533f7f1def95",
    "name": "Test Case 4",
    "has_pet": false,
    "has_flood_coverage": true,
    "coverage": {
        "id": "72b76039-16bf-441e-b941-0a994710228a",
        "base_coverage_type": "Basic",
        "price": 20.0
    },
    "coverage_state": {
        "id": "012a4c74-bcdc-4333-9bf2-8cb168f2b3e8",
        "state": "Texas",
        "tax_multiplier": 0.005,
        "flood_multiplier": 1.5
    },
    "subtotal": 30.0,
    "taxes": 0.15,
    "total_price": 30.15
}
```
To query the quote information:
```
GET localhost:8000/home/quote?id=6c85fcd7-b1a9-4d2a-9c93-533f7f1def95
```
```
GET localhost:8000/home/quote/
```
To get a prettified view of the quote, you can use the "rater" method.
```
localhost:8000/home/quote/rater?id=5a11a71e-e784-4fd2-ba58-5b51d664a62a
```
To recieve:
```json
{
    "id": "5a11a71e-e784-4fd2-ba58-5b51d664a62a",
    "subtotal": "$60.00",
    "taxes": "$0.30",
    "total_price": "$60.30"
}
```
I support other query parameters as well:
```
GET localhost:8000/home/quote?has_pet=True
```

### Other exposed routes

The following routes have GET, POST, and DELETE methods:
#### Base Coverage
This is for retrieving, updating, creating, and deleting Base Coverage types such as Premium and Basic coverage.
```
localhost:8000/home/base_coverage/
```
Parameters:
```
-> id: uuid
-> base_coverage_type: string
-> price: float
```
#### Additional Costs
This is for retrieving, updating, creating, and deleting Additional Costs types such as Pet Fees.
```
localhost:8000/home/additional_costs/
```
Parameters:
```
-> id: uuid
-> description: string
-> price: float
```
#### State of Coverage
This route is used for retrieving, updating, creating, and deleting State specific information such as tax multipliers, and flood insurance multipliers.
```
localhost:8000/home/state/
```
Parameters:
```
-> id: uuid
-> state: string
-> tax_multiplier: float (Usage note: if the tax amount is 2%, input as 0.02)
-> flood_multiplier: float (Usage note: if the flood multiplier is 2%, input as 0.02)
```
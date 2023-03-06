

# Flask Cafe API

This is a Flask-based API for managing cafes. It allows users to add, update, delete, and search for cafes, as well as retrieve a random cafe or a list of all cafes. 

## Installation

1. Clone this repository
2. Install the required packages: `pip install -r requirements.txt`
3. Run the app: `python main.py`

## Endpoints

- `/` - Render the API documentation 
- `/random` - Get a random cafe
- `/all` - Get all cafes
- `/cafe/<int:cafe_id>` - Get a single cafe by ID
- `/search` - Search for a cafe by location
- `/add` - Add a new cafe
- `/update-price/<int:cafe_id>` - Update the price of a cafe
- `/delete/<int:cafe_id>` - Delete a cafe

For more information on each endpoint and how to use them, please see the API documentation. 

## API Documentation

Please see `https://documenter.getpostman.com/view/17571014/2s93JowRG3` for detailed documentation on how to use each endpoint. 

## Author

This API was developed by Mamour DIOP.

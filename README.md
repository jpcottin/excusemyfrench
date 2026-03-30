# Excusemyfrench

excusemyfrench is the application beyond https://excusemyfrench.herokuapp.com/

## Local Setup and Installation

1. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Run the application locally:
   ```bash
   export PORT=5000
   python3 app.py
   ```
   The app will be available at `http://localhost:5000/`.

## Running Tests

To run the unit tests, simply execute:
```bash
python3 test_app.py
```

## List of Features
----

### Original simple insult
    will return you a random French insult
      https://excusemyfrench.herokuapp.com/

### Insult with image
    will include not only a random French insult *but also* a random picture of an authentic French person.
      https://excusemyfrench.herokuapp.com/img

### Specific Insult with specific image
    will include a specific insult/picture (based of the index in fixed tables)
      https://excusemyfrench.herokuapp.com/img/<number>/<number> like https://excusemyfrench.herokuapp.com/img/127/1

### Flow of Insults with image
    will refresh automatically the insult ( with image ) every second
      https://excusemyfrench.herokuapp.com/series

### API version
    will return a JSON response of the insult ( see [Detail of the API] )
    https://excusemyfrench.herokuapp.com/api

## Details of the API
----

### Return of a single insult
  Returns json data of a single insult.

* **URL:** `/api/v1`
* **Method:** `GET`
* **Success Response:**
  * **Code:** 200
    **Content:**
    ```json
    {
      "insult":
      {
        "text": "Playboy De Superette" ,
        "index": 356
      }
    }
    ```

### Return of an insult AND an image
  Returns json data of an insult and the base64 encoded image

* **URL:** `/api/v1/img`
* **Method:** `GET`
* **Success Response:**
  * **Code:** 200
    **Content:**
    ```json
    {
      "insult": {
        "text": "Loutre Analphabète",
        "index": 254
      },
      "image": {
        "data": "/9j/4AA*****",
        "mimetype": "image/jpg",
        "indexImg": 10
      }
     }
    ```

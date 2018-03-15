# excusemyfrench*


excusemyfrench is the application beyond https://excusemyfrench.herokuapp.com/ 



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

* **URL**

  /api/v1

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**
 
   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** Sucessful Response will return the insult as a STRING and its index number in the base used.

    ```json
    { 
      "insult": 
      { 
        "text": "Playboy De Superette" , 
        "index": 356
      } 
    }
    ```

 
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ error : "You are unauthorized to make this request." }`

* **Sample Call:**

  ```javascript
    $.ajax({
      url: "/api/v1",
      dataType: "json",
      type : "GET",
      success : function(r) {
        console.log(r);
      }
    });
  ```

  or a simple
`curl https://excusemyfrench.herokuapp.com/api/v1` will return 
`{"insult": { "text": "Playboy De Superette" , "index": 356} }`


### Return of an insult AND an image
  Returns json data of an insult and the base64 encoded image

* **URL**

  /api/v1/img

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**
 
   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** Sucessful Response will return the insult as a STRING and its index number in the base used.
    In Addition it will return an image with its base64 encoded data, its mimetype and its index number in the base used.

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

 
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ error : "You are unauthorized to make this request." }`

* **Sample Call:**

  ```javascript
    $.ajax({
      url: "/api/v1/img",
      dataType: "json",
      type : "GET",
      success : function(r) {
        console.log(r);
      }
    });
  ```


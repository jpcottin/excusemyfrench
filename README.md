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

  /api

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**
 
   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{result: Guignol}`
 
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ error : "You are unauthorized to make this request." }`

* **Sample Call:**

  ```javascript
    $.ajax({
      url: "/api",
      dataType: "json",
      type : "GET",
      success : function(r) {
        console.log(r);
      }
    });
  ```

  or a simple
`curl https://excusemyfrench.herokuapp.com/api` will return 
`{result: Putassière}`

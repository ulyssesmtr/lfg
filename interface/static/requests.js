const formFieldsApiUrl = "http://localhost:8000/api/v1/loanfield/";
const addLoanApiUrl = "http://localhost:8000/api/v1/loan/";

function titleCase(string) {
    var sentence = string.toLowerCase().split(' ');
    for(var i = 0; i< sentence.length; i++){
       sentence[i] = sentence[i][0].toUpperCase() + sentence[i].slice(1);
    }
 return sentence.join(' ');
}

async function fetchJSON(url) {
  try {
      const response = await fetch(url);

      if (!response.ok) {
          throw new Error('Request failed with status:', response.status);
      }
      const jsonResponse = await response.json();
      return jsonResponse;
  } catch (error) {
      console.error('Error:', error);
      throw error;
  }
}

function submitForm(e) {
  e.preventDefault()
  var formData = $("#loan-form").serializeArray(); 
  payload = {
    "name": formData.shift().value,
    "document": {}
  }
  for (let key in formData) {
    obj = formData[key]
    payload.document[obj.name] = obj.value
  }
  fetch(addLoanApiUrl, {
    method: "POST",
    body: JSON.stringify(payload),
    headers: new Headers({'content-type': 'application/json'}),
  })
  .then((response) => {
    if (response.ok) {
        return response.json().then((data) => {
            alert('Your loan submission was sucessfuly received.');
            window.location.reload();
        });
    } else if (response.status === 400) {
        return response.json().then((errorObj) => {
          alert(JSON.stringify(errorObj));
          window.location.reload();});
    } else {
        console.log(response.statusText);
    }
  })
  .catch((err) => {
      console.log(String(err));
  });
}

$(document).ready(function() {
  // Fetches the loan form fields from the api and creates
  // the form inputs when page is loaded
  fetchJSON(formFieldsApiUrl)
  .then(formFields => {
      for (let key in formFields) {
        if (formFields.hasOwnProperty(key)) {
            value = formFields[key];

            let newInput = document.createElement("input");
            newInput.id = value.name
            newInput.name = value.name
            newInput.setAttribute('type', value.input_type);

            let newlabel = document.createElement("Label");
            newlabel.setAttribute("for", newInput.id);
            newlabel.innerHTML = titleCase(value.name);

            if (value.required){
              newInput.setAttribute('required', value.required);
              newlabel.classList.add('required');
            }
    
            let newDiv = document.createElement('div');
            newDiv.classList.add('item');

            let formColumn = document.getElementById("form-columns")
            formColumn.appendChild(newDiv)

            newDiv.appendChild(newlabel);
            newDiv.appendChild(newInput);

            }
        }
  })
    .catch(error => {
        console.error('An error occurred:', error);
    });

  var myform = document.getElementById("loan-form");
  myform.addEventListener("submit", submitForm);
});
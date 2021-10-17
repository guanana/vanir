function getPrice(url){
 var token_from = document.querySelector('[id=select2-id_token_from-container]').innerText
 var token_to = document.querySelector('[id=select2-id_token_to-container]').innerText
 var account_name = document.querySelector("#id_account").selectedOptions[0].innerHTML
 if ( token_from && token_to && account_name){
   $.ajax({                       // initialize an AJAX request
    url: url,
    data: {
      'token_from': token_from,       // add the token_from to the GET parameters
      'token_to': token_to,           // add the token_to to the GET parameters
      'account_name': account_name    // add the account_name to the GET parameters
    },
    success: function (data) {   // `data` is the return of the `TokenPriceAutocomplete` view function
      if (document.querySelector("#id_price")) {
          $("#id_price")[0].value = data;  // replace the contents of the price input with the data that came from the server
          $("#id_price")[0].placeholder = data;
      }else{
          $("#id_stopprice")[0].value = data;
          $("#id_stopprice")[0].placeholder = data
      }
    }
  });
 }
}

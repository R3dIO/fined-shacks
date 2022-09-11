$(document).ready(function () {
    $("form").submit(function (event) {
      var formData = {
        name: $("#fullname").val(),
        email: $("#email").val(),
        age: $("#age").val(),
        sex: $("#sex").val(),
        martial_status: $("#martial_status").val(),
        race: $("#race").val(),
        occupation: $("#occupation").val(),
        income: $("#income").val(),
        health_insurance: $("#health_insurance").val(),
        personal_savings: $("#personal_savings").val(),  
        monthly_living_expenses: $("#living_expenses").val(),
        investment: $("#investment").val(),
        credit_cards_issued: $("#number_of_cards").val(),
        credit_score: $("#credit_score").val(),
        city:  $("#city").val(),  
      };
  
      console.log(formData);
  
      $.ajax({
        type: "POST",
        url: "http://www.google.com",
        data: formData,
        dataType: "json",
        encode: true,
      }).done(function (data) {
        console.log(data);
      });
  
      event.preventDefault();
    });
  });
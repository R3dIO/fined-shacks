$(function () {
    var $sections = $('.form-section');
  
    function navigateTo(index) {
      // Mark the current section with the class 'current'
      $sections
        .removeClass('current')
        .eq(index)
          .addClass('current');
      // Show only the navigation buttons that make sense for the current section:
      $('.form-navigation .previous').toggle(index > 0);
      var atTheEnd = index >= $sections.length - 1;
      $('.form-navigation .next').toggle(!atTheEnd);
      $('.form-navigation [type=submit]').toggle(atTheEnd);
    }
  
    function curIndex() {
      // Return the current index by looking at which section has the class 'current'
      return $sections.index($sections.filter('.current'));
    }
  
    // Previous button is easy, just go back
    $('.form-navigation .previous').click(function() {
      navigateTo(curIndex() - 1);
    });
  
    // Next button goes forward iff current block validates
    $('.form-navigation .next').click(function() {
      $('.demo-form').parsley().whenValidate({
        group: 'block-' + curIndex()
      }).done(function() {
        navigateTo(curIndex() + 1);
      });
    });
  
    // Prepare sections by setting the `data-parsley-group` attribute to 'block-0', 'block-1', etc.
    $sections.each(function(index, section) {
      $(section).find(':input').attr('data-parsley-group', 'block-' + index);
    });
    navigateTo(0); // Start at the beginning
  });

  $(document).ready(function () {
  $("form").submit(function (event) {
    var formData = {
      name: $("#fullname").val(),
      email: $("#email").val(),
      age: $("#age").val(),
      gender: $("#gender").val(),
      martial_status: $("#martial_status").val(),
      race: $("#race").val(),
      occupation: $("#occupation").val(),
      income: $("#income").val(),
      health_insurance: $("#health_insurance").val(),
      personal_savings: $("#personal_savings").val(),  
      living_expenses: $("#living_expenses").val(),  
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
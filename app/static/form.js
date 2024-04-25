$(document).ready(function () {
  $("#ip-form").submit(function (event) {
    var formData = {
      ip_block: $("#ip_block").val(),
    };

    $.ajax({
      type: "POST",
      url: "/api/scan-new",
      data: formData,
      dataType: "json",
      encode: true,
    }).done(function (data) {
      //console.log(data);
      $("#response").html(`<p>${data.message}</p>`);
    });

    event.preventDefault();
  });
});

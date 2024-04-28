$(document).ready(function () {
  $("#ip-form").submit(function (event) {
    var ip = $("#ip_block").val();
    var ports = $("#ports").val();

    var formData = {
      ip_block: ip,
      ports: ports
    };

    $.ajax({
      type: "POST",
      url: "/api/scan-new",
      data: formData,
      dataType: "json",
      encode: true,
    }).done(function (data) {
      $("#response").html(`<p>${data.message}</p>`);
    });

    event.preventDefault();
  });
});

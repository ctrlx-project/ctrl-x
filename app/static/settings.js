const default_command = "-Pn -sS -sV -A -T5 --script=default,discovery,vuln";
const default_dns = "1.1.1.1";
$(document).ready(function () {
  $("#command-form").submit(function (event) {
    var formData = {
      command: $("#command").val(),
      dns: $("#dns").val(),
    };

    $.ajax({
      type: "POST",
      url: "/api/settings",
      data: formData,
      dataType: "json",
      encode: true,
    }).done(function (data) {
      //console.log(data);
      $("#response_settings").html(`<p>${data.message}</p>`);
    });

    event.preventDefault();
  });

  $("#def").on("click", function () {
    console.log("hi")
    $.ajax({
      type: "POST",
      url: "/api/settings",
      data: {
        command: default_command,
        dns: default_dns,
      },
      dataType: "json",
      encode: true,
    }).done(function (data) {
      //console.log(data);
      $("#response_settings").html(`<p>${data.message}</p>`);
    });
  });
});

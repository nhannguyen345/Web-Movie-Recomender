$(document).ready(() => {
  $("#btn-signup").click(function () {
    // Lấy giá trị từ các trường input
    var name = $("#name").val();
    var email = $("#email").val();
    var password = $("#password").val();

    // Kiểm tra trường input trống
    if (!email || !password) {
      alert("Hãy điền các trường trống");
      return;
    }

    // Gửi dữ liệu đến server
    $.ajax({
      type: "POST",
      url: "http://127.0.0.1:5000/check_signup",
      data: {
        name: name,
        email: email,
        password: password,
      },
      success: function (response) {
        // Hiển thị kết quả trả về từ server
        alert("Đăng kí thành công!");
        setTimeout(() => {
          window.location.href = "/login";
        }, 1000);
      },
      error: function (error) {
        console.log("Error:", error);
      },
    });
  });

  $("#showPassword").on("change", function () {
    if ($(this).is(":checked")) {
      $("#password").attr("type", "text");
    } else {
      $("#password").attr("type", "password");
    }
  });
});

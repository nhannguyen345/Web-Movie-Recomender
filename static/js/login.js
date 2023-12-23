$(document).ready(() => {
  $("#btn-login").click(function () {
    // Lấy giá trị từ các trường input
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
      url: "http://127.0.0.1:5000/check_login",
      data: {
        email: email,
        password: password,
      },
      success: function (response) {
        // Hiển thị kết quả trả về từ server
        alert("Đăng nhập thành công!");
        window.localStorage.setItem("id", 611);
        setTimeout(() => {
          window.location.href = "/homepage";
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

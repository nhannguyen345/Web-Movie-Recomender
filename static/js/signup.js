$(document).ready(() => {
  $("#btn-signup").click(function () {
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
      url: "http://127.0.0.1:5000/process_data",
      data: {
        email: email,
        password: password,
      },
      success: function (response) {
        // Hiển thị kết quả trả về từ server
        alert("Đăng nhập thành công!");
      },
      error: function (error) {
        console.log("Error:", error);
      },
    });
  });
});

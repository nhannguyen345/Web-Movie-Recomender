$(document).ready(function () {
  var $searchInput = $("#searchInput");
  var $suggestionsList = $("#suggestionsList");

  $("#searchInput").focus(function () {
    $(this).css("border-radius", "0 0 5px 5px");
    $suggestionsList.css("display", "block");
  });

  $searchInput.on("blur", function () {
    $(this).css("border-radius", "30px");
    // Delay 200ms để kiểm tra xem đã click vào li chưa
    setTimeout(function () {
      if (!$suggestionsList.is(":focus-within")) {
        $suggestionsList.css("display", "none");
      }
    }, 200);
  });

  $searchInput.on("input", async function () {
    $suggestionsList.html("");
    if ($searchInput.val() == "") {
      return;
    }

    var suggestions = await fetch(
      `http://127.0.0.1:5000/search?str=${encodeURIComponent(
        $searchInput.val()
      )}`
    );
    var data = await suggestions.json();

    data.forEach(function (suggestion) {
      var $li = $("<li>")
        .text(suggestion.title)
        .data("movie-id", suggestion.movieId); // Lưu trữ movieId trong data attribute
      $suggestionsList.append($li);

      $li.on("click", function () {
        var movieId = $(this).data("movie-id");
        window.location.href = "/ratingpage?movie_id=" + movieId;
        console.log("Clicked on LI:", $(this).text());
      });
    });
  });
});

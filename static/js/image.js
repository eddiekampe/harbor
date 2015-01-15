/**
 * Work in very much progress
 */

$(document).ready(function() {

    $("#search").on("click", function (e) {

        e.preventDefault();
        var search_term = $("[name=inputName]").val(),
            $result_list = $(".list-group");

        $.post("/images/search", { term: search_term }, function (data, status) {
            console.log(status);
            //console.log(data);
            data = JSON.parse(data);

            for (var i = 0; i < data.length; i++) {
                console.log(data[i].name);
                $result_list.append(
                    $("<a>")
                        .attr("href", "/images/pull")
                        .attr("data-image", data[i].name)
                        .attr("class", "list-group-item")
                        .append(
                            $("<h4>")
                                .attr("class", "list-group-item-heading")
                                .text(data[i].name)
                        )
                        .append(
                            $("<p>")
                                .attr("class", "list-group-item-text")
                                .text(data[i].description)
                        )
                );

                console.log(data[i]);
            }

            $(".list-group-item").on("click", function (e) {

                e.preventDefault();

                var image = $(this).data("image"),
                    url = $(this).attr("href");

                console.log(image);

                $.post(url, { image: image }, function (data, status) {
                    console.log("Download complete");
                });
            });

            // [
            // {"star_count": 0, "is_official": false, "description": "", "is_trusted": false, "name": "sunlitweb/ngnix"},
            // {"star_count": 0, "is_official": false, "description": "", "is_trusted": false, "name": "jhuiting/ngnix"}
            // ]
        });
    })
});
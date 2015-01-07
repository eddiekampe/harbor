/**
 * @fileOverview Contains function, methods and classes for search functionality.
 * @author Eddie Kämpe
 */

/**
 * @namespace Harbor Namespace
 * @this {Harbor}
 */
Harbor = function ($) {
    "use strict";
    return {};
}(jQuery);


/**
 * @namespace Harbor.Image Namespace
 * @this {Harbor.Image}
 * @extends Harbor
 */
Harbor.Image = function ($) {
    "use strict";
    return {};
}(jQuery);


/**
 * @namespace Harbor.Image.Search Namespace
 * @this {Harbor.Image.Search}
 * @extends Harbor.Image
 */
Harbor.Image.Search = function ($) {
    "use strict";

    return {

        settings: {},

        Initialize: function (options) {

            this.settings = $.extend({
                $searchElm: undefined,
                $clearElm: undefined,
                $inputElm: undefined,
                $resultElm: undefined,
                searchUrl: "/images/search",
                pullUrl: "/images/pull"
            }, options);

            // Register event listener
            this.settings.$searchElm.on("click", function (e) {
                e.preventDefault();
                Harbor.Image.Search.OnClick();
            });

            this.settings.$clearElm.on("click", function (e) {
                e.preventDefault();
                Harbor.Image.Search.OnClear();
            })
        },

        /**
         * Handle search button click
         * @constructor
         */
        OnClick: function () {

            $(".loader").show();

            var imageName = this.settings.$inputElm.val(),
                searchUrl = this.settings.searchUrl;

            $.post(searchUrl, { term: imageName }, function (data, status) {

                data = JSON.parse(data);
                Harbor.Image.Search.ListResult(data);
            });
        },

        /**
         * Handle clear result click
         * @constructor
         */
        OnClear: function () {
            this.settings.$resultElm.empty();
        },

        /**
         * Display result in list view
         * @param result Result data
         * @constructor
         */
        ListResult: function (result) {

            $(".loader").hide();
            for (var i = 0; i < result.length; i++) {

                this.settings.$resultElm.append(
                    $("<a>")
                        .attr("href", this.settings.pullUrl)
                        .attr("data-image", result[i].name)
                        .attr("class", "list-group-item")
                        .append(
                            $("<h4>")
                                .attr("class", "list-group-item-heading")
                                .text(result[i].name)
                        )
                        .append(
                            $("<p>")
                                .attr("class", "list-group-item-text")
                                .text(result[i].description)
                        )
                )
            }

            console.log(result);
        },

        Error: function (message) {
            console.log("----------------------------");
            console.log("Harbor.Image.Search: Error");
            console.log(message);
            console.log("----------------------------");
        }
    };

}(jQuery);
odoo.define("website_project_e_service.form", function (require) {
    "use strict"; // Start of use strict

    console.log(123);

    var options = require('web_editor.snippets.options');
    options.registry.s_testimonial_options = options.Class.extend({
        onFocus: function () {
            alert("On focus!")
        },
    });
    var tabs = $(`ul[role="tablist"] li a[role="tab"]`);
    tabs.each((i, tab) => {
        if (i < tabs.length) {
            var current_tab = $(tab);
            var current_tab_content = $(tab.attributes.href.textContent);
            var next_tab = $(tabs[i + 1])
            var next_tab_content = $(tabs[i + 1].attributes.href.textContent);
            var button_to_next_tab = $(`a[href="#${tabs[i + 1].id}"]`);
            if (button_to_next_tab.length == 1) {
                button_to_next_tab.on("click", function () {
                    $(".is-invalid").toggleClass("is-invalid");
                    current_tab_content.find(`*[required]`).each((i, requiredTag) => { // Find required input tags
                        if (requiredTag.type === "checkbox" && requiredTag.checked === false)
                            $(requiredTag).toggleClass("is-invalid");
                        if (requiredTag.type === "text" && requiredTag.value === "")
                            $(requiredTag).toggleClass("is-invalid");
                        if (requiredTag.type === "select-one") {
                            $(requiredTag).find('*[disabled]').each((i, selectTag) => {
                                if (selectTag.value === requiredTag.value)
                                    $(requiredTag).toggleClass("is-invalid");
                            })
                        };
                    });
                    if ($(".is-invalid").length === 0) { // Check if all required tags have values
                        current_tab.toggleClass("active");
                        next_tab.toggleClass("active");
                        current_tab_content.toggleClass("active show");
                        next_tab_content.toggleClass("active show");
                    } else {
                        alert("Fyll i alla fält med stjärnor");
                    };
                });
            } else if (button_to_next_tab.length > 1) {
                console.log("Error, more than one button");
            };
        };
    });
    // $("#top_menu").addClass("justify-content-around align-items-sm-center");
    // $(".navbar").addClass("bl-navbar").attr("style","box-shadow: 0px 0px 10px #333 !important");
    // $(".navbar-brand.logo").addClass("d-block d-md-none").removeAttr("style");
    // $(".navbar-expand-lg").addClass("navbar-expand-md").removeClass("navbar-expand-lg");
    // $(".o_header_standard").removeClass("o_header_standard");
    // $("li.nav-item.dropdown").addClass("d-none");
    // $("#wrapwrap").scroll(function () {
    //     //~ var t = parseInt(getComputedStyle(document.querySelector(":root")).getPropertyValue("--o-we-toolbar-height"))
    //     //~ if (!isNaN(t)) {
    //     //~ }
    //     var scrollTop = $("#wrapwrap").scrollTop()
    //     if (scrollTop > $("#block_logo_div").height()) {
    //         setTimeout(() => { $("#top>nav").css("top", getComputedStyle(document.querySelector(":root")).getPropertyValue("--o-we-toolbar-height")); }, 10);
    //         $("#top>nav").css({"transform": ""});
    //         $("#top_menu").addClass("justify-content-end").removeClass("justify-content-around");
    //         $("#top_menu_container").addClass("col-md-11")
    //         $(".navbar").addClass("bl-navbar-fixed-top").removeClass("bl-navbar").attr("style","box-shadow: 0px 0px 5px #FF4100 !important");
    //         $(".navbar-brand.logo").removeClass("d-md-none");

    //         //~ $("#top_menu_container").removeClass("col-md-12");
    //     } else {
    //         //~ $("#top").css("top",-1);
    //         $("#top>nav").css({"transform": ""});
    //         setTimeout(() => { $("#top>nav").css("top", 0); }, 10);
    //         $("#top_menu").addClass("justify-content-around").removeClass("justify-content-end");
    //         $("#top_menu_container").removeClass("col-md-11")
    //         $(".navbar").addClass("bl-navbar").removeClass("bl-navbar-fixed-top").attr("style","box-shadow: 0px 0px 10px #333 !important");
    //         $(".navbar-brand.logo").addClass("d-md-none");
    //         //~ $("#top_menu_container").addClass("col-md-12");
    //     }
    // });
}); // End of use strict
odoo.define("website_project_e_service.e_service_form", function (require) {
    "use strict"; // Start of use strict

    require('web.dom_ready');
    const ajax = require('web.ajax');

    $('document').ready(function (event) {
        var tabs = $(`ul[role="tablist"] li a[role="tab"]`);
        tabs.each((i, tab) => {
            if (i < tabs.length) {
                var current_tab = $(tab);
                var current_tab_content = $(tab.attributes.href.textContent);
                var next_tab = $(tabs[i + 1])
                if (next_tab.length > 0) {
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
                }
            };
        });

    })
})

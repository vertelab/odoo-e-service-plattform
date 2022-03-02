odoo.define("website_project_e_service.e_service_form", function (require) {
    "use strict"; // Start of use strict

    const core = require("web.core");
    const Dialog = require("web.Dialog");
    const rpc = require("web.rpc");
    const session = require("web.session");
    require("web.dom_ready");
    const _t = core._t;

    function validateInput() {
        $(`[id="s_website_form_result"]`).empty();
        const self = $(this);
        const type = this.type;
        const value = this.value;
        self.removeClass("is-invalid");
        switch (type) {
            case "checkbox": {
                if (!this.checked) self.addClass("is-invalid");
                break;
            }
            case "text": {
                if (!value) self.addClass("is-invalid");
                if (this.pattern) {
                    const re = new RegExp(this.pattern);
                    if (!re.test(value)) { self.addClass("is-invalid"); };
                };
                break;
            }
            case "select-one": {
                self.find(`[disabled]`).each(function (i, selectTag) {
                    if (selectTag.value === value)
                        self.addClass("is-invalid");
                });
                break;
            }
            default:
                console.log("type", type);
                break;
        };
    };

    $("document").ready(function () {
        const snippet = $(`[data-snippet="s_tabs"]`);
        if (snippet.length) {
            snippet.find(`[required]`).on("input", validateInput);
            if (session.user_id != false) {
                rpc.query({
                    model: "res.users",
                    method: "search_read",
                    args: [[["id", "=", session.user_id]], ["city", "email", "name", "partner_id", "social_sec_nr", "street", "zip"],],
                }).then(function (data) {
                    if (data.length) {
                        let userInfo = data[0]
                        for (let key in userInfo) {
                            let val = userInfo[key];
                            if (val) {
                                if (Array.isArray(val)) val = val[0];
                                $(`input[name="${key}"]`).val(val);
                            };
                        };
                    };
                });
            };
            const tabs = $(`ul[role="tablist"] li a[role="tab"]`);
            tabs.each(function (i, tab) {
                if (i < tabs.length) {
                    const currentTab = $(tab);
                    const currentTabContent = $(tab.attributes.href.textContent);
                    const nextTab = $(tabs[i + 1])
                    if (nextTab.length) {
                        const nextTabContent = $(tabs[i + 1].attributes.href.textContent);
                        const nextTabButton = currentTabContent.find(`div[data-name="Next Button"]>a`);
                        if (nextTabButton.length) {
                            nextTabButton.on("click", function () {
                                currentTabContent.find(`[required]`).each(validateInput);
                                if (!currentTabContent.find(`.is-invalid`).length) { // Check if all required tags have values
                                    currentTab.toggleClass("active");
                                    nextTab.toggleClass("active");
                                    currentTabContent.toggleClass("active show");
                                    nextTabContent.toggleClass("active show");
                                } else {
                                    Dialog.alert(this, _t("Please fill in all required fields"));
                                };
                            });
                        };
                    };
                };
            });
            snippet.find('form').each(function() {
                let self = $(this);
                let action = this.action;
                let model_name = self.data('model_name');
                let hidden = self.find(`input[type="hidden"]`);
                let name = hidden[0].name;
                let value = hidden[0].value;
                const unique_key = action + model_name + name + value;
                
                let storage = localStorage.getItem(unique_key);
                if (storage == null) {storage = new Object()}
                else {storage = JSON.parse(storage)}

                for (let field in storage) {
                    snippet.find(`[name="${field}"]`).each(function() {
                        if (this.type === 'checkbox') {
                            this.checked = storage[field];
                        }
                        else if (this.type === 'radio') {
                            if (this.value == storage[field]) {
                                this.checked = true
                            }
                        }
                        else {
                            this.value = storage[field];
                        }

                        $(this).on('input',function() {
                            if (this.type === 'checkbox') {
                                storage[field] = this.checked;
                            }
                            else {
                                storage[field] = this.value;
                            }
                            localStorage.setItem(unique_key,JSON.stringify(storage));
                        });
                    });
                }

                self.find(".s_website_form_input").each(function() {
                    if (this.type === 'checkbox') {
                        storage[this.name] = this.checked;
                    }
                    else {
                        storage[this.name] = this.value;
                    }
                    localStorage.setItem(unique_key,JSON.stringify(storage));
                });
            });
        };
    });
});

odoo.define("website_project_e_service.e_service_form", function (require) {
    "use strict"; // Start of use strict

    const core = require("web.core");
    const Dialog = require("web.Dialog");
    const rpc = require("web.rpc");
    const session = require("web.session");

    require("web.dom_ready");
    const _t = core._t;

    function autofillInput(selector, res_field, datas) {
        for (const data of datas){
            for (let key in data) {
                let val = data[key];
                if (val) {
                    if (Array.isArray(val))
                    val = val[0];
                    $(selector).find(`[data-autofill]`).each(function () {
                        if ($(this).data("autofill") === `${res_field}.${key}`)
                        $(this).val(val);
                    });
                };
            };
        };
    };

    function getAutofillInputs(selector, res_field) {
        let fields = []
        res_field += '.'
        $(selector).find("[data-autofill]").each(function () {
            const data = $(this).data("autofill");
            if (data.startsWith(res_field)) {
                fields.push(data.slice(res_field.length));
            };
        });
        return fields;
    };

    async function getData(args = [], kwargs = {}) {
        return await rpc.query({
            model: "res.partner",
            method: "getHumanRelationData",
            args: args,
            kwargs: kwargs,
        });
    };

    function validateInput() {
        $(`[id="s_website_form_result"]`).empty();
        const self = $(this);
        let checkPattern = validatePattern(this);
        let checkRequired = validateRequired(this);
        if (checkPattern && checkRequired)
            self.removeClass("is-invalid");
        else
            self.addClass("is-invalid");
    };

    function validatePattern(tag) {
        if (tag.pattern && tag.value)
            return new RegExp(tag.pattern).test(tag.value);
        return true;
    };

    function validateRequired(tag) {
        if (tag.required) {
            switch (tag.type) {
                case "checkbox": {
                    return Boolean(tag.checked)
                }
                case "select-one": {
                    let checkSelect = true;
                    $(tag).find(`[disabled]`).each(function () {
                        if (this.value === tag.value)
                            checkSelect = false;
                    });
                    return checkSelect;
                }
                default: {
                    return Boolean(tag.value);
                }
            };
        };
        return true
    };

    $("document").ready(function () {
        $(`[data-snippet="s_tabs"]`).each(function () {
            const elem = this;
            const snippet = $(this);
            snippet.find(".s_website_form_input").on("input", validateInput);
            if (session.user_id != false) {
                const userFields = getAutofillInputs(elem, "user");
                rpc.query({
                    model: "res.users",
                    method: "search_read",
                    args: [[["id", "=", session.user_id]], userFields],
                }).then(function (data) {
                    autofillInput(elem, "user", data);
                    const childFields = getAutofillInputs(elem, "child");
                    getData(childFields, { method: "children" }).then(function (children) {
                        snippet.find(`[data-autofill="children"]`).each(function (i, selectTag) {
                            for (const child of children) {
                                $(selectTag).append(`<option value="${child.name}">${child.name}</option>`);
                            };
                            $(selectTag).on("input", function () {
                                for (const child of children) {
                                    if (child.name === selectTag.value)
                                        autofillInput(elem, "child", [child]);
                                };
                            });
                        });
                    });
                });
            };

            const tabs = snippet.find(`ul[role="tablist"] li a[role="tab"]`);
            tabs.each(function (i) {
                if (i < tabs.length) {
                    const currentTab = $(this);
                    const currentTabContent = $(this.attributes.href.textContent);
                    const nextTab = $(tabs[i + 1])
                    if (nextTab.length) {
                        const nextTabContent = $(tabs[i + 1].attributes.href.textContent);
                        const nextTabButton = currentTabContent
                            .find(`div[data-name="Next Button"]>a`)
                            .on("click", function (event) {
                                event.preventDefault();
                                currentTabContent.find(".s_website_form_input").each(validateInput);
                                if (!currentTabContent.find(`.is-invalid`).length) { // Check if all tags are valid
                                    elem.scrollIntoView({ behavior: "smooth" });
                                    currentTab.toggleClass("active");
                                    nextTab.toggleClass("active");
                                    currentTabContent.toggleClass("active show");
                                    nextTabContent.toggleClass("active show");
                                } else {
                                    Dialog.alert(this, _t("Please fill in all required fields and make sure data is valid"));
                                };
                            });
                    };
                };
            });

            snippet.find('form').each(function () {
                let self = $(this);
                let action = this.action;
                let model_name = self.data('model_name');
                let hidden = self.find(`input[type="hidden"]`);
                let name = hidden[0].name;
                let value = hidden[0].value;
                const unique_key = action + model_name + name + value;

                let storage = localStorage.getItem(unique_key);
                if (storage == null) { storage = new Object() }
                else { storage = JSON.parse(storage) }

                for (let field in storage) {
                    snippet.find(`[name="${field}"]`).each(function () {
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

                        $(this).on("input", function () {
                            if (this.type === 'checkbox') {
                                storage[field] = this.checked;
                            }
                            else {
                                storage[field] = this.value;
                            }
                            console.log("onInput", storage[this.name])
                            localStorage.setItem(unique_key, JSON.stringify(storage));
                        });
                    });
                }

                self.find(".s_website_form_input").each(function () {
                    if (this.type === 'checkbox') {
                        storage[this.name] = this.checked;
                    }
                    else {
                        storage[this.name] = this.value;
                    }
                    localStorage.setItem(unique_key, JSON.stringify(storage));
                });
            });
        });
    });
});

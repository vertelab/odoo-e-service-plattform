odoo.define('website_project_e_service.new_e_service', function (require) {
    'use strict';

    var core = require('web.core');
    var wUtils = require('website.utils');
    var WebsiteNewMenu = require('website.newMenu');

    const {qweb, _t} = core;

    WebsiteNewMenu.include({
        actions: _.extend({}, WebsiteNewMenu.prototype.actions || {}, {
            new_e_service: '_createNewService',
        }),

        //--------------------------------------------------------------------------
        // Actions
        //--------------------------------------------------------------------------

        /**
         * Asks the user information about a new e-service, then creates
         * it and redirects the e-service page.
         *
         * @private
         * @returns {Promise} Unresolved if there is a redirection
         */
        _createNewService: function () {
            var self = this;

            return self._rpc({
                model: 'e_service.category',
                method: 'search_read',
                args: [[], ['name']],
            }).then(function (project_services) {
                return wUtils.prompt({
                    id: 'editor_new_blog',
                    window_title: _t("New E-Service"),
                    select: _t("Select Service"),
                    init: function (field) {
                        var $group = this.$dialog.find('div.form-group');
                        $group.removeClass('mb0');
                        var $add = $(
                            '<div/>', {'class': 'form-group row'}
                        ).append(
                            $('' +
                                '<label class="col-md-3 col-form-label">Project Name:</label>' +
                                '<div class="col-sm-9">' +
                                    '<input class="form-control" type="text" id="project_name" required="1"/>' +
                                '</div>' +
                                '<label class="col-md-12 col-form-label" style="text-align: center; color: red">All fields are required !</label>'
                            )
                        );
                        $group.after($add);

                        return _.map(project_services, function (project_service) {
                            return [project_service['id'], project_service['name']];
                        });
                    },
                }).then(function (result) {
                    var $dialog = result.dialog;
                    var project_name = $dialog.find('input[type="text"]')[0].value

                    var e_service_id = result.val;
                    if (!e_service_id) {
                        return;
                    }
                    self._createProject(project_name, e_service_id)
                    return new Promise(function () {});
                });
            });
        },

        _createProject: function (project_name, e_service_id) {
            return this._rpc({
                model: 'project.project',
                method: 'create_project_portal',
                args: [{
                    project_name: project_name,
                    e_service_id: e_service_id,
                }],
            }).then(function (response) {
                if (response.errors) {
                    alert(response.errors)
                    document.location = '/e-services'
                } else {
                    document.location = '/e-service/' + response.id;
                }
            });
        },
    });
});


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
         * Asks the user information about a new blog post to create, then creates
         * it and redirects the user to this new post.
         *
         * @private
         * @returns {Promise} Unresolved if there is a redirection
         */
        _createNewService: function () {
            return this._rpc({
                model: 'project.project',
                method: 'search_read',
                args: [[], ['name']],
            }).then(function (projects) {
                if (projects.length === 1) {
                    document.location = '/e-service/' + projects[0]['id'] + '/post/new';
                    return new Promise(function () {});
                } else if (projects.length > 1) {
                    return wUtils.prompt({
                        id: 'editor_new_blog',
                        window_title: _t("New E-Service"),
                        select: _t("Select Project"),
                        init: function (field) {
                            var $group = this.$dialog.find('div.form-group');
                            $group.removeClass('mb0');
                            var $add = $(
                                '<div/>', {'class': 'form-group row'}
                            ).append(
                                $('' +
                                    '<label class="col-md-3 col-form-label">E-Service Name:</label>' +
                                    '<div class="col-sm-9">' +
                                        '<input class="form-control" type="text" id="e_service_name"/>' +
                                    '</div>'
                                )
                            );
                            $group.after($add);

                            return _.map(projects, function (project) {
                                return [project['id'], project['name']];
                            });


                        },
                    }).then(function (result) {
                        var $dialog = result.dialog;
                        var e_service_name = $dialog.find('input[type="text"]')[0].value

                        var e_service_id = result.val;
                        if (!e_service_id) {
                            return;
                        }
                        document.location = '/e-service/' + e_service_id;
                        return new Promise(function () {});
                    });
                }
            });
        },
    });
});


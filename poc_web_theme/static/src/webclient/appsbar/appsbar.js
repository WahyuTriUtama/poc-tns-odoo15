/** @odoo-module **/

import { useService } from "@web/core/utils/hooks";

const { Component, hooks } = owl;

export class AppsBar extends Component {}

Object.assign(AppsBar, {
  template: "poc_web_theme.AppsBar",
  props: {
    apps: Array,
  },
});

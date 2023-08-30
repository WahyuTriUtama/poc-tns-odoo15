/** @odoo-module */

import { session } from "@web/session";
import { url } from "@web/core/utils/urls";
import { patch } from "@web/core/utils/patch";
import { registry } from "@web/core/registry";

import { NavBar } from "@web/webclient/navbar/navbar";
import { AppsMenu } from "@poc_web_theme/webclient/appsmenu/appsmenu";
import { AppsBar } from "@poc_web_theme/webclient/appsbar/appsbar";
import { SwitchCompanyMenu } from "@web/webclient/switch_company_menu/switch_company_menu";
import { UserMenu } from "@web/webclient/user_menu/user_menu";

patch(NavBar.prototype, "poc_web_theme.NavBar", {
  setup() {
    this._super();
    this.backgroundBlendMode = session.theme_background_blend_mode;
  },
});

patch(NavBar, "poc_web_theme.NavBar", {
  components: {
    ...NavBar.components,
    AppsMenu,
    AppsBar,
  },
});

const systrayItemUserMenu = {
  Component: UserMenu,
};

const systrayItemSwitchCompanyMenu = {
  Component: SwitchCompanyMenu,
  isDisplayed(env) {
    const { availableCompanies } = env.services.company;
    return Object.keys(availableCompanies).length > 1;
  },
};

registry.category("systray").add("web.user_menu", systrayItemUserMenu, {
  force: true,
  sequence: 1,
});
registry
  .category("systray")
  .add("SwitchCompanyMenu", systrayItemSwitchCompanyMenu, {
    force: true,
    sequence: 2,
  });

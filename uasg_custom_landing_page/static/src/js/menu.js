
/** @odoo-module **/
import { registry } from "@web/core/registry";
import { preferencesItem } from "@web/webclient/user_menu/user_menu_items";
import { routeToUrl } from "@web/core/browser/router_service";
import { browser } from "@web/core/browser/browser";
const userMenuRegistry = registry.category("user_menuitems");
const { patch } = require('web.utils');


userMenuRegistry.remove("support");
userMenuRegistry.remove("documentation");
userMenuRegistry.remove("odoo_account");
userMenuRegistry.remove("shortcuts");
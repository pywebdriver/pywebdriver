/*!
 * Gettext.js - GNU gettext port for JavaScript
 * Lightweight implementation for browser
 * Based on https://github.com/guillaumepotier/gettext.js
 */

(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        define([], factory);
    } else if (typeof module === 'object' && module.exports) {
        module.exports = factory();
    } else {
        root.Gettext = factory();
    }
}(typeof self !== 'undefined' ? self : this, function () {
    'use strict';

    function Gettext(options) {
        options = options || {};
        this.domain = options.domain || 'messages';
        this.locale = options.locale || 'en';
        this.locale_data = options.locale_data || {};
    }

    Gettext.prototype.dcnpgettext = function (domain, context, msgid, msgid_plural, count) {
        domain = domain || this.domain;
        var key = context ? context + '\u0004' + msgid : msgid;
        var translation = this.locale_data[domain] && this.locale_data[domain][key];

        if (!translation) {
            return msgid;
        }

        if (typeof translation === 'string') {
            return translation;
        }

        // Plural handling
        var index = this.plural_func(this.locale, count);
        if (translation[index]) {
            return translation[index];
        }

        return msgid;
    };

    Gettext.prototype.dnpgettext = function (domain, context, msgid, msgid_plural, count) {
        return this.dcnpgettext(domain, context, msgid, msgid_plural, count);
    };

    Gettext.prototype.dngettext = function (domain, msgid, msgid_plural, count) {
        return this.dcnpgettext(domain, null, msgid, msgid_plural, count);
    };

    Gettext.prototype.dgettext = function (domain, msgid) {
        return this.dcnpgettext(domain, null, msgid, null, 1);
    };

    Gettext.prototype.npgettext = function (context, msgid, msgid_plural, count) {
        return this.dcnpgettext(null, context, msgid, msgid_plural, count);
    };

    Gettext.prototype.ngettext = function (msgid, msgid_plural, count) {
        return this.dcnpgettext(null, null, msgid, msgid_plural, count);
    };

    Gettext.prototype.pgettext = function (context, msgid) {
        return this.dcnpgettext(null, context, msgid, null, 1);
    };

    Gettext.prototype.gettext = function (msgid) {
        return this.dcnpgettext(null, null, msgid, null, 1);
    };

    Gettext.prototype.plural_func = function (locale, count) {
        // Simple plural rules for common languages
        var plural_forms = {
            'en': function (n) { return n != 1 ? 1 : 0; },
            'es': function (n) { return n != 1 ? 1 : 0; },
            'fr': function (n) { return n > 1 ? 1 : 0; },
            'de': function (n) { return n != 1 ? 1 : 0; },
            'pt': function (n) { return n != 1 ? 1 : 0; },
        };

        var func = plural_forms[locale] || plural_forms['en'];
        return func(count);
    };

    return Gettext;
}));

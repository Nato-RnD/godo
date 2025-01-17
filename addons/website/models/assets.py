# -*- coding: utf-8 -*-
# Part of Godo. See LICENSE file for full copyright and licensing details.

import re

from odoo import models


class Assets(models.AbstractModel):
    _inherit = 'web_editor.assets'

    def make_scss_customization(self, url, values):
        """
        Makes a scss customization of the given file. That file must
        contain a scss map including a line comment containing the word 'hook',
        to indicate the location where to write the new key,value pairs.

        Params:
            url (str):
                the URL of the scss file to customize (supposed to be a variable
                file which will appear in the assets_common bundle)

            values (dict):
                key,value mapping to integrate in the file's map (containing the
                word hook). If a key is already in the file's map, its value is
                overridden.
        """
        if 'color-palettes-name' in values:
            self.reset_asset('/website/static/src/scss/options/colors/user_color_palette.scss', 'web.assets_common')
            self.reset_asset('/website/static/src/scss/options/colors/user_gray_color_palette.scss', 'web.assets_common')
            # Do not reset all theme colors for compatibility (not removing alpha -> epsilon colors)
            self.make_scss_customization('/website/static/src/scss/options/colors/user_theme_color_palette.scss', {
                'success': 'null',
                'info': 'null',
                'warning': 'null',
                'danger': 'null',
            })
            # Also reset gradients which are in the "website" values palette
            self.make_scss_customization('/website/static/src/scss/options/user_values.scss', {
                'menu-gradient': 'null',
                'header-boxed-gradient': 'null',
                'footer-gradient': 'null',
                'copyright-gradient': 'null',
            })

        custom_url = self.make_custom_asset_file_url(url, 'web.assets_common')
        updatedFileContent = self.get_asset_content(custom_url) or self.get_asset_content(url)
        updatedFileContent = updatedFileContent.decode('utf-8')
        for name, value in values.items():
            pattern = "'%s': %%s,\n" % name
            regex = re.compile(pattern % ".+")
            replacement = pattern % value
            if regex.search(updatedFileContent):
                updatedFileContent = re.sub(regex, replacement, updatedFileContent)
            else:
                updatedFileContent = re.sub(r'( *)(.*hook.*)', r'\1%s\1\2' % replacement, updatedFileContent)

        # Bundle is 'assets_common' as this route is only meant to update
        # variables scss files
        self.save_asset(url, 'web.assets_common', updatedFileContent, 'scss')

    def _get_custom_attachment(self, custom_url, op='='):
        """
        See web_editor.Assets._get_custom_attachment
        Extend to only return the attachments related to the current website.
        """
        if self.env.user.has_group('website.group_website_designer'):
            self = self.sudo()
        website = self.env['website'].get_current_website()
        res = super(Assets, self)._get_custom_attachment(custom_url, op=op)
        return res.with_context(website_id=website.id).filtered(lambda x: not x.website_id or x.website_id == website)

    def _get_custom_asset(self, custom_url):
        """
        See web_editor.Assets._get_custom_asset
        Extend to only return the views related to the current website.
        """
        if self.env.user.has_group('website.group_website_designer'):
            # TODO: Remove me in master, see commit message, ACL added right to
            #       unlink to designer but not working without -u in stable
            self = self.sudo()
        website = self.env['website'].get_current_website()
        res = super(Assets, self)._get_custom_asset(custom_url)
        return res.with_context(website_id=website.id).filter_duplicate()

    def _save_asset_hook(self):
        """
        See web_editor.Assets._save_asset_hook
        Extend to add website ID at attachment creation.
        """
        res = super(Assets, self)._save_asset_hook()

        website = self.env['website'].get_current_website()
        if website:
            res['website_id'] = website.id
        return res

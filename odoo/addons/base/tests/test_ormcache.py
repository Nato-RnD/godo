# -*- coding: utf-8 -*-
# Part of Godo. See LICENSE file for full copyright and licensing details.

from odoo.tests.common import TransactionCase
from odoo.tools import get_cache_key_counter


class TestOrmcache(TransactionCase):
    def test_ormcache(self):
        """ Test the effectiveness of the ormcache() decorator. """
        IMD = self.env['ir.model.data']
        XMLID = 'base.group_no_one'

        # retrieve the cache, its key and stat counter
        cache, key, counter = get_cache_key_counter(IMD._xmlid_lookup, XMLID)
        hit = counter.hit
        miss = counter.miss

        # clear the caches of ir.model.data, retrieve its key and
        IMD.clear_caches()
        self.assertNotIn(key, cache)

        # lookup some reference
        self.env.ref(XMLID)
        self.assertEqual(counter.hit, hit)
        self.assertEqual(counter.miss, miss + 1)
        self.assertIn(key, cache)

        # lookup again
        self.env.ref(XMLID)
        self.assertEqual(counter.hit, hit + 1)
        self.assertEqual(counter.miss, miss + 1)
        self.assertIn(key, cache)

        # lookup again
        self.env.ref(XMLID)
        self.assertEqual(counter.hit, hit + 2)
        self.assertEqual(counter.miss, miss + 1)
        self.assertIn(key, cache)

# ----------------------------------------------------------------------------
# Copyright (c) 2017-, labman development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from unittest import main

from tornado.escape import json_decode, json_encode

from labman.gui.testing import TestHandlerBase


class TestPoolingProcessHandlers(TestHandlerBase):
    def test_get_pool_pool_process_handler(self):
        response = self.get('/process/poolpools')
        self.assertEqual(response.code, 200)
        self.assertNotEqual(response.body, '')

        response = self.get('/process/poolpools?pool_id=1')
        self.assertEqual(response.code, 200)
        self.assertNotEqual(response.body, '')

    def test_post_pool_pool_process_handler(self):
        data = {'pool_name': 'Test pool pool',
                'pools_info': json_encode([
                    {'pool_id': 1, 'concentration': 2.2,
                     'volume': 5, 'percentage': 100}])}
        response = self.post('/process/poolpools', data)
        self.assertEqual(response.code, 200)
        self.assertCountEqual(json_decode(response.body), ['process'])

    def test_get_library_pool_process_handler(self):
        response = self.get('/process/poollibraries')
        self.assertEqual(response.code, 200)
        self.assertNotEqual(response.body, '')

    def test_post_library_pool_process_handler(self):
        data = {'plates-info': json_encode([{
            'plate-id': 23, 'pool-func': 'amplicon', 'dna-amount-23': 240,
            'min-val-23': 1, 'max-val-23': 15, 'blank-val-23': 2,
            'epmotion-23': 10, 'dest-tube-23': 1}])}
        response = self.post('/process/poollibraries', data)
        self.assertEqual(response.code, 200)
        obs = json_decode(response.body)
        self.assertEqual(len(obs), 1)
        self.assertCountEqual(obs[0], ['plate-id', 'process-id'])

    def test_post_compute_library_pool_values_handler(self):
        data = {'plate-info': json_encode({
            'plate-id': 23, 'pool-func': 'amplicon', 'dna-amount-23': 240,
            'min-val-23': 1, 'max-val-23': 15, 'blank-val-23': 2,
            'epmotion-23': 10, 'dest-tube-23': 1})}
        response = self.post('/process/compute_pool', data)
        self.assertEqual(response.code, 200)
        self.assertCountEqual(json_decode(response.body),
                              ['plate_id', 'pool_vals'])

    def test_get_download_pool_file_handler(self):
        response = self.get("/process/poollibraries/1/pool_file")
        self.assertNotEqual(response.body, '')
        self.assertTrue(response.body.startswith(
            b'Rack,Source,Rack,Destination,Volume,Tool'))

        response = self.get("/process/poollibraries/3/pool_file")
        self.assertNotEqual(response.body, '')
        self.assertTrue(response.body.startswith(
            b'Source Plate Name,Source Plate Type,Source Well,Concentration,'))


if __name__ == '__main__':
    main()

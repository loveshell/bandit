#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright 2014 Hewlett-Packard Development Company, L.P.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import argparse
from bandit import manager as b_manager

default_test_config = 'bandit.yaml'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Bandit - a Python source code analyzer.'
    )
    parser.add_argument(
        'files', metavar='file', type=str, nargs='+',
        help='source file/s to be tested'
    )
    parser.add_argument(
        '-a', '--aggregate', dest='agg_type',
        action='store', default='file', type=str,
        help='group results by (vuln)erability type or (file) it occurs in'
    )
    parser.add_argument(
        '-n', '--number', dest='context_lines',
        action='store', default=0, type=int,
        help='number of context lines to print'
    )
    parser.add_argument(
        '-c', '--configfile', dest='config_file',
        action='store', default=default_test_config, type=str,
        help='test config file (default: %s)' % (
            default_test_config
        )
    )
    parser.add_argument(
        '-p', '--profile', dest='profile',
        action='store', default=None, type=str,
        help='test set profile in config to use (defaults to all tests)'
    )
    parser.add_argument(
        '-l', '--level', dest='level', action='count',
        default=1, help='results level filter'
    )
    parser.add_argument(
        '-o', '--output', dest='output_file', action='store',
        default=None, help='write report to filename'
    )
    parser.add_argument(
        '-d', '--debug', dest='debug', action='store_true',
        help='turn on debug mode'
    )
    parser.set_defaults(debug=False)

    args = parser.parse_args()

    b_mgr = b_manager.BanditManager(args.config_file, args.agg_type,
                                    args.debug, profile_name=args.profile)
    b_mgr.run_scope(args.files)
    if args.debug:
        b_mgr.output_metaast()
    b_mgr.output_results(args.context_lines, args.level - 1, args.output_file)

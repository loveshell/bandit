# -*- coding:utf-8 -*-
#
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


import bandit
from bandit.test_selector import *


@takes_config
@checks_imports
def blacklist_imports(context, config):
    if config is not None and 'bad_import_sets' in config:
        sets = config['bad_import_sets']
    else:
        sets = []

    checks = []

    # load all the checks from the config file
    for cur_item in sets:
        for blacklist_item in cur_item:
            blacklist_object = cur_item[blacklist_item]
            cur_check = _get_tuple_for_item(blacklist_object)
            # skip bogus checks
            if cur_check:
                checks.append(cur_check)

    # for each check, go through and see if it matches all qualifications
    for check in checks:
        does_match = True
        # item 0=import, 1=message, 2=level
        if check[0]:
            for im in check[0]:
                if context.is_module_being_imported(im):
                    # substitute '{module}' for the imported module name
                    message = check[1].replace('{module}', im)

                    level = None
                    if check[2] == 'ERROR':
                        level = bandit.ERROR
                    elif check[2] == 'WARN':
                        level = bandit.WARN
                    elif check[2] == 'INFO':
                        level = bandit.INFO

                    return level, "%s" % message


def _get_tuple_for_item(blacklist_object):
    # default values
    imports = None
    message = ""
    level = 'WARN'

    # if the item we got passed isn't a dictionary, do nothing with the object;
    # if the item we got passed doesn't have an import field, or the import
    # isn't a string, we can't do anything with this.  Return None
    if(not isinstance(blacklist_object, dict)
            or 'import' not in blacklist_object
            or not type(blacklist_object['import']) == str):
        return None

    import_list = blacklist_object['import'].split(',')
    for i in import_list:
        if not imports:
            imports = []
        imports.append(i.replace(' ', '').strip())

    if 'message' in blacklist_object:
        message = blacklist_object['message']

    if 'level' in blacklist_object:
        if blacklist_object['level'] == 'ERROR':
            level = 'ERROR'
        elif blacklist_object['level'] == 'WARN':
            level = 'WARN'
        elif blacklist_object['level'] == 'INFO':
            level = 'INFO'
    return_tuple = (imports, message, level)
    return return_tuple

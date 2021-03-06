# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 Mirantis, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

'''
Main purpose of following attribute is
to supply general information about test set.
This information will be stored in ostf database
in test_sets table.
'''
__profile__ = {
    "id": "platform_tests",
    "driver": "nose",
    "test_path": "fuel_health/tests/platform_tests",
    "description": ("Platform services functional tests."
                    " Duration 3 min - 60 min"),
    "deployment_tags": ['additional_components']
}

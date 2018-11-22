#!/usr/bin/env python3

# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding:utf-8 -*-
#
# Copyright 2014 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import argparse
import os
import subprocess
import sys
from shutil import which


def _init_extensions():
    from bandit.core import extension_loader as ext_loader
    return ext_loader.MANAGER


def find_executable(file_name, additional_paths=None):
    path = None
    if additional_paths:
        path = os.getenv('PATH', os.defpath)
        path += os.path.pathsep + os.path.pathsep.join(additional_paths)
    return which(file_name, path=path)


def main(argv=sys.argv[1:]):
    config_file = os.path.join(
        os.path.dirname(__file__), 'configuration', 'bandit.yaml')
    # bring our logging stuff up as early as possible
    extension_mgr = _init_extensions()

    baseline_formatters = [f.name for f in filter(lambda x:
                                                  hasattr(x.plugin,
                                                          '_accepts_baseline'),
                                                  extension_mgr.formatters)]

    # now do normal startup
    parser = argparse.ArgumentParser(
        description='Bandit - a Python source code security analyzer',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'targets', metavar='targets', type=str, nargs='*', default=[os.curdir],
        help='source file(s) or directory(s) to be tested'
    )
    parser.add_argument(
        '-r', '--recursive', dest='recursive', default=True,
        action='store_true', help='find and process files in subdirectories'
    )
    parser.add_argument(
        '-c', '--configfile', dest='config_file',
        action='store', default=None, type=str,
        help='optional config file to use for selecting plugins and '
             'overriding defaults'
    )
    output_format = 'screen' if sys.stdout.isatty() else 'txt'
    parser.add_argument(
        '-f', '--format', dest='output_format', action='store',
        default=output_format, help='specify output format',
        choices=sorted(extension_mgr.formatter_names)
    )
    args = parser.parse_args(argv)
    print(args)
    exec_bandit = find_executable('bandit')
    print(config_file)
    base_cmd = [exec_bandit,
                '.', '-c', '%s' % config_file, '-r']
    print(base_cmd)
    try:
        p = subprocess.Popen(base_cmd, stderr=subprocess.PIPE)
        xml = p.communicate()[1]
    except subprocess.CalledProcessError as e:
        print("The invocation of 'bandit' failed with error code %d: %s" %
              (e.returncode, e), file=sys.stderr)
        return 1
    print(xml)


if __name__ == '__main__':
    sys.exit(main())

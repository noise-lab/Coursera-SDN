#!/usr/bin/env python

# Copyright 2013-present Barefoot Networks, Inc. 
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import os
from subprocess import Popen

root_dir = os.path.dirname(os.path.realpath(__file__))
pd_dir = os.path.join(root_dir, 'of-tests/pd_thrift')

oft_path = os.path.join(root_dir, '..', '..', 'submodules', 'oft-infra', 'oft')

if __name__ == "__main__":
    args = sys.argv[1:]
    args += ["--pd-thrift-path", pd_dir]
    args += ["--enable-erspan", "--enable-vxlan", "--enable-geneve"]
    child = Popen([oft_path] + args)
    child.wait()
    sys.exit(child.returncode)

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

import oftest.dataplane as dataplane
import oftest.pd_base_tests as pd_base_tests

from oftest.testutils import *

from utils import *

from p4_pd_rpc.ttypes import *
from res_pd_rpc.ttypes import *

class EchoTest(pd_base_tests.ThriftInterfaceDataPlane):
    def __init__(self):
        pd_base_tests.ThriftInterfaceDataPlane.__init__(self, "simple_router_acl")

    def runTest(self):
        sess_hdl = self.conn_mgr.client_init(16)
        dev_tgt = DevTarget_t(0, hex_to_i16(0xFFFF))
        
        self.conn_mgr.echo("TEST !!!")

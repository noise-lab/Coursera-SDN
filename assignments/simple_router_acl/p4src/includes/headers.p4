/*
Copyright 2013-present Barefoot Networks, Inc. 

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

/*
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment: Simple Router with ACL
Professor: Nick Feamster
Author: Muhammad Shahbaz
*/

header_type ethernet_t {
    fields {
        dstAddr : 48;
        srcAddr : 48;
        etherType : 16;
    }
}

header_type ipv4_t {
    fields {
        version : 4;
        ihl : 4;
        diffserv : 8;
        totalLen : 16;
        identification : 16;
        flags : 3;
        fragOffset : 13;
        ttl : 8;
        protocol : 8;
        hdrChecksum : 16;
        srcAddr : 32;
        dstAddr: 32;
    }
}


/* Add your logic here ... */
// -begin-

// You should declare a tcp header type here ...
// Note: Name the header `tcp_t` and fields: `srcPort`, `dstPort`, `seqNo`, `ackNo`, `dataOffset`, `res`, `flags`, `window`,
//                                           `checksum`, and `urgentPtr`


// -end-

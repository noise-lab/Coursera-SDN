# ################################################################################
# ##
# ##  https://github.com/NetASM/NetASM-python
# ##
# ##  File:
# ##        learning_switch.py
# ##
# ##  Project:
# ##        NetASM: A Network Assembly Language for Programmable Dataplanes
# ##
# ##  Author:
# ##        Muhammad Shahbaz
# ##
# ##  Copyright notice:
# ##        Copyright (C) 2014 Princeton University
# ##      Network Operations and Internet Security Lab
# ##
# ##  Licence:
# ##        This file is a part of the NetASM development base package.
# ##
# ##        This file is free code: you can redistribute it and/or modify it under
# ##        the terms of the GNU Lesser General Public License version 2.1 as
# ##        published by the Free Software Foundation.
# ##
# ##        This package is distributed in the hope that it will be useful, but
# ##        WITHOUT ANY WARRANTY; without even the implied warranty of
# ##        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# ##        Lesser General Public License for more details.
# ##
# ##        You should have received a copy of the GNU Lesser General Public
# ##        License along with the NetASM source package.  If not, see
# ##        http://www.gnu.org/licenses/.

__author__ = 'shahbaz'

# Coursera:
# - Software Defined Networking (SDN) course
# -- Programming Assignment: Simple Router with ACL
# Professor: Nick Feamster
# Author: Muhammad Shahbaz

from netasm.netasm.core import *


def main():
    # Constants
    PORT_COUNT_BITMAP = 0xFFFF  # means [... bit(1): port_2, bit(0): port_1]
    ETH_IP_TYPE = 0x0800

    # Declarations
    decls = Decls(TableDecls())

    # Tables
    # Ethernet address table
    MAC_TABLE_SIZE = Size(16)
    decls.table_decls[TableId('eth_match_table')] = \
        Table(TableFieldsCollection.MatchFields(),
            MAC_TABLE_SIZE,
            TableTypeCollection.CAM)
    match_table = decls.table_decls[TableId('eth_match_table')]
    match_table.table_fields[Field('eth_addr')] = Size(48), MatchTypeCollection.Binary

    decls.table_decls[TableId('eth_params_table')] = \
        Table(TableFieldsCollection.SimpleFields(),
            MAC_TABLE_SIZE,
            TableTypeCollection.RAM)
    params_table = decls.table_decls[TableId('eth_params_table')]
    params_table.table_fields[Field('outport_bitmap')] = Size(3)

    # Index address table
    INDEX_TABLE_SIZE = Size(1)
    decls.table_decls[TableId('index_table')] = \
        Table(TableFieldsCollection.SimpleFields(),
            INDEX_TABLE_SIZE,
            TableTypeCollection.RAM)
    index_table = decls.table_decls[TableId('index_table')]
    index_table.table_fields[Field('index')] = Size(16)

    # Add your logic here ...
    # -begin-

    # Implement the following:
    # 1. Create a new acl match table and add it in the table_decls (see above for examples)
    #    a. Table should have match field types as we will be doing an exact match on ip src and dst
    #       (see eth_match_table)
    #    b. Should be of size 16
    #    c. Should be of type CAM
    #
    # 2. Add two fields in the table for ip src and dst
    #    a. Should be of size 32 (i.e., ip field size)
    #    b. Should have a binary match type

    # -end-

    # Code
    code = I.Code(
        ##################
        ### Arguments ####
        ##################
        Fields(),

        ##################
        ## Instructions ##
        ##################
        I.Instructions(
            ##################
            ## Parse packet ##
            ##################

            # Add ethernet header fields in the header set
            I.ADD(O.Field(Field('eth_dst')),
                  Size(48)),
            I.ADD(O.Field(Field('eth_src')),
                  Size(48)),
            I.ADD(O.Field(Field('eth_type')),
                  Size(16)),

            # Add you logic here ...
            # -begin-

            # Implement the following:
            # 1. Add a 1-bit field say has_ip to check if the packet was an ip packet or not
            # 2. Add ip header fields (not the size is specified in bits)

            # -end-

            # Load fields with default values
            I.LD(O.Field(Field('eth_dst')),
                 O.Value(Value(0, Size(48)))),
            I.LD(O.Field(Field('eth_src')),
                 O.Value(Value(0, Size(48)))),
            I.LD(O.Field(Field('eth_type')),
                 O.Value(Value(0, Size(16)))),

            # Add your logic here ...
            # -begin-

            # Load ip header fields with default value of 0

            # -end

            # Parse ethernet
            # load ethernet header fields from the packet
            I.LD(O.Field(Field('eth_dst')),
                 O.Location(
                     Location(
                         O.Value(Value(0, Size(16)))))),
            I.LD(O.Field(Field('eth_src')),
                 O.Location(
                     Location(
                         O.Value(Value(48, Size(16)))))),
            I.LD(O.Field(Field('eth_type')),
                 O.Location(
                     Location(
                         O.Value(Value(96, Size(16)))))),

            # Add your logic here ...
            # -begin-

            # Implement the following:
            # 1. Check if the incoming packet is ip (use BR instruction for this purpose)
            #    a. if not ip, load has_ip with value 0 and jump to l2 learning
            #    b. else if is ip, load has_ip with value 1 and load the ip field values from the packet

            # -end-

            #################
            ## L2 Learning ##
            #################

            I.LBL(Label('LBL_L2')),

            I.ATM(
                I.Code(
                    Fields(Field('eth_dst'), Field('eth_src')),
                    I.Instructions(
                        # Add the following header fields in the header set
                        I.ADD(O.Field(Field('index')),
                              Size(16)),

                        # Lookup in the match table and store the matched index
                        I.LKt(O.Field(Field('index')),
                              TableId('eth_match_table'),
                              O.Operands_(
                                  O.Field(Field('eth_dst')))),
                        I.BR(O.Field(Field('index')),
                             Op.Neq,
                             O.Value(Value(-1, Size(16))),
                             Label('LBL_LKP_0')),

                        # Case: there is no match in the match table
                        # Broadcast the packet
                        I.OP(
                            O.Field(Field('outport_bitmap')),
                            O.Field(Field('inport_bitmap')),
                            Op.Xor,
                            O.Value(Value(PORT_COUNT_BITMAP, Size(16))),
                        ),
                        I.JMP(Label('LBL_LRN')),

                        # Case: there is a match in the l2 match table
                        I.LBL(Label('LBL_LKP_0')),

                        # Load output port from the parameters table
                        I.LDt(
                            O.Operands__(
                                O.Field(Field('outport_bitmap'))),
                            TableId('eth_params_table'),
                            O.Field(Field('index'))),

                        #######################
                        ## Learn MAC address ##
                        #######################
                        I.LBL(Label('LBL_LRN')),

                        # Lookup in the match table and store the matched index
                        I.LKt(O.Field(Field('index')),
                              TableId('eth_match_table'),
                              O.Operands_(
                                  O.Field(Field('eth_src')))),
                        I.BR(O.Field(Field('index')),
                             Op.Neq,
                             O.Value(Value(-1, Size(16))),
                             Label('LBL_LRN_0')),

                        # Case: there is no match in the match table
                        # Read the running index from the index table
                        I.LDt(
                            O.Operands__(
                                O.Field(Field('index'))),
                            TableId('index_table'),
                            O.Value(Value(0, Size(1)))),

                        # Store eth_src in the eth_match_table
                        I.STt(TableId('eth_match_table'),
                              O.Field(Field('index')),
                              O.OperandsMasks_(
                                  (O.Field(Field('eth_src')), Mask(0xFFFFFFFFFFFF)))),

                        # Store inport_bitmap in the eth_params_table
                        I.STt(TableId('eth_params_table'),
                              O.Field(Field('index')),
                              O.Operands_(
                                  O.Field(Field('inport_bitmap')))),

                        # Increment the running index
                        I.OP(
                            O.Field(Field('index')),
                            O.Field(Field('index')),
                            Op.Add,
                            O.Value(Value(1, Size(16))),
                        ),

                        # Check if the index is less than the MAC_TABLE_SIZE
                        I.BR(O.Field(Field('index')),
                             Op.Lt,
                             O.Value(Value(MAC_TABLE_SIZE, Size(16))),
                             Label('LBL_LRN_1')),

                        # Reset the running index
                        I.LD(O.Field(Field('index')),
                             O.Value(Value(0, Size(16)))),

                        # Store the running index back in the table
                        I.LBL(Label('LBL_LRN_1')),

                        I.STt(TableId('index_table'),
                              O.Value(Value(0, Size(1))),
                              O.Operands_(
                                  O.Field(Field('index')))),
                        I.JMP(Label('LBL_HLT')),

                        # Store the current inport_bitmap in the eth_params_table
                        I.LBL(Label('LBL_LRN_0')),

                        I.STt(TableId('eth_params_table'),
                              O.Field(Field('index')),
                              O.Operands_(
                                  O.Field(Field('inport_bitmap')))),

                        # Halt
                        I.LBL(Label('LBL_HLT')),
                        I.HLT()
                    )
                )
            ),

            #########
            ## ACL ##
            #########

            I.LBL(Label('LBL_ACL')),

            # Add your logic here ...
            # -begin-

            # Implement the following:
            # 1. Check if the packet is ip using has_ip field
            #    a. if not ip, jump to the HLT instruction
            #    b. else if is ip, lookup in the acl match table (see eth_match_table lookup example above)
            #       1. if no match, drop the packet (you can use the DRP instruction here, but remember to jump to the
            #          HLT instruction)
            #       2. else pass through (you can use the ID instruction for this)

            # -end-

            ##########
            ## Halt ##
            ##########
            I.LBL(Label('LBL_HLT')),
            I.HLT()
        )
    )

    return Policy(decls, code)

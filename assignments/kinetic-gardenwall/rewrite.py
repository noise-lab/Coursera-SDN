import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import EthAddr
from pox.lib.addresses import IPAddr
import pox.lib.packet as pkt

def build_clear_rule(flow):
    msg = of.ofp_flow_mod()
    msg.command = of.ofp_flow_mod_command_rev_map['OFPFC_DELETE']
    msg.priority = 42
  
    return msg

def build_rewrite_rule(flow):
    msg = of.ofp_flow_mod()
    msg.priority = 42
    msg.match.dl_type = pkt.ethernet.IP_TYPE

    srcmac_field = flow.get('srcmac')
    if srcmac_field is not None:
        msg.match.dl_src = EthAddr(str(flow['srcmac']))
        msg.actions.append(of.ofp_action_nw_addr.set_dst(IPAddr('10.0.0.3')))
        msg.actions.append(of.ofp_action_dl_addr.set_dst(EthAddr('00:00:00:00:00:03')))
        msg.actions.append(of.ofp_action_output(port=3))

    return msg

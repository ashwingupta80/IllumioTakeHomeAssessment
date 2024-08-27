import unittest
from unittest.mock import patch, mock_open
from src.flow_log_processor import parse_protocol_mapping, parse_lookup_table, process_flow_logs, generate_output

class TestFlowLogProcessor(unittest.TestCase):

    #@patch('builtins.open', new_callable=mock_open, read_data="Decimal,Keyword\n6,transmission control\n17,user datagram\n")
    def test_parse_protocol_mapping(self):
        expected_output = {0: 'hopopt', 1: 'icmp', 2: 'igmp', 3: 'ggp', 4: 'ipv4', 5: 'st', 6: 'tcp', 7: 'cbt', 8: 'egp', 9: 'igp', 10: 'bbn-rcc-mon', 11: 'nvp-ii', 12: 'pup', 13: 'argus (deprecated)', 14: 'emcon', 15: 'xnet', 16: 'chaos', 17: 'udp', 18: 'mux', 19: 'dcn-meas', 20: 'hmp', 21: 'prm', 22: 'xns-idp', 23: 'trunk-1', 24: 'trunk-2', 25: 'leaf-1', 26: 'leaf-2', 27: 'rdp', 28: 'irtp', 29: 'iso-tp4', 30: 'netblt', 31: 'mfe-nsp', 32: 'merit-inp', 33: 'dccp', 34: '3pc', 35: 'idpr', 36: 'xtp', 37: 'ddp', 38: 'idpr-cmtp', 39: 'tp++', 40: 'il', 41: 'ipv6', 42: 'sdrp', 43: 'ipv6-route', 44: 'ipv6-frag', 45: 'idrp', 46: 'rsvp', 47: 'gre', 48: 'dsr', 49: 'bna', 50: 'esp', 51: 'ah', 52: 'i-nlsp', 53: 'swipe (deprecated)', 54: 'narp', 55: 'min-ipv4', 56: 'tlsp', 57: 'skip', 58: 'ipv6-icmp', 59: 'ipv6-nonxt', 60: 'ipv6-opts', 61: '', 62: 'cftp', 63: '', 64: 'sat-expak', 65: 'kryptolan', 66: 'rvd', 67: 'ippc', 68: '', 69: 'sat-mon', 70: 'visa', 71: 'ipcv', 72: 'cpnx', 73: 'cphb', 74: 'wsn', 75: 'pvp', 76: 'br-sat-mon', 77: 'sun-nd', 78: 'wb-mon', 79: 'wb-expak', 80: 'iso-ip', 81: 'vmtp', 82: 'secure-vmtp', 83: 'vines', 84: 'iptm', 85: 'nsfnet-igp', 86: 'dgp', 87: 'tcf', 88: 'eigrp', 89: 'ospfigp', 90: 'sprite-rpc', 91: 'larp', 92: 'mtp', 93: 'ax.25', 94: 'ipip', 95: 'micp (deprecated)', 96: 'scc-sp', 97: 'etherip', 98: 'encap', 99: '', 100: 'gmtp', 101: 'ifmp', 102: 'pnni', 103: 'pim', 104: 'aris', 105: 'scps', 106: 'qnx', 107: 'a/n', 108: 'ipcomp', 109: 'snp', 110: 'compaq-peer', 111: 'ipx-in-ip', 112: 'vrrp', 113: 'pgm', 114: '', 115: 'l2tp', 116: 'ddx', 117: 'iatp', 118: 'stp', 119: 'srp', 120: 'uti', 121: 'smp', 122: 'sm (deprecated)', 123: 'ptp', 124: 'isis over ipv4', 125: 'fire', 126: 'crtp', 127: 'crudp', 128: 'sscopmce', 129: 'iplt', 130: 'sps', 131: 'pipe', 132: 'sctp', 133: 'fc', 134: 'rsvp-e2e-ignore', 135: 'mobility header', 136: 'udplite', 137: 'mpls-in-ip', 138: 'manet', 139: 'hip', 140: 'shim6', 141: 'wesp', 142: 'rohc', 143: 'ethernet', 144: 'aggfrag', 145: 'nsh'}
        result = parse_protocol_mapping('protocol-numbers-1.csv')
        #print("Result ",result)
        self.assertEqual(result, expected_output)

    #@patch('builtins.open', new_callable=mock_open, read_data="dstport,protocol,tag\n25,tcp,sv_P1\n443,tcp,sv_P2\n")
    def test_parse_lookup_table(self):
        expected_output = {(25, 'tcp'): 'sv_p1',(68, 'udp'): 'sv_p2',(23, 'tcp'): 'sv_p1',(31, 'udp'): 'sv_p3',(443, 'tcp'): 'sv_p2',(22, 'tcp'): 'sv_p4',(3389, 'tcp'): 'sv_p5',(0, 'icmp'): 'sv_p5',(110, 'tcp'): 'email',(993, 'tcp'): 'email',(143, 'tcp'): 'email'}
        result = parse_lookup_table('lookup_table.csv')
        self.assertEqual(result, expected_output)

    #@patch('builtins.open', new_callable=mock_open, read_data="2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK\n")
    def test_process_flow_logs(self):
        lookup_table = {(25, 'tcp'): 'sv_p1',(68, 'udp'): 'sv_p2',(23, 'tcp'): 'sv_p1',(31, 'udp'): 'sv_p3',(443, 'tcp'): 'sv_p2',(22, 'tcp'): 'sv_p4',(3389, 'tcp'): 'sv_p5',(0, 'icmp'): 'sv_p5',(110, 'tcp'): 'email',(993, 'tcp'): 'email',(143, 'tcp'): 'email'}
        protocol_mapping = {0: 'hopopt', 1: 'icmp', 2: 'igmp', 3: 'ggp', 4: 'ipv4', 5: 'st', 6: 'tcp', 7: 'cbt', 8: 'egp', 9: 'igp', 10: 'bbn-rcc-mon', 11: 'nvp-ii', 12: 'pup', 13: 'argus (deprecated)', 14: 'emcon', 15: 'xnet', 16: 'chaos', 17: 'udp', 18: 'mux', 19: 'dcn-meas', 20: 'hmp', 21: 'prm', 22: 'xns-idp', 23: 'trunk-1', 24: 'trunk-2', 25: 'leaf-1', 26: 'leaf-2', 27: 'rdp', 28: 'irtp', 29: 'iso-tp4', 30: 'netblt', 31: 'mfe-nsp', 32: 'merit-inp', 33: 'dccp', 34: '3pc', 35: 'idpr', 36: 'xtp', 37: 'ddp', 38: 'idpr-cmtp', 39: 'tp++', 40: 'il', 41: 'ipv6', 42: 'sdrp', 43: 'ipv6-route', 44: 'ipv6-frag', 45: 'idrp', 46: 'rsvp', 47: 'gre', 48: 'dsr', 49: 'bna', 50: 'esp', 51: 'ah', 52: 'i-nlsp', 53: 'swipe (deprecated)', 54: 'narp', 55: 'min-ipv4', 56: 'tlsp', 57: 'skip', 58: 'ipv6-icmp', 59: 'ipv6-nonxt', 60: 'ipv6-opts', 61: '', 62: 'cftp', 63: '', 64: 'sat-expak', 65: 'kryptolan', 66: 'rvd', 67: 'ippc', 68: '', 69: 'sat-mon', 70: 'visa', 71: 'ipcv', 72: 'cpnx', 73: 'cphb', 74: 'wsn', 75: 'pvp', 76: 'br-sat-mon', 77: 'sun-nd', 78: 'wb-mon', 79: 'wb-expak', 80: 'iso-ip', 81: 'vmtp', 82: 'secure-vmtp', 83: 'vines', 84: 'iptm', 85: 'nsfnet-igp', 86: 'dgp', 87: 'tcf', 88: 'eigrp', 89: 'ospfigp', 90: 'sprite-rpc', 91: 'larp', 92: 'mtp', 93: 'ax.25', 94: 'ipip', 95: 'micp (deprecated)', 96: 'scc-sp', 97: 'etherip', 98: 'encap', 99: '', 100: 'gmtp', 101: 'ifmp', 102: 'pnni', 103: 'pim', 104: 'aris', 105: 'scps', 106: 'qnx', 107: 'a/n', 108: 'ipcomp', 109: 'snp', 110: 'compaq-peer', 111: 'ipx-in-ip', 112: 'vrrp', 113: 'pgm', 114: '', 115: 'l2tp', 116: 'ddx', 117: 'iatp', 118: 'stp', 119: 'srp', 120: 'uti', 121: 'smp', 122: 'sm (deprecated)', 123: 'ptp', 124: 'isis over ipv4', 125: 'fire', 126: 'crtp', 127: 'crudp', 128: 'sscopmce', 129: 'iplt', 130: 'sps', 131: 'pipe', 132: 'sctp', 133: 'fc', 134: 'rsvp-e2e-ignore', 135: 'mobility header', 136: 'udplite', 137: 'mpls-in-ip', 138: 'manet', 139: 'hip', 140: 'shim6', 141: 'wesp', 142: 'rohc', 143: 'ethernet', 144: 'aggfrag', 145: 'nsh'}
        tag_counts, port_protocol_counts = process_flow_logs('flow_logs.txt', lookup_table, protocol_mapping)
        self.assertEqual(tag_counts, {'untagged': 8, 'sv_p2': 1, 'sv_p1': 2, 'email': 3})
        self.assertEqual(port_protocol_counts, {(49153, 'tcp'): 1,(49154, 'tcp'): 1,(49155, 'tcp'): 1,(49156, 'tcp'): 1,(49157, 'tcp'): 1,(49158, 'tcp'): 1,(80, 'tcp'): 1,(1024, 'tcp'): 1,(443, 'tcp'): 1,(23, 'tcp'): 1,(25, 'tcp'): 1,(110, 'tcp'): 1,(993, 'tcp'): 1,(143, 'tcp'): 1})

    #@patch('builtins.open', new_callable=mock_open)
    def test_generate_output(self):
        tag_counts = {'sv_p2': 1, 'untagged': 2}
        port_protocol_counts = {(443, 'tcp'): 1, (25, 'tcp'): 1}
        generate_output(tag_counts, port_protocol_counts)
        #mock_file.assert_called()  # Check if file write operations were called

if __name__ == '__main__':
    unittest.main()

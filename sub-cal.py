import ipaddress
import math

def get_class(ip):
    first_octet = int(ip.split('.')[0])
    if 1 <= first_octet <= 126:
        return "A", "255.0.0.0"
    elif 128 <= first_octet <= 191:
        return "B", "255.255.0.0"
    elif 192 <= first_octet <= 223:
        return "C", "255.255.255.0"
    else:
        return "Unknown", "N/A"

def binary_mask(mask):
    return ".".join([f'{int(octet):08b}' for octet in mask.split('.')])

def calculate_subnet(ip_str, required_hosts):
    ip_class, default_mask = get_class(ip_str)
    default_binary = binary_mask(default_mask)
    
    # Calculate how many bits are needed for host part
    host_bits = math.ceil(math.log2(required_hosts + 2))  # +2 for network and broadcast
    subnet_bits = 32 - host_bits
    new_mask = str(ipaddress.IPv4Network(f'0.0.0.0/{subnet_bits}').netmask)
    new_mask_binary = binary_mask(new_mask)
    
    # Determine subnet group size
    SG = 2 ** host_bits
    
    # Total 1s and 0s in new subnet mask
    total_ones = subnet_bits
    total_zeros = 32 - subnet_bits
    
    # Extended part from default to new mask (only those octets matter for host per subnet)
    default_mask_bin = ''.join([f'{int(x):08b}' for x in default_mask.split('.')])
    new_mask_bin = ''.join([f'{int(x):08b}' for x in new_mask.split('.')])
    
    # Subtract default 1s from new 1s to get extended subnet area
    extended_subnet_ones = new_mask_bin.count('1') - default_mask_bin.count('1')

    # Host counts
    host_per_network = 2 ** total_zeros
    host_per_subnet = 2 ** extended_subnet_ones

    # Output
    print("\nSolution")
    print(f"Host per network = 2^{total_zeros} = {host_per_network}")
    print(f"Host per subnet  = 2^{extended_subnet_ones} = {host_per_subnet}\n")

    print(f"1. Class {ip_class} - Default Subnet Mask: {default_mask}")
    print(f"2. Default Binary : {default_binary}")
    print(f"3. Required Hosts : {required_hosts} ({bin(required_hosts)[2:]}) → Needs {host_bits} bits")
    print(f"4. New Subnet Mask: {new_mask} or /{subnet_bits}")
    print(f"5. New Binary     : {new_mask_binary}")
    print("6. Network Ranges (Subnets)")
    print(f"{'Network Address':<20} {'Broadcast Address':<20}")

    # Print all subnets within the classful range
    classful_network = ipaddress.IPv4Network(f"{ip_str}/{default_mask}", strict=False)
    current = int(classful_network.network_address)
    end = int(classful_network.broadcast_address)

    while current + SG - 1 <= end:
        net_start = ipaddress.IPv4Address(current)
        net_end = ipaddress.IPv4Address(current + SG - 1)
        print(f"{str(net_start):<20} {str(net_end):<20}")
        current += SG

if __name__ == "__main__":
    print("Subnetting Tool\n")
    ip_input = input("Enter IP address (e.g., 216.21.5.0): ").strip()
    hosts_input = int(input("Enter hosts per subnet (e.g., 30): ").strip())
    calculate_subnet(ip_input, hosts_input)

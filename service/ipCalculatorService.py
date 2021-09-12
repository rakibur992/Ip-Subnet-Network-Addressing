import ipcalc
from ipaddress import IPv4Network
from flask import jsonify
from math import ceil, log
def getFirstAndLastAddressWithNumberOfAddress(ipWithMask):
    ip_address = IPv4Network(ipWithMask,False)
    return f"{ip_address[0]}/{ip_address.prefixlen}", f"{ip_address[-1]}/{ip_address.prefixlen}",ip_address.num_addresses,ip_address


def getModelOneAnswer(ip):

    first_address,last_address , numberOfAddress,_= getFirstAndLastAddressWithNumberOfAddress(ip)
    return jsonify({'first_address': first_address, 'last_address':last_address , 'numberOfAddress':numberOfAddress})



def getModelOneAnswerWithId(id):
    x1 = int(id[0:3])
    x2 = int(id[3:5])
    x3 = int(id[5:7])
    x4 = 0
    p = int(id[0:2])
    subnetArray = [[240,120,2000],[4000,800,400]]
    ip = f"{x1}.{x2}.{x3}.{x4}/{p}"
    base_first_address,base_last_address , numberOfAddress,network = getFirstAndLastAddressWithNumberOfAddress(ip)
    response = dict()
    count = 0
    response[count] = {'first_address': base_first_address, 'last_address':base_last_address , 'numberOfAddress':numberOfAddress}
    existingSubnetArr = []
    for subnets in subnetArray:
        count += 1
        response[count]= getSubnetsWithUnusedAddress(existingSubnetArr,network,subnets)
        
    return response
def getNextPowerOf2(x):
    return pow(2, ceil(log(x)/log(2)))
def getMask(x):
    return int(32-(log(x)/log(2)))
def getSubnetsWithUnusedAddress(existingSubnetArr,network,subnets):
    subnets = [getNextPowerOf2(address) for address in subnets]
    subnets.sort(reverse=True)
    masks = [getMask(address) for address in subnets]
    subnetDict = dict()
    
    for address,mask in zip(subnets,masks):
        genSubnet = network.subnets(new_prefix=mask)
        subnet = next(genSubnet)
        for existingSubnet in existingSubnetArr:
            while subnet.supernet_of(existingSubnet) or subnet.subnet_of(existingSubnet):
                subnet = next(genSubnet)
        existingSubnetArr.append(subnet)
        subnetDict[address] = {'first_address': f"{subnet[0]}/{mask}", 'last_address': f"{subnet[-1]}/{mask}" }
    return subnetDict

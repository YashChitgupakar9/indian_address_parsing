import re

# Sample input file
inpfile = open("sample_addresses.txt", 'r').read().split('\n')

# Output file
outfile = open("formatted_addresses.txt", 'w')

def floorNum(num):
    if num.group('num'):
        try:
            addr_dic['FloorNumber'].append(num.group('num'))
        except:
            addr_dic['FloorNumber'] = [num.group('num')]
    return ''

def blockNum(num):
    if num.group('num'):
        try:
            addr_dic['BlockNumber'].append(num.group('num'))
        except:
            addr_dic['BlockNumber'] = [num.group('num')]
    return ''

def sectorNum(num):
    if num.group('num'):
        try:
            addr_dic['SectorNumber'].append(num.group('num'))
        except:
            addr_dic['SectorNumber'] = [num.group('num')]
    return ''

def pincodeNum(num):
    if num.group('num'):
        try:
            addr_dic['pincode'].append(num.group('num'))
        except:
            addr_dic['pincode'] = [num.group('num')]
    return ''

def pocketNum(num):
    if num.group('num'):
        try:
            addr_dic['PocketNumber'].append(num.group('num'))
        except:
            addr_dic['PocketNumber'] = [num.group('num')]
    return ''

def houseNum(num):
    if num.group('num'):
        try:
            addr_dic['HouseNumber'].append(num.group('num'))
        except:
            addr_dic['HouseNumber'] = [num.group('num')]
    return ''

for i in range(len(inpfile)):
    Name, inp_address = inpfile[i].split('\t')
    addr_dic = {}
    
    inp_address = re.sub(r"\\", r'\/', inp_address)
    inp_address = re.sub("(?P<num>(((?<![a-z])X|(?<![a-z])IX|(?<![a-z])IV|(?<![a-z])I{1,3}))(?![a-z]))\s*(rd|st|nd|th)*\s*(FLOOR|FLR|FL(?![a-z])|FOOR)", floorNum, inp_address, flags = re.I | re.S | re.X)
    inp_address = re.sub("H[^\w\,]+I[^\w\,]+G[^\w\,]*(?![a-z])", 'HIG', inp_address, flags = re.I | re.S)
    inp_address = re.sub("M[^\w\,]+I[^\w\,]+G[^\w\,]*(?![a-z])", 'MIG', inp_address, flags = re.I | re.S)
    inp_address = re.sub("L[^\w\,]+I[^\w\,]+G[^\w\,]*(?![a-z])", 'LIG', inp_address, flags = re.I | re.S)
    inp_address = re.sub("(?<![a-z])([a-z])[^\w\,]+([a-z])[^\w\,]+([a-z])[^\w\,]+([a-z])(?![a-z])", r'\1\2\3\4', inp_address, flags = re.I | re.S)
    inp_address = re.sub("^\W*(?P<num>[0-9]\W*[a-z])\W+(BLOCK|BLK|BLCOK)", blockNum, inp_address, flags = re.I | re.S | re.X)
    inp_address = re.sub("(BLOCK|BLK|BLCOK)[^\w\,]+(NUMBER|NUM|NO)?\W*(?P<num>[a-z]\W*(i{1,3}|\d+))(?![a-z])", blockNum, inp_address, flags = re.I | re.S | re.X)
    inp_address = re.sub("(SECTOR|SCETOR|SECT|SEC)[^\w\,]+(NO|NUMBER|NUM)?[^\w\,]*(?P<num>\d{1,3}|(((?<![a-z])X|(?<![a-z])IX|(?<![a-z])IV|(?<![a-z])I{1,3}))(?![a-z]))", sectorNum, inp_address, flags = re.I | re.S | re.X)
    inp_address = re.sub("(SECTOR|SCETOR|SECT|SEC)\W*(?P<num>\d+)(?![a-z])", sectorNum, inp_address, flags = re.I | re.S | re.X)
    inp_address = re.sub("(?<![0-9])(?P<num>\d{6})(?![0-9])", pincodeNum, inp_address, flags = re.I | re.S)

    inp_address = re.sub("""(?P<delimit>NAGAR\s*MARKET | NAGAR\s*(COLONY|CLY|SOCIETY)?
    | [a-z]\s+(BASTI | VIHAR\s*(IV|III|II|I)? | GANJ | COLONY | PLAZA | ROAD | NAGAR\W*(IV|III|II|I) | PARK | FLATS  ) | appartment 
    | (\w\s+)MANDIR)[^\w\,]+(?!\,)""", '\g<delimit>' + ' ,', inp_address, flags = re.I | re.S | re.X)
     
    inp_address = re.sub("(?<=[\,\s])\s*(?P<num>[a-z]{1-2}(-|\/)?\d+[a-z](?=[\,\s]))", houseNum, inp_address, flags = re.I | re.S | re.X) # c-123 or g-23 a
    inp_address = re.sub("(?<=[\,\s])(?P<num>[a-z]{1-2}(-|\/)?\d+(?=[\,\s]))", houseNum, inp_address, flags = re.I | re.S | re.X) 
    inp_address = re.sub("^\s*(?P<num>\d+(-|\/)?[a-z](?=[\,\s]))", houseNum, inp_address, flags = re.I | re.S | re.X)    #123/A
        
    inp_address = re.sub("^\s*(?P<num>[a-z]{1,2}(-|\/)?\d+([a-z])?)", houseNum, inp_address, flags = re.I | re.S | re.X) #c-123 or g-92 a 
    
    inp_address = re.sub("(?<=[\,\s])(?P<num>\d+(-|\/)?[a-z])", houseNum, inp_address, flags = re.I | re.S | re.X)

    inp_address = re.sub("(?<=[\,\s])(?P<num>\d+(-|\/)?\d+)(?![0-9])", houseNum, inp_address, flags = re.I | re.S | re.X)
    
    inp_address = re.sub("(?P<num>\d+)", houseNum, inp_address, flags = re.I | re.S | re.X)
    
    firstline = True
    for attr, val in addr_dic.items():
        for v in range(len(val)):
            if not firstline:
                outfile.write('\t'.join([' '*len(Name), attr + '_' +  str(v+1), val[v].lower()]) + '\n')
            else:
                outfile.write('\t'.join([Name, attr + '_' +  str(v+1), val[v].lower()]) + '\n')
                firstline = False
    
    localities = [i.strip(' ') for i in inp_address.split(',')]
    for loc in range(len(localities)):
        localities[loc] = re.sub("block", '', localities[loc], flags = re.I | re.S)
        localities[loc] = re.sub("^\W+", '', localities[loc], flags = re.I | re.S)
        localities[loc] = re.sub("\W+$", '', localities[loc], flags = re.I | re.S)
        if localities[loc]:
            outfile.write('\t'.join([' '*len(Name), 'Locality_' +  str(loc+1), localities[loc].lower()]) + '\n')    # Person    Locality-1    LocName
    
    outfile.write('\n')

outfile.close()

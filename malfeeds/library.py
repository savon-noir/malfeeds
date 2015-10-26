import re


def valid_type(strtype):
    tlist = ['ip',
             'subnet',
             'domain',
             'url',
             'email',
             'dummy'
    ]
    return strtype in tlist

def check_ip(item):
    ip = None
    regres = re.compile('^\s*([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\s*').search(item)
    if regres is not None:
        ip = regres.group(1)
    return ip


def check_subnet(item):
    subnet = None
    regres = re.compile('^\s*([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\/[0-9]{1,2})\s*').search(item)
    if regres is not None:
        subnet = regres.group(1)
    return subnet


def check_url(item):
    url = None
    m =  re.compile('^(http(?:s)?:\/\/.*$|^[^:\/\.\s]{1,}\.[^:\/\.\s]*[^:\s]*)').search(item)
    if m is not None:
        url = m.group(1)
    return url


def check_file(item):
    filepath = None

    m = re.compile('^(?:file:\/\/)?(.*)').search(item)
    if m is not None:
        filename = m.group(1)
        from os.path import isfile as os_isfile
        fexists = os_isfile(filename)
        if fexists:
            filepath = filename

    return filepath

def get_item_type(item):
    itype = None
    if check_subnet(item) is not None:
        itype = 'subnet'
    elif check_ip(item) is not None:
        itype = 'ip'
    elif check_url(item) is not None:
        itype = 'url'
    return itype

def get_clean_item(item, itype='ip'):
    rval = ''
    if itype == 'ip':
        rval = check_ip(item)
    elif itype == 'subnet':
        rval = check_subnet(item)
    elif itype == 'url':
        rval = check_url(item)
    else:
        rval = item
    return rval

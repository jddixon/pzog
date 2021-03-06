# ~/dev/py/pzog/pzog/__init__.py

__version__ = '0.6.13'
__version_date__ = '2018-03-23'

__all__ = ['__version__', '__version_date__',
           'PZOG_MAX_MSG', 'PZOG_PORT', 'RING_IP_ADDR',

           # methods
           'ring_size', ]

# the maximum number of bytes in a message
PZOG_MAX_MSG = 512

PZOG_PORT = 55552        # for this version, v0.2.x

# these are indexed in this order
RING_IP_ADDR = [('losaltos', '192.168.152.253'),
                ('test', '192.168.152.10'),
                ('losgatos', '192.168.136.254'),
                ('supermicro', '192.168.144.16'),
                ('guadalupe', '192.168.152.254'), ]


@property
def ring_size():
    return len(RING_IP_ADDR)

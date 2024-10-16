import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/ny/FsRobo-A1/install/fsrobo_a1_serve_py'

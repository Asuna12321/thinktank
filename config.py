from multiprocessing import cpu_count

# This is where you put the data
# DATA_PATH = r'D:\Dataset\ThinkTank'
# DATA_PATH = r'C:\Users\impor\PycharmProjects\ThinkTank\data'

DATA_PATH = r'C:\Users\Jin tian Zhou\PycharmProjects\thinktank'
USE_DATA = 'asn'  # 'asn' or 'dblp', 'asn' for academic social network

# Count for cpu cores, used for multi processing
CPU_COUNT = cpu_count() // 2

# DEFAULT USING MULTIPROCESSING
# NUM JOBBERS
N_JOBS = CPU_COUNT

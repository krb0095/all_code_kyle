#  this code is writen to find the frame that we get to eq\

import numpy as np
import sys
def check_eq(data,std_max=0.05):
    """check_eq returns a bool when the std of a numpy array is less then
    the vaule of std_max

    data : 1d numpy array
    std_max : thershold that if the std is less then we are consider in eq
    """
    # smaple size
    num_samples = len(data)
    # find if the std error of the sample is less than std_max
    if np.std(data) / np.sqrt(num_samples) < std_max:
        # stop
        ans = True
    else:
        ans = False
    return ans

def block_eq_check(timeseries,std_max=0.05,chuck_size=100,stride=1):
    """block_eq_check takes the frist chuck_size frames and evalutes if the
    current lenght of the data frame has a std less then  std_max
    timeseries : 1d numpy array of all vaules in the timeseries for eq
    std_max : thershold that if the std is less then we are consider in eq
    chuck_size : sets the intail size of the data and how much we add each time
    stride : how many frames we skip over in the data array
    """
    # stride the numpy array
    data = timeseries[::stride]
    # vaildate that the strided data < than the data array
    # we times chuck_size by there so we have at least three loop in the while
    assert len(data) > chuck_size *3 , "The chunck size X 3 given is greater than then total lenght of the data"
    chunk = 0
    iters = 0
    while True:
        # add one to the iteration
        iters += 1
        if iters >= 100000:
            # to many times we brake
            chunk = 0
            break
        # check first chuck_size
        chunk += chuck_size
        # if the chunk is > the total lenght of data then use we can not be at eq
        assert chunk <= len(data) , "system can not be at eq. due to reaching total timeseries size"
        # check when check_eq is not at eq
        # if this is true we contiune to add
        if check_eq(data[:chunk],std_max): # check_eq is ture when we are at eq
        # not check_eq is true when we are not eq
        # if this is true we can break
            break
    # we nor have to total chunk size that we get to eq
    return chunk
def exact_frame_to_cut(data,std_max=0.05,stride=1,chuck_size=100):
    """ increament frame by frame till we get the excat trame to cut to """
    # find the chunk size
    chunk = block_eq_check(data, std_max=std_max,chuck_size=chuck_size,stride=stride)
    # shorten data to size
    if chunk != 0: #chunk 0 is that there is not size for eq

        cnt = 0
        while True:
            data_not_eq = data[:int(chuck_size*0.2) +cnt] # using 20% of cghunck to start
            cnt += 1
            if check_eq(data_not_eq,std_max):
                # break out of while
                break
        # the frame we should cut is int(chuck_size*0.2) +cnt
    return int(chuck_size*0.2) +cnt

def cut_data_to_production(data,chunk):
    after_cut_lenght = len(data) - chunk
    return data[:after_cut_lenght]


if __name__ == '__main__':
    # given data file
    file = sys.argv[1]
    # column number
    col_num = int(sys.argv[2])
    # create 1d numpy array
    data = np.loadtxt(file)[:,col_num]
    # checking for other items
    # defult vaules
    std_max = 0.05
    chuck_size = 100
    stride = 1
    if len(sys.argv) == 4:
        # setting the std_max to a new values
        std_max = float(sys.argv[3])
    elif len(sys.argv) == 5:
        std_max = float(sys.argv[3])
        # max and chunk to serach by
        chuck_size = int(sys.argv[4])
    elif len(sys.argv) == 6:
        std_max = float(sys.argv[3])
        # max and chunk to serach by
        chuck_size = int(sys.argv[4])
        # adding stride
        stride = int(sys.argv[5])



    # run the code for exact cut
    chunk = exact_frame_to_cut(data,std_max=std_max,stride=stride,chuck_size=chuck_size)
    print(file , 'production length',chunk)

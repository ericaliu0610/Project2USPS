from XMLGetter import sendRequest
from GenCheckDigit import gen_check_digit
import pickle
import time
import random


def fetchContinuData(pre_serial, tra_start, tra_end, file_des):
    '''
    Given a format correct tracking number, send request to USPS API to fetch its related information,
    if there is information on the server, it will be saved as a pickle file in file_des
    :param pre_serial: CIA (channel application id) + Service Type Code + Mailer ID, Ex. 94055102008835 
    :param tra_start: start of the serial number, in my case is a 7 digit, Ex.5753000
    :param tra_end: end of the serial number, in my case is a 7 digit, Ex.5754999
    :param file_des: the file destination of the file one want to save results from API
    :return: 9405510200883500
    '''
    with open(file_des, "ab") as f:

        id = 1
        if tra_start % 100000 != 0 or tra_end % 100000 != 99999:
            print("Plz input trajectory start and end id numbers in the format like 1100000, 1299999")
            exit()
        else:
            batch_num = int((tra_end + 1 - tra_start) / 100000)
            for batch in range(batch_num):
                sample_id = random.sample(range(100000), 3000)
                for i in sample_id:
                    package_ic = str(pre_serial) + str(tra_start+batch*100000 + i).zfill(7)
                    package_ic += gen_check_digit(package_ic)
                    tracking_dict = sendRequest(package_ic)
                    time.sleep(0.05)

                    if 'TrackDetail' in tracking_dict.keys():
                        pickle.dump(tracking_dict, f)
                        print("valid tracking # " + str(id) + ": " + package_ic + " has been fetched")
                        id += 1
                        # else :
                        #     print "No info for tracking #: " + package_ic

    print("The process is finished!")

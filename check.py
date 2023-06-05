import re
from criterias.chi2kol import Interval

class DataCheck():
    def __init__(self) -> None:
        pass
    @staticmethod    
    def toCheck(data_int):
        regex = re.compile(r"([-+.,\d]+)[,\s]+([-+.,\d]+)")
        
        intervals = []
        for i in range(len(data_int)):
            matching =  re.search(regex, data_int[i])
            if(matching.group(1),matching.group(2)):
                intervals.append(Interval(float(matching.group(1).replace(",",".")),float(matching.group(2).replace(",","."))))
            else:
                raise ValueError

        return intervals

#chi2kol.TableForX2([int(i) for i in ["2","3"]], DataCheck.toCheck(["[3, 4)"," [4 5)"]),2, 0.05 )


        
        
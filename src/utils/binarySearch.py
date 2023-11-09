def lastTrueIndexBinarySearch(begin, end, condition):
    if begin >= end:
        return begin
    middle = (begin + end + 1) // 2
    bool = condition(middle)
    if bool:
        return lastTrueIndexBinarySearch(middle, end, condition)
    else:
        return lastTrueIndexBinarySearch(begin, middle-1, condition)
         

def firstFalseIndexBinarySerch(begin, end, condition):
    if begin >= end:
        return begin
    middle = (begin + end) // 2
    bool = condition(middle)
    if bool:
        return firstFalseIndexBinarySerch(middle + 1, end, condition)
    else:
        return firstFalseIndexBinarySerch(begin, middle, condition)
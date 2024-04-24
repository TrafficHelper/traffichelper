#import application
import csv

def range(filepath:str, index:int):
    data = {*()}
    with open(filepath) as file:
        parser = csv.reader(file)
        first = True
        for line in parser:
            element = line[index]
            if first:
                variable = element
                first = False
            data.add(element)
    return (variable, data)





    # classification = []
    # with open(filepath) as file:
    #     parser = csv.reader(file, delimiter=' ')
    #     first = True
    #     for line in parser:
    #         if first:
    #             classification+=[(elem,{*()}) for elem in line]
    #             first = False
    #         for index in range(len(classification)):
    #             classification[index][1].add(line[index])
    # return classification

if __name__ == '__main__':
    s = {*()}
    s.add(3)
    print(str(s))
    print([1,2] == [1,2])
    filename = 'C:/Users/SAT/PycharmProjects/traffic/Data/TrafficCollisionData.csv'
    print(range(filename, 11))
    print(range(filename, 12))
    print(range(filename, 13))
    print(range(filename, 9))
# Parse road centerlines

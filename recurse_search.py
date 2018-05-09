import sys
import os
import os.path as path
import re
import matplotlib.pyplot as plt
import numpy as np

'''
Author:     Daryl Pham 
Date:       2018/09/05
'''


''' 
 Search function that recursively traverses the root_dir and sub_dirs and counts the number 
 of files that contain a match to the provided keyword/pattern.
''' 
def search(directory, keyword, sub_dir = ''):

    pattern = re.compile(keyword)
    result = {sub_dir : 0} if sub_dir != '' else {'root_dir' : 0}
    
    try:
        #If the directory exists get a list of items in it, else raise exception
        if not (path.lexists(directory)):
            raise Exception("Error: " + directory + " does not exist.")
        if not path.isdir(directory):
            raise Exception("Error: " + directory + " is not a valid directory.")
        
        
        #Iterate through each item in the directory and process based on whether
        #it is a file or a sub-directory
        for item in os.listdir(directory):
            if path.isdir(path.join(directory,item)):
                result = merge(result, search(path.join(directory,item), keyword, path.join(sub_dir, item)))
            elif re.search(pattern, item):
                if sub_dir == '':
                    result['root_dir'] = result['root_dir'] + 1
                else:
                    result[sub_dir] = result[sub_dir] + 1
        return result

    #If exceptions related to directory access is found, return to skip that 
    #directory and continue to the remaining sub-directories if any
    except PermissionError as e:
        print(e)
        return None
    except OSError as e:
        print(e)
        return None
    except Exception as e:
        print(e)
        sys.exit()

'''
 Function that merges two dictionaries together into one.
 Used to combine the returned dictionary with the current.
'''
def merge(a, b):
    if b == None:
        return a
    c = a.copy()
    c.update(b)
    return c

'''
 Function to plot the results of the search function.
'''
def plot(result):
    figure = plt.figure("Bar")
    ax = figure.add_subplot(1,1,1)
    ax.set(xlabel = "Sub-Directory", ylabel = "Count", title = ("Number of matched files in Dir/Sub-Dir of " + sys.argv[1]))
    x = sorted(result.keys())
    y = [result[i] for i in x]
    ax.set_yticks(np.arange(min(y), max(y)+1, 1))
    ax.bar(x, y)
    plt.show()

'''
 Function to print out dictionary with corresponding values
'''
def print_dict(dict):
    for key in sorted(dict.keys()):
        print(key + ": " + str(dict[key]))


'''
 Main Script
'''
def main():
    try:

        #Check the input and raise exception if there are any issues.  If not run Search, and then plot the results.
        if len(sys.argv) != 3:
            raise Exception("Error: Invalid number of Arguments - requires directory and keyword.")

        result = search(sys.argv[1], sys.argv[2])
        print(result)
        plot(result)
    
    except Exception as e:
        print(e)
        sys.exit()


if __name__ == "__main__":
    main()
import sys
import os
import os.path as path
import re
import matplotlib.pyplot as plt

''' 
 Search function that recursively traverses the root_dir and sub_dirs and counts the number 
 of files that contain a match to the provided keyword/pattern.
''' 
def search(directory, keyword):

    dir_list, result = None,  {directory: 0}
    base_dir = path.abspath(directory) + "\\"
    pattern = re.compile(keyword)

    try:
        #If the directory exists get a list of items in it, else raise exception
        if (path.lexists(directory)):
            dir_list = [base_dir + x for x in os.listdir(directory)]
        else:
            raise Exception("Error: " + directory + " is not a valid directory.")
        
        
        #Iterate through each item in the directory and process based on whether
        #it is a file or a sub-directory
        for item in dir_list:
            if path.isdir(item):
                result = merge(result, search(item, keyword))
            else:
                if re.search(pattern, item):
                    result[directory] = result[directory] + 1
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
    ax.set(xlabel = "Directory", ylabel = "Count", title = "Number of matched files in each Dir/Subdir")
    ax.bar(result.keys(), result.values())
    plt.show()

'''
 Where the Script begins
'''
try:

    #Check the input and raise exception if there are any issues.  If not run Search, and then plot the results.
    if len(sys.argv) != 3:
        raise Exception("Error: Invalid number of Arguments - requires directory and keyword.")

    result = search(sys.argv[1], sys.argv[2])
    for key in sorted(result.keys()):
        print(key + ": " + str(result[key]))
    plot(result)

except Exception as e:
    print(e)
    sys.exit()
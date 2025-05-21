from os import listdir

def find_paths(folder_in_cwd:str):
    """
    takes the path of a folder in the current working directory (must not end in /)

    returns a list of filepaths to all the files in its sub folders,
    ie this format: < input folder > / < sub folder > / < file.extension >

    any files in the main folder and any folders in the sub folder will be ignored

    """
    # find only folder paths
    folder_list = [folder_in_cwd + "/" + item for item in listdir(folder_in_cwd) if "." not in item]

    # find only files in those folders
    file_list = [folder + "/" + file for folder in folder_list for file in listdir(folder) if "." in file]

    return file_list

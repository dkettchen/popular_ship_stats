from os import listdir

# function to extract file paths into a list we can cycle through
def find_paths(folder_in_cwd: str):
    """
    takes a string specifying the folder path in the current working directory one wants \
    to extract file paths from the subfolders of

        -folder must have only one level of sub folders containing the files

        -there must not be un-foldered files present

        -string must end with a "/"

    returns a list of file paths leading to all files in the sub folders
    """
    folder_list = [folder_in_cwd + item for item in listdir(folder_in_cwd)]
    file_list = [folder + "/" + file  for folder in folder_list for file in listdir(folder)]
    return file_list

if __name__ == "__main__":
    print(find_paths("data/raw_data/"))
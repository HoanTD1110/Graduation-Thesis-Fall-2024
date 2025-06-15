import glob

def get_files(root_folder):
    filenames = []
    for filename in glob.iglob(root_folder + "/**/*.docx", recursive=True):
        filenames.append(filename)
    return sorted(filenames)
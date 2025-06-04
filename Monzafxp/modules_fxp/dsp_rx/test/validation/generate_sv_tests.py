import os
import re

# Get the current working directory
current_folder_path = os.getcwd()

# Get the parent folder's name
parent_folder = os.path.basename(os.path.abspath(os.path.join(current_folder_path, os.pardir)))

print(f"The parent folder name is: {parent_folder}")

file_name = f"../../../scratch/{parent_folder}_test/summary.txt"

# Open the file in read mode and read its contents
with open(file_name, "r") as file:
    content = file.read()

content_splited = content.split(" ")

# Regular expression pattern to match words starting with 'a' or 'c'
pattern = re.compile(f"^{parent_folder}")


# Find matching words
matching_words = [word for word in content_splited if re.match(pattern, word)]
names =[]

for i,name in enumerate(matching_words):
    names.append(name.split("\n")[0])

path_to_save = f"/projects/farina16/crn16ffPLUSll_sos/work/ibalbo/farina_tc_dsp/modules/{parent_folder}/verification/tests/"


# Open the file in write mode to create it, then close it
for name in names:
    

    try:
        with open(path_to_save+"usim_"+name+".sv", "x") as file:
            pass

        print(f"Archivo 'usim_{name}.sv' creado exitosamente.")
    except FileExistsError:
        print(f"El archivo 'usim_{name}.sv' ya existe. No se ha creado ningún archivo nuevo.")





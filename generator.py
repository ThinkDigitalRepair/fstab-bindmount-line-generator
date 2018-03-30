import time
from os import path, makedirs, listdir
from pathlib import Path


def make_line(data_dir: str, home_dir: str, dir_to_link, create_nonexistant_dirs: bool = False):
    """

    :param data_dir: the directory you have your data mounted to.
    :param home_dir: the home directory you to add mounts to.
    :param dir_to_link: the name of the directory you want to link in your home directory
    :param create_nonexistant_dirs: True if you want to create directories for those that don't exist.
    :return:
    """
    full_dir = "{data_dir}/{dir}".format(data_dir=data_dir, dir=dir_to_link).replace("//", '/')
    if not path.isdir(full_dir):
        raise FileNotFoundError(full_dir)
    else:
        if create_nonexistant_dirs:
            makedirs("{home_dir}/directory".format(home_dir=home_dir), exist_ok=True)

        template = "{data_dir}/{dir} {home_dir}/{dir} none defaults,bind 0 0".format(
            data_dir=data_dir, home_dir=home_dir, dir=dir_to_link).replace('//', '/')
        return template


def gen_all_dirs(data_dir):
    return [dir for dir in listdir(data_dir) if path.isdir("{}/{}".format(data_dir, dir))]


def print_options():
    pass


def prompt(prompt_text: str, accept_blank: bool = False, base_dir: str = "") -> str:
    """

    :param prompt_text: the text to prompt the user with
    :param accept_blank: allow an empty response to be a valid response
    :param base_dir: for function calls that require extra information to check for valid folders.
    :return:
    """
    directory = input(prompt_text)

    if directory == "" and accept_blank:
        return ""
    elif directory.lower() == 'exit':
        return directory

    valid_dir = path.isdir(
        base_dir + '/' + directory if base_dir else directory)
    while not valid_dir:
        print("{dir} cannot be found. Please try again.".format(dir=directory))
        directory = input(prompt_text)
        valid_dir = path.isdir("{base_dir}/{dir}".format(base_dir=base_dir, dir=directory))

        if directory == "" and accept_blank:
            return ""
        elif directory.lower() == 'exit':
            return directory
    return directory


if __name__ == '__main__':
    # Home
    home = str(Path.home())
    d = prompt("Enter the full path to your home directory: Press enter to use {0}: ".format(home), accept_blank=True)
    home_dir = d if d else home

    # Data
    data_dir = prompt("Enter the full path to your data directory: ")
    print("Subdirectories of {data_dir}: ".format(data_dir=data_dir))
    time.sleep(2)
    for directory in gen_all_dirs(data_dir):
        print(directory)

    # Bind
    while True:
        dir_to_bind = prompt(
            "Enter the name of the directory you would like to bind (Type 'exit' to quit): {base_dir}/".format(
                base_dir=data_dir), base_dir=data_dir)

        if dir_to_bind == 'exit':
            break

        line = make_line(data_dir, home_dir, dir_to_bind)
        print('\n' + line + '\n')

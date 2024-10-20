import os, sys, json, shutil
from datetime import datetime

author = ''
min_ram = 0
max_ram = 0
world_backup_url = ''
world_log_url = ''
world_name = ''
log_name = ''


def main():
    if len(sys.argv) == 1:
        start()
    elif sys.argv[1] == '-c':
        clean_up()
    elif sys.argv[1] == '-d':
        download_world()
        download_log()
    elif sys.argv[1] == '-u':
        push_world()
        push_log()
    elif sys.argv[1] == '--clean':
        clean_up()
    elif sys.argv[1] == '--download':
        download_world()
        download_log()
    elif sys.argv[1] == '--upload':
        push_world()
        push_log()
    elif sys.argv[1] == "--json":
        print_json_config()
    elif sys.argv[1] == "--help":
        show_help()
    else:
        print("Argumento inválido")
        print("Tente 'python start.py --help' para mais informações.")


def print_json_config():
    """Print the content of the 'config.json' file.
    
    Does not return anything.
    """
    with open('config.json', 'r') as file:
        config = json.load(file)
    print(config)


def read_json_config():
    """Read the 'config.json' file and store its content in the global variables:

    - author
    - min_ram
    - max_ram
    - world_backup_url
    - world_log_url
    - world_name
    - log_name

    Does not return anything.
    """
    global author, min_ram, max_ram, world_backup_url, world_log_url, world_name, log_name

    with open('config.json', 'r') as file:
        config = json.load(file)

    author = config['author']
    min_ram = config['minRam']
    max_ram = config['maxRam']
    world_backup_url = config['worldBackupUrl']
    world_log_url = config['worldLogUrl']
    world_name = config["worldName"]
    log_name = config["logName"]


def download_world():
    """Downloads the world from the repository specified in the 'config.json' file to a new folder
    with the name specified in the 'config.json' file.

    Does not return anything.
    """
    os.system(f"git clone {world_backup_url}")
    write_to_log("download")


def download_log():
    """Downloads the log from the repository specified in the 'config.json' file to a new folder
    with the name specified in the 'config.json' file.

    Does not return anything.
    """
    os.system(f"git clone {world_log_url}")


def pull_world():
    """Pulls the latest version of the world from the repository specified in the 'config.json' file.
    
    The function navigates to the world directory, pulls the latest version from the repository, and
    navigates back to the parent directory.
    
    Does not return anything.
    """
    os.chdir(world_name)
    os.system("git pull")
    os.chdir("..")
    write_to_log("download")


def pull_log():
    """Pulls the latest version of the log from the repository specified in the 'config.json' file.
    
    The function navigates to the log directory, pulls the latest version from the repository, and
    navigates back to the parent directory.
    
    Does not return anything.
    """
    os.chdir(log_name)
    os.system("git pull")
    os.chdir("..")


def write_to_log(action: str):
    """
    Writes an entry to the log file and pushes changes to the remote repository.

    This function pulls the latest log changes, appends a new entry to the 'latest.txt' file
    with the current date and time, the author's name, and the specified action. The changes 
    are then staged, committed, and pushed to the remote repository.
    
    Does not return anything.
    """
    pull_log()

    log_date = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    set_owner(author)

    os.chdir(log_name)

    with open("latest.txt", "a") as file:
        file.write(f"\n{author} - {log_date} - {action}")
        file.close()
    
    os.system("git add *")
    os.system(f"git commit -m '{author}'")
    os.system("git push")
    os.chdir("..")


def get_owner() -> str:
    """
    Reads the current owner from the 'owner.txt' file and returns it.

    The function pulls the latest log changes, reads the 'owner.txt' file, and pushes the changes
    back to the remote repository.

    Returns a str that represents the new owner.
    """
    owner = ''
    
    pull_log()

    os.chdir(log_name)

    with open("owner.txt", "r") as file:
        owner = file.read()
    
    os.system("git add *")
    os.system(f"git commit -m '{author}'")
    os.system("git push")
    os.chdir("..")
    return owner


def set_owner(new_owner: str):
    """
    Sets the current owner in the 'owner.txt' file and pushes changes to the remote repository.

    This function pulls the latest log changes, writes the new owner to the 'owner.txt' file, and
    pushes the changes back to the remote repository.
    
    Does not return anything.
    """
    pull_log()

    os.chdir(log_name)

    with open("owner.txt", "w") as file:
        file.write(f"{new_owner}")
        file.close()
    
    os.system("git add *")
    os.system(f"git commit -m '{author}'")
    os.system("git push")
    os.chdir("..")


def start():
    """
    This function checks if the world and log directories exist, downloads them if they don't,
    then changes to the world directory and starts the server with the specified RAM. 
    If the program receives a KeyboardInterrupt, it prints a message and pushes changes to the world.

    Does not return anything.
    """
    read_json_config()

    if not os.path.exists(f"{log_name}") or len(os.listdir(f"{log_name}")) == 0:
        download_log()
    else:
        pull_log()
    if not os.path.exists(f"{world_name}") or len(os.listdir(f"{world_name}")) == 0:
        download_world()
    else:
        pull_world()

    os.chdir(world_name)

    try:
        os.system(f"java -Xmx{max_ram}G -Xms{min_ram}G -jar server.jar nogui")

        print("\033[94m\nFechando o programa...\033[0m")
    except KeyboardInterrupt: # Ctrl + C
        print("\033[94m\nFechando o programa...\033[0m")

    os.chdir("..")
    push_world()


def clean_up():
    """
    Ask the user for confirmation before deleting the local world.
    
    The function prompts the user with a confirmation message and proceeds to delete the local world 
    directory if the user confirms by entering 'Tenho absoluta certeza'. If the world directory exists, 
    it is removed along with a success message. If the world directory does not exist, a message is printed 
    indicating that the world does not exist.

    Does not return anything.
    """
    answer = input("Tem certeza que quer deletar o mundo local? [Tenho absoluta certeza/n]")
    if answer == "Tenho absoluta certeza":
        if os.path.exists(world_name):
            shutil.rmtree(world_name)
            print(f"O mundo '{world_name}' foi removido com sucesso.")
        else:
            print(f"O mundo não existe")


def push_world():
    """Pushes the world changes to the remote repository.

    This function navigates to the world directory, stages all changes, commits with the author's name,
    and pushes the changes to the remote repository.

    Does not return anything.
    """
    os.chdir(world_name)
    os.system("git add *")
    os.system(f"git commit -m'{author}'")
    os.system("git push")
    os.chdir("..")

    write_to_log("upload")


def push_log():
    """Pushes the log changes to the remote repository.

    This function navigates to the log directory, stages all changes, commits with the author's name,
    and pushes the changes to the remote repository.

    Does not return anything.
    """
    os.chdir(log_name)
    os.system("git add *")
    os.system(f"git commit -m '{author}'")
    os.system("git push")
    os.chdir("..")

    write_to_log("upload")


def show_help():
    """Print the help message for the start.py script.

    The help message includes information about how to use the script,
    what options are available, and examples of how to use the script.

    Does not return anything.
    """
    help_text = """
    Uso: python start.py [OPÇÃO]

    Opções:
      -c, --clean          Limpa o mundo local do servidor.
      -d, --download       Faz o download do mundo e do log.
      -u, --upload         Faz o upload do mundo e do log.
      --json               Lê a configuração em formato JSON.
      --help               Mostra esta mensagem de ajuda.

    Exemplos de uso:
      python start.py            Inicia o servidor, quando fechado faz upload do mundo e do log.
      python start.py --download Baixa os arquivos do mundo e log.
      python start.py --help     Exibe esta mensagem de ajuda.
    """
    print(help_text)


if __name__ == '__main__':
    main()
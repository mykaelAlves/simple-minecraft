import os, sys, json

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
    elif sys.argv[1] == "--json": #test
        read_json_config()
    else:
        print("Argumento inválido")


def read_json_config():
    global author, min_ram, max_ram, world_backup_url, world_log_url, world_name, log_name

    with open('config.json', 'r') as file:
        config = json.load(file)
    
    #print(config)

    author = config['author']
    min_ram = config['minRam']
    max_ram = config['maxRam']
    world_backup_url = config['worldBackupUrl']
    world_log_url = config['worldLogUrl']
    world_name = config["worldName"]
    log_name = config["logName"]


def download_world():
    os.system(f"git clone {world_backup_url}")


def download_log():
    os.system(f"git clone {world_log_url}")


def pull_world():
    os.system(f"cd {world_name}; git pull")


def pull_log():
    os.system(f"cd {log_name}; git pull")


# TODO
def write_to_log():
    pass


def start():
    read_json_config()

    if not os.path.exists(f"{world_name}") or len(os.listdir(f"{world_name}")) == 0:
        download_world()
    else:
        pull_world()
    if not os.path.exists(f"{log_name}") or len(os.listdir(f"{log_name}")) == 0:
        download_log()
    else:
        pull_log()

    os.system(f"cd {world_name}; java -Xmx{max_ram}G -Xms{min_ram}G -jar server.jar nogui")

    end()


def clean_up():
    os.system("rm -rf server/")


def end():
    os.system(f"cd {world_name}; git add *; git commit -m '.'; git push")


if __name__ == '__main__':
    main()
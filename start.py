import os, sys, json, shutil
from datetime import datetime

author = ''
min_ram = 4
max_ram = 6
world_backup_url = ''
world_log_url = ''
world_name = ''
log_name = ''

def main():
    start_json_config()

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
    elif sys.argv[1] == "--json": #test
        read_json_config()
    elif sys.argv[1] == "--help":
        show_help()
    else:
        print("Argumento inválido")
        print("Tente 'python start.py --help' para mais informações.")


def start_json_config():
    if not os.path.exists("config.json"):
        create_json_config()
    read_json_config()
    if author == "undefined":
        create_json_config()

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

def create_json_config():
    new_author = input("Seu nick: ")
    with open('config.json', 'w') as file:
        file.write(f"""{{
    "author": "{new_author}",
    "minRam": 4,
    "maxRam": 6,
    "worldBackupUrl": "https://github.com/vctorfarias/minecraft-server-01",
    "worldLogUrl": "https://github.com/vctorfarias/minecraft-log-1",
    "worldName": "minecraft-server-01",
    "logName": "minecraft-log-1"
}}""")

def download_world():
    os.system(f"git clone {world_backup_url}")


def download_log():
    os.system(f"git clone {world_log_url}")


def pull_world():
    os.chdir(world_name)
    os.system("git pull")
    os.chdir("..")


def pull_log():
    os.chdir(log_name)
    os.system("git pull")
    os.chdir("..")


def write_to_log(action):
    pull_log()
    os.chdir(log_name)

    log_date = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    with open("latest.txt", "a") as file:
        file.write(f"\n{author} - {log_date} - {action}")
        file.close()
    
    os.system("git add *")
    os.system(f"git commit -m '{author}'")
    os.system("git push")
    os.chdir("..")


def get_owner():
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


def set_owner(new_owner):
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
    if not os.path.exists(f"{world_name}") or len(os.listdir(f"{world_name}")) == 0:
        download_world()
    else:
        pull_world()
    if not os.path.exists(f"{log_name}") or len(os.listdir(f"{log_name}")) == 0:
        download_log()
    else:
        pull_log()

    os.chdir(world_name)
    try:
        os.system(f"java -Xmx{max_ram}G -Xms{min_ram}G -jar server.jar nogui")
    except KeyboardInterrupt: # Ctrl + C
        print("\nfechando o programa.")
    os.chdir("..")
    push_world()


def clean_up():
    answer = input("Tem certeza que quer deletar o mundo local? [Tenho absoluta certeza/n]")
    if answer == "Tenho absoluta certeza":
        if os.path.exists(world_name):
            shutil.rmtree(world_name)  # Remove o diretório e todo o seu conteúdo
            print(f"O mundo '{world_name}' foi removido com sucesso.")
        else:
            print(f"O mundo não existe")


def push_world():
    os.chdir(world_name)
    os.system("git add *")
    os.system(f"git commit -m'{author}'")
    os.system("git push")
    os.chdir("..")

def push_log():
    os.chdir(log_name)
    os.system("git add *")
    os.system(f"git commit -m '{author}'")
    os.system("git push")
    os.chdir("..")

def show_help():
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
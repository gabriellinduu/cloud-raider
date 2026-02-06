import discord
from discord.ext import commands
from discord import app_commands
import os
import json
from colorama import init, Fore, Style

init(autoreset=True)

def save_token(token):
    with open("token.json", "w") as file:
        json.dump({"TOKEN": token}, file)

def load_token():
    try:
        with open("token.json", "r") as file:
            data = json.load(file)
            return data.get("TOKEN")
    except FileNotFoundError:
        print(Fore.RED + "Erro: token.json não encontrado")
        return None
    except json.JSONDecodeError:
        print(Fore.RED + "Erro: Formato JSON inválido em token.json.")
        return None

def display_logo():
    logo = '''
 ██████╗██╗      ██████╗ ██╗   ██╗██████╗     ██████╗  █████╗ ██╗██████╗ ███████╗██████╗ 
██╔════╝██║     ██╔═══██╗██║   ██║██╔══██╗    ██╔══██╗██╔══██╗██║██╔══██╗██╔════╝██╔══██╗
██║     ██║     ██║   ██║██║   ██║██║  ██║    ██████╔╝███████║██║██║  ██║█████╗  ██████╔╝
██║     ██║     ██║   ██║██║   ██║██║  ██║    ██╔══██╗██╔══██║██║██║  ██║██╔══╝  ██╔══██╗
╚██████╗███████╗╚██████╔╝╚██████╔╝██████╔╝    ██║  ██║██║  ██║██║██████╔╝███████╗██║  ██║
 ╚═════╝╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
                       TOOL CREATE FOR gabriel_bonitu'''
    os.system('cls' if os.name == 'nt' else 'clear')  
    print(Fore.BLUE + logo)

def display_status(connected):
    if connected:
        print(Fore.GREEN + "Status: Conectado")
    else:
        print(Fore.RED + "Status: Desconectado")

def token_management():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console before showing token options
    print(Fore.RED + "1. Novo Token")
    print(Fore.RED + "2. Usar token definido")
    
    # Adding an empty line between options and the input prompt
    print()

    choice = input(Fore.RED + "Cloud Raider: ")

    if choice == "1":
        new_token = input(Fore.GREEN + "Novo Token: ")
        save_token(new_token)
        print(Fore.GREEN + "Token definido com sucesso!")
        return new_token
    elif choice == "2":
        token = load_token()
        if token:
            print(Fore.GREEN + f"Token carregado: {token}")
            return token
        else:
            print(Fore.RED + "Token não encontrado.")
            return None
    else:
        print(Fore.RED + "Escolha inválida. Tente novamente.")
        return None

intents = discord.Intents.default()
intents.messages = True  # Enable access to message content
intents.message_content = True  # Enable access to message content specifically
intents.typing = False  # Disable typing intent (optional)
intents.presences = False  # Disable presence updates (optional)

bot = commands.Bot(command_prefix="!", intents=intents)

class SpamButton(discord.ui.View):
    def __init__(self, message):
        super().__init__()
        self.message = message

    @discord.ui.button(label="Enviar", style=discord.ButtonStyle.red)
    async def spam_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()  
        for _ in range(5):  
            await interaction.followup.send(self.message)  

@bot.tree.command(name="raid", description="Envie a mensagem e gere o botão 'Enviar'")
@app_commands.describe(message="A mensagem que você quer spamar")
async def spamraid(interaction: discord.Interaction, message: str):
    view = SpamButton(message)
    await interaction.response.send_message(f"{message}", view=view, ephemeral=True)  

@bot.event
async def on_ready():
    display_logo()
    display_status(True)
    print(Fore.GREEN + f"🤖 Bot conectado como {bot.user}")
    print(Fore.GREEN + f"🆔 Id do bot {bot.user.id}")
    print(Fore.GREEN + f"💻 Bot desenvolvido pela Cloud Applications")

    try:
        await bot.tree.sync()  
        print(Fore.GREEN + "✅ Comandos sincronizados com sucesso!")
    except Exception as e:
        display_status(False)
        print(Fore.RED + f"Erro durante a sincronização: {e}")

if __name__ == "__main__":
    TOKEN = token_management()
    if TOKEN:
        try:
            bot.run(TOKEN)
        except discord.errors.LoginFailure:
            print(Fore.RED + "Impossivel conectar ao token. Por favor verifique se o token é válido e tente novamente.")
            input(Fore.YELLOW + "Clique Enter para voltar ao o menu pincipal...")
            TOKEN = token_management()  # Restart the token selection process
            if TOKEN:
                bot.run(TOKEN)  # Run again with the new token
        except Exception as e:
            print(Fore.RED + f"Erro inesperado ocorreu: {e}")
            input(Fore.YELLOW + "Clique Enter para voltar ao menu principal...")
            TOKEN = token_management()  # Restart the token selection process
            if TOKEN:
                bot.run(TOKEN)  # Run again with the new token
    else:
        print(Fore.RED + "❌ Erro: Não foi possível carregar ou definir um token.")

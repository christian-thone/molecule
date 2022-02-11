import discord, os
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv('.env')

class Molecule():
    def __init__(self) -> None:
        super().__init__()
        self.Client = commands.Bot(command_prefix=".")

    def start(self, token):
        self.Client.run(token)

    async def load_modules(self, path):
        directory = os.listdir(path)

        for file in directory:
            if (file[-3:] == ".py"):
                print(f"Loading: '{file[:-3]}'")
                self.Client.load_extension(f"Modules.{file[:-3]}")
                print(f"Module: '{file}' loaded")



molecule = Molecule()

@molecule.Client.event
async def on_ready():
    await molecule.load_modules("./Modules/")
    """ conn = molecule.get_db("C:\\Users\\insom\\Desktop\\Molecule\\Databases\\moderation.db")
    conn.close() """
    await molecule.Client.change_presence(activity=discord.Game('with puppies'))


molecule.start(os.getenv('MOLECULE_TOKEN'))
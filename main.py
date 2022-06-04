try:
    import os
    import sys
    import time
    import discord
    import threading

    from httpx import Client
    from discord.ext import commands
except ImportError:
    os.system('cls & pip install -r requirements.txt')

client = commands.Bot(
    command_prefix = "!",
    intents = discord.Intents.all()
)

client.remove_command("help")

class functions(object):

    def __init__(self, token, guild, bot) -> None:
        self._reason = "tokyo!"
        self.bot = bot
        self.token = token
        self.guild = guild

        if self.bot in ("y", "Y"):
            self.headers = {"Authorization": f"Bot {self.token}"}
        elif self.bot in ("n", "N"):
            self.headers = {"Authorization": self.token}
        else:
            pass

    def clear() -> None:
        if sys.platform.startswith("win"):
            os.system("cls")
        else:
            os.system("clear")

    def massban_worker(self, session, id) -> None:
        try:
            s = session.put(f"https://discord.com/api/v9/guilds/{self.guild}/bans/{id}", headers = self.headers)
            if s.status_code in (200, 201, 204, 205, 206, 207, 208, 209, 210):
                print(f"\u001b[38;5;20m[\033[37m+\u001b[38;5;20m] \033[37m-> banned member\u001b[38;5;20m: \033[37m{id}")
            elif s.status_code == 429:
                print(f"\u001b[38;5;20m[\033[37m+\u001b[38;5;20m] \033[37m-> ratelimited for\u001b[38;5;20m: \033[37m{s.json()['retry_after']}")
            elif "Missing Permissions" in s.text:
                print(f"\u001b[38;5;20m[\033[37m+\u001b[38;5;20m] \033[37m-> couldnt ban\u001b[38;5;20m: \033[37m{id}")
            else:
                print(f"\u001b[38;5;20m[\033[37m+\u001b[38;5;20m] \033[37m-> failed to ban\u001b[38;5;20m: \033[37m{id}")
        except Exception:
            pass

    @staticmethod
    async def scrape_request(guildobj) -> None:
        if os.path.exists("data/users.txt"):
            os.remove("data/users.txt") 
        else:
            None

        mc = 0
        with open("data/users.txt", "a") as f:
            for member in guildobj.members:
                mc += 1
                f.write(f"{str(member.id)}\n")

        print(f"\u001b[38;5;20m-> \033[37msuccessfully scraped\u001b[38;5;20m; \033[37m{mc} members\u001b[38;5;20m! \033[37m")

os.system('cls; clear && mode 80, 20 & title tokyo - login/~')
token = input(f"\u001b[38;5;20m-> \033[37mtoken\u001b[38;5;20m; \033[37m")
functions.clear()
guild = int(input(f"\u001b[38;5;20m-> \033[37mguild\u001b[38;5;20m; \033[37m"))
functions.clear()
bot = input(f"\u001b[38;5;20m-> \033[37mbot -> \u001b[38;5;20m[\033[37my\u001b[38;5;20m/\033[37mn\u001b[38;5;20m]\033[37m; ").lower()
functions.clear()

class main:

    def __init__(self) -> None:
        self.gui = f"\u001b[38;5;20m[\033[37m1\u001b[38;5;20m] \033[37m-> massban\n\u001b[38;5;20m[\033[37m2\u001b[38;5;20m] \033[37m-> scrape"
        self.instance = functions(token, guild, bot)
        guildobj = None

    @client.event
    async def on_ready() -> None:
        global guildobj
        guildobj = client.get_guild(guild)
        await main().menu()

    async def menu(self) -> None:
        os.system('cls; clear && mode 80, 20 & title tokyo - menu/~')
        print(f"{self.gui}\n")

        cmd = input(f"\u001b[38;5;20m-> \033[37mcommand\u001b[38;5;20m; \033[37m")

        if cmd in ['1', '01', 'massban']:

            i = []
            session = Client()
            self._ids = open("data/users.txt").read().splitlines()
            for id in self._ids:
                t = threading.Thread(target = self.instance.massban_worker, args = (session, id, ))
                i.append(t)
                t.start()
            for t in i:
                try:
                    t.join()
                except Exception:
                    pass
            time.sleep(2)
            await main().menu()

        elif cmd in ['2', '02', 'scrape']:

            await functions.scrape_request(guildobj)
            time.sleep(1.5)
            await main().menu()

    def run(self):
        try:
            if bot in ("y", "Y"):
                client.run(
                    token
                )
            else:
                client.run(
                    token,
                    bot = False
                )
        except Exception:
            pass

if __name__ == "__main__":
    j = main()
    j.run()
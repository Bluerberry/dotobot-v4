import logging as log
from os import getenv

import discord
from discord.ext import commands
from dotenv import load_dotenv
from pretty_help import PrettyHelp


log.basicConfig(
    level=log.INFO,
    format='%(asctime)s [%(levelname)8s] @ %(name)-18s: %(message)s',
    datefmt='%d/%m/%y %H:%M:%S',
    filename='storage/discord.log',
    filemode='w',
    encoding='utf-8'
)
log.getLogger('discord').setLevel('WARNING')


load_dotenv()
bot = commands.Bot(command_prefix=getenv('PREFIX'), intents=discord.Intents.all())


@bot.before_invoke
async def logging(ctx: commands.Context) -> None:
    """
    Logs all commands called to the bot.

    :param ctx: The context in which the command was called.
    """
    if not ctx.invoked_subcommand:
        command_log = log.getLogger('command.invoke')
        if log.root.level != log.DEBUG:
            command_log.info(f"{ctx.author.name.ljust(16,' ')} | " +
                             f"called: {str(ctx.command)}")
        else:
            command_log.debug(f"{ctx.author.name.ljust(16,' ')} | " +
                              f"called: {str(ctx.command).ljust(12,' ')} | " +
                              f"with: {ctx.message.content}")


@bot.event
async def on_ready(self) -> None:
    """
    Runs code to be triggered on start up.
    Displays login message to terminal and sets up the help message.
    """
    log.info(f'Logged in as {self.bot.user}')
    ending_note = f'Powered by {self.bot.user.name}\nFor command {{help.clean_prefix}}{{help.invoked_with}}'
    self.bot.help_command = PrettyHelp(
        ending_note=ending_note,
        color=discord.Color.from_rgb(255, 0, 0),
        no_category='System'
    )

if __name__ == '__main__':
    bot.run(getenv('TOKEN'))

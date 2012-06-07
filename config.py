admins = set(["joshz"])  # Users that can send privileged commands to the bot.
prefix = "&"  # Prepends all bot commands; bot only responds to commands with prefix at the start.
nick = "noFifthGlyphTest" 
userName = "joshzNoFifthBot"
hostName = "joshz"
realName = "joshz"
server = "irc.foonetic.net"  # Server to connect to
password = ""  # Password to use on that server, if any (blank password means no authentication!)

def botIdentify(con, botNick=""):
    '''Identify to the network as a bot.
    Note that network policies bots and bot identification vary.
    Follow your network's rules.

    '''
    con.sendMessage("MODE " + nick + " +B")


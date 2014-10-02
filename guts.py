# hot-reloadable internals

cmd_prefix = '%'

def show_help(bot, user, chan, args):
    bot.say(chan, 'Supported commands:')
    bot.say(chan, '  ' + ' '.join(
        '%s%s' % (cmd_prefix, k) for k in cmds.keys()))

def hi(bot, user, chan, args):
	bot.say(chan, 'Hi!')

cmds = {
    'help': show_help,
	'hi': hi,
}

#!/usr/bin/env python

from __future__ import print_function

from twisted.internet import reactor, protocol, inotify
from twisted.words.protocols import irc
from twisted.python import filepath

import json
from datetime import date

import guts

nickname = 'zbot'
channel = '#openra'
bot = None

class Bot(irc.IRCClient):
    @property
    def nickname(self):
        return self.factory.nickname

    def signedOn(self):
        print('Signed on as %s.' % self.nickname)
        self.join(self.factory.channel)
        global bot
        bot = self

    def joined(self, channel):
        print('Joined %s.' % channel)

    def say(self, channel, msg):
        if type(msg) is unicode:
            msg = msg.encode('utf-8')
        irc.IRCClient.say(self, channel, msg)

    def privmsg(self, user, channel, msg):
        if not msg.startswith(guts.cmd_prefix):
            return

        parts = msg[len(guts.cmd_prefix):].split(' ')
        cmd = guts.cmds.get(parts[0])

        if not cmd:
            self.say(channel, 'Eh?')
            return

        cmd(self, user, channel, parts[1:])


class BotFactory(protocol.ClientFactory):
    protocol = Bot

    def __init__(self, channel, nickname=nickname):
        self.channel = channel
        self.nickname = nickname

    def clientConnectionLost(self, connector, reason):
        print('Connection lost. Reason: %s' % reason)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed. Reason: %s' % reason)
        connector.connect()

def reload_guts(ignored, fp, mask):
    if fp == filepath.FilePath('guts.py'):
        reload(guts)
        if bot:
            bot.say(channel, 'brain transplant complete.')


if __name__ == '__main__':
    reactor.connectTCP('irc.freenode.org', 6667, BotFactory(channel))
    notifier = inotify.INotify()
    notifier.startReading()
    notifier.watch(filepath.FilePath('.'), callbacks=[reload_guts], mask=8)
    reactor.run()

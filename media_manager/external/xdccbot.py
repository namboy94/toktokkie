#!/usr/bin/python
"""
XDCC file downloader

Hacked together by Gregory Eric Sanderson Turcot Temlett MacDonnell Forbes
Modified by Hermann Krumrey
Requires the python package "twisted"

This script connects to an IRC server and batch downloads files using the XDCC
protocol.

TODO:
 * Manage partial downloads
 * Manage unexpected DCC connections
 * Add optional port to command line

License:

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import sys
import logging as log

try:
    # noinspection PyUnresolvedReferences
    from twisted.words.protocols import irc
    # noinspection PyUnresolvedReferences
    from twisted.internet import reactor, protocol
    # noinspection PyUnresolvedReferences
    from twisted.python import log as twistedlog


    class XdccBot(irc.IRCClient):

        @property
        def nickname(self):
            return self.factory.nickname

        def connection_made(self):
            irc.IRCClient.connection_made(self)
            log.info("Bot connection made")

        def signed_on(self):
            log.info("Bot has signed on")
            self.join(self.factory.channel)

        def joined(self, connected_channel):
            log.info("Bot has joined channel %s" % connected_channel)
            self.process_xdcc_requests()

        def process_xdcc_requests(self):

            xdccmsg = "XDCC SEND #%s"

            if len(self.factory.xdcc_requests) > 0:
                number = self.factory.xdcc_requests.pop(0)
                self.msg(self.factory.xdcc_bot, xdccmsg % str(number))
            else:
                reactor.stop()

        def privmsg(self, user, channel, msg):
            log.info("<%s> %s" % (user, msg))

        def dcc_do_send(self, user, address, port, filename, size, data):

            xdcc_factory = XdccDownloaderFactory(self,
                                                 filename,
                                                 self.factory.destdir,
                                                 (user, self.factory.channel, data))

            if not hasattr(self, 'dcc_sessions'):
                self.dcc_sessions = []
            self.dcc_sessions.append(xdcc_factory)

            reactor.connectTCP(address, port, xdcc_factory)

        def dcc_download_finished(self, filename, success):

            log.info("Download of %s finished. Download status: %s" %
                     (filename, success))
            sys.exit(0)
            # self.process_xdcc_requests()

    class XdccBotFactory(protocol.ClientFactory):

        def __init__(self, irc_channel, irc_nickname, xdcc_bot, xdcc_requests, destdir='.'):
            self.channel = irc_channel
            self.nickname = irc_nickname
            self.destdir = destdir
            self.xdcc_bot = xdcc_bot
            self.xdcc_requests = xdcc_requests

        def clientConnectionLost(self, connector, reason):
            log.warning("Lost connection. Will try to reconnect. reason : %s" % reason)
            connector.connect()

        def buildProtocol(self, addr):
            bot = XdccBot()
            bot.factory = self
            return bot

        def clientConnectionFailed(self, connector, reason):
            log.warning("Connection failed. reason: %s" % reason)
            reactor.stop()

    class XdccDownloader(irc.DccFileReceive):

        notify_block_size = 1024 * 1024

        def __init__( self, filename, filesize=-1, query_data=None, destination_dir='.', resume_offset=0):

            irc.DccFileReceive.__init__( self, filename, filesize, query_data, destination_dir, resume_offset)
            self.bytes_notify = 0

        def is_download_successful(self):
            return self.bytes_received == self.file_size

        def data_received(self, data):
            irc.DccFileReceive.data_received(self, data)
            if self.bytes_received >= self.bytes_notify + self.notify_block_size:

                self.bytes_notify += self.notify_block_size

                log.info("%s is now at %s bytes" % (self.filename, self.bytes_received))
                print("%s is now at %s bytes" % (self.filename, self.bytes_received))

        def connection_lost(self, reason):

            self.file_size = self.file.tell()
            irc.DccFileReceive.connection_lost(self, reason)

            if hasattr(self.factory.client, 'dcc_download_finished'):
                self.factory.client.dcc_download_finished(self.filename, self.is_download_successful())

    class XdccDownloaderFactory(protocol.ClientFactory):

        def __init__(self, client, filename, destdir, query_data):
            self.client = client
            self.query_data = query_data
            self.filename = filename
            self.destdir = destdir

        def buildProtocol(self, addr):
            downloader = XdccDownloader(self.filename,
                                        -1,
                                        self.query_data,
                                        self.destdir)
            downloader.factory = self
            return downloader

        def clientConnectionFailed(self, connector, reason):
            log.warning("connection failed during DCC download. reason: %s" % reason)
            self.client.dcc_sessions.remove(self)

        def clientConnectionLost(self, connector, reason):
            self.client.dcc_sessions.remove(self)

    if __name__ == "__main__":

        if len(sys.argv) != 7:
            print("Usage: %s IRC_SERVER CHANNEL NICKNAME BOTNICKNAME DESTINATION_DIR XDCC_REQUEST ")
            sys.exit(1)

        log.basicConfig(level=log.INFO)

        observer = twistedlog.PythonLoggingObserver()
        observer.start()

        server, channel, nickname, xdccbot, dest_dir = sys.argv[1:6]
        xdccrequests = sys.argv[6:]

        print(server, channel, nickname, xdccbot, xdccrequests)

        factory = XdccBotFactory(channel, nickname, xdccbot, xdccrequests, dest_dir)
        reactor.connectTCP(server, 6667, factory)
        reactor.run()

except ImportError:
    def get_file_loc():
        return __file__

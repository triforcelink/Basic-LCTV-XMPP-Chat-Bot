#Script based on work from:
#https://github.com/benhoff/CHATIMUSMAXIMUS
#http://sleekxmpp.com/getting_started/muc.html

import sleekxmpp
from settings import USER, PASS, BOT_NAME


class MUCBot(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password='', room=None, nick=BOT_NAME):

        super(MUCBot, self).__init__(jid, password)
        if room is None:
            room = '{}@chat.livecoding.tv'.format(jid.user)
        self.room = room
        self.nick = nick
        self.user_list = []
        self._register_plugin_helper() 

        #More on available events: http://sleekxmpp.com/event_index.html
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("groupchat_message", self.muc_message)
        # self.add_event_handler("muc::{}::got_online".format(room), self.muc_online)
        # self.add_event_handler("muc::{}::got_offline".format(room), self.muc_offline)

    def _register_plugin_helper(self):
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0004') # Data Forms
        self.register_plugin('xep_0060') # PubSub
        self.register_plugin('xep_0199', {'keepalive': True, 'frequency': 60}) # XMPP Ping
        self.register_plugin('xep_0045') # MUC

    #Called on bot startup
    def start(self, event):
        self.get_roster()
        self.send_presence()
        self.plugin['xep_0045'].joinMUC(self.room, self.nick, wait=True)

    #Called any time there is a group message
    def muc_message(self, msg):
        if msg['mucnick'] != self.nick:
        	print("Message:", msg['body'])
	
    # #Called for each user in chat, and when new users join.
    # def muc_online(self, presence):
    #     #Add user to self.user_list. For tracking whos online.
    #     if presence['muc']['nick'] not in self.user_list:
    #         self.user_list.append(presence['muc']['nick'])
    #         print("Added user:", presence['muc']['nick'])

    #     #Send hello message to joining user
    #     if presence['muc']['nick'] != self.nick:
    #         self.send_message(mto=presence['from'].bare,
    #         mbody="Welcome, {}!".format(presence['muc']['nick']),
    #         mtype='groupchat')

    # #Gets called when a user leaves chat
    # #Not sure if this actually works
    # def muc_offline(self, presence):
    #     #If user leaves chat, remove them from self.user_list
    #     if presence['muc']['nick'] in self.user_list:
    #         self.user_list.remove(presence['muc']['nick'])
    #         print("Removed user:", presence['muc']['nick'])

    #     #Send bye message to chat
    #     if presence['muc']['nick'] != self.nick:
    #         self.send_message(mto=presence['from'].bare,
    #         mbody="Bye, {}!".format(presence['muc']['nick']),
    #         mtype='groupchat')


if __name__ == '__main__':
    jid = sleekxmpp.JID(local=USER, domain='livecoding.tv', resource='bot')
    xmpp = MUCBot(jid, PASS)

    if xmpp.connect():
    	xmpp.process(block=True)
    	print("Done")
    else:
        print("Unable to connect")
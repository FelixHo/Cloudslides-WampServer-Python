# -*- coding: utf-8 -*
'''
Created on 2014-5-30
For Test Only

@author: Felix
'''
import sys
import json
from twisted.python import log
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.internet.endpoints import clientFromString

from autobahn.twisted import wamp, websocket
from time import sleep



class MyFrontendComponent(wamp.ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        #pageTopic的handler
        #
        def on_event(res):
            print('page change to :'+str(res))
            
        #获取制定会议的页码，并且根据返回的topic订阅
        #
        try:
            self.res = yield self.call(u'rpc.page.currentindex' , 1)
        except Exception as e:
            print("Error: {}".format(e))
        else:
            print("return:"+self.res)          
            result = json.loads(self.res)
            if result['code']=="200":
                print(result['status']+' '+'currentPage:'+str(result['current_page']))
                self.currentIndex = result['current_page']
                self.topic = result['page_topic_uri'] 
                yield self.subscribe(on_event, self.topic)
            else:
                print(result['status'])
        
        #每隔5秒翻一页
        #
        self.page = 1;
        while True:
            self.res = yield self.call(u'rpc.page.setpage',1,self.page)
            result = json.loads(self.res)
            if result['code']=="200":
                self.page+=1
                sleep(5)
            else:
                print(result['status'])
                break
                    

    def onDisconnect(self):
        reactor.stop()
  


if __name__ == '__main__':

    ## 0) start logging to console
    log.startLogging(sys.stdout)

    ## 1) create a WAMP application session factory
    session_factory = wamp.ApplicationSessionFactory()
    session_factory.session = MyFrontendComponent

    ## 2) create a WAMP-over-WebSocket transport client factory
    transport_factory = websocket.WampWebSocketClientFactory(session_factory, \
                                                            debug = False, \
                                                            debug_wamp = False)

    ## 3) start the client from a Twisted endpoint
    client = clientFromString(reactor, "tcp:localhost:9000")
    client.connect(transport_factory)

    ## 4) now enter the Twisted reactor loop
    reactor.run()

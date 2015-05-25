# -*- coding: utf-8 -*
'''
Created on 2014-5-30
MeetingSync PageController for Cloudslides
@author: Felix
'''

import sys

from twisted.python import log
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.internet.endpoints import serverFromString

from autobahn.wamp import router
from autobahn.twisted import wamp, websocket

from pymongo import MongoClient

import json



class PageSyncComponent(wamp.ApplicationSession):
    
    @inlineCallbacks
    def onJoin(self, details):
        
        #获取指定会议的当前页码及会议topic
        #
        def currentIndex(meetingId):
            print("rpc call currentIndex...")
            
            client = MongoClient('localhost', 27017)#init db
            db = client.Cloudslides
            collection = db.meeting
                        
            query = collection.find_one({"id":meetingId})
            
            if query is None:#检查会议是否存在
                
                print('Meeting Not Foud')
                return self.JsonResultForCurrentIndex(404, "Meeting Not Found")
            
            else:
                currentPage = query['current_page_index']
                pageTopicUri = self.PageTopicGenerator(meetingId)
                
                print("return:"+str(currentPage)+"-"+pageTopicUri)
                
                return self.JsonResultForCurrentIndex(200, 'success', currentPage, pageTopicUri)
    
        #设置指定会议的当前页码
        #
        def setPage(meetingId,pageIndex):
            print("rpc call setPage...")
            
            client = MongoClient('localhost', 27017)#init db
            db = client.Cloudslides
            collection = db.meeting
            
            res = collection.update({'id':meetingId},{'$set':{'current_page_index':pageIndex}})
            if res['updatedExisting']: #检查是否更新成功 
                              
                print('pagetopic.meetingid_'+str(meetingId)+' currentPage:'+str(pageIndex))
                self.publish(self.PageTopicGenerator(meetingId),pageIndex)
                
                return self.JsonResultForSetPage(200,'success')
            
            else:
                print('Meeting Not Found')
                return self.JsonResultForSetPage(404, 'Meeting Not Found')
            
              
        yield self.register(currentIndex, u'rpc.page.currentindex')
        yield self.register(setPage, u'rpc.page.setpage')
        
    #currentIndex RPC 返回
    #    
    def JsonResultForCurrentIndex(self,resCode,desc,currentPage=None,pageTopicUri=None):
        result = {
                  "code":str(resCode),
                  "status":desc,
                  "current_page":currentPage,
                  "page_topic_uri":pageTopicUri                  
                  }
        return json.dumps(result)
    
    #setPage RPC 返回
    #
    def JsonResultForSetPage(self,resCode,desc):
        result = {
                  "code":str(resCode),
                  "status":desc
                  }
        return json.dumps(result)
    
    #会议页码topic生成
    #
    def PageTopicGenerator(self,meetingId):
        return u'pagetopic.meetingid_'+str(meetingId)
        
        
if __name__ == '__main__':

    ## 0) start logging to console
    log.startLogging(sys.stdout)

    ## 1) create a WAMP router factory
    router_factory = router.RouterFactory()
 
    ## 2) create a WAMP router session factory
    session_factory = wamp.RouterSessionFactory(router_factory)

    ## 3) Optionally, add embedded WAMP application sessions to the router
    session_factory.add(PageSyncComponent())

    ## 4) create a WAMP-over-WebSocket transport server factory
    transport_factory = websocket.WampWebSocketServerFactory(session_factory, \
                                                            debug = False, \
                                                            debug_wamp = False)

    ## 5) start the server from a Twisted endpoint
    server = serverFromString(reactor, "tcp:9000")
    server.listen(transport_factory)

    ## 6) now enter the Twisted reactor loop
    reactor.run()

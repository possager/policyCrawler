import pymongo
import gridfs
import logging

class gridfsProcessor:
    __instance = {}

    def __init__(self,host="localhost",port=27017,COL="default_policy_COL",DOC="default_policy_DOC",gridfsDB="default_policy_gridfs"):
        self.mongoclient=pymongo.MongoClient(host=host,port=port)
        self.COL=self.mongoclient[COL]
        self.DOC=self.COL[DOC]
        self.fs=gridfs.GridFS(self.COL,gridfsDB)
        self.data_cache=[]

        self.data_cache_len=50


    @classmethod
    def from_setting(cls,host="localhost",port=27017,COL="default_policy_COL",DOC="default_policy_DOC",gridfsDB="default_policy_gridfs",):
        if COL in cls.__instance.values() and DOC in cls.__instance[COL].values():
            return cls.__instance[COL][DOC]
        else:
            if COL not in cls.__instance.values():
                cls.__instance[COL]={}
            cls.__instance[COL][DOC]=gridfsProcessor(host,port,COL,DOC,gridfsDB)
            return cls.__instance[COL][DOC]

    def __putdata_to_cache(self,data, **kwargs):
        _data_cache={
            'data':data,
            'kwargs':kwargs
        }
        self.data_cache.append(_data_cache)

    def __putcache_to_db(self):
        while self.data_cache:
            one_cache_data=self.data_cache.pop()
            self.fs.put(one_cache_data['data'],**one_cache_data['kwargs'])
        print('has successed in putting cache data to gridfs!')


    def __getattr__(self, item):
        if hasattr(self.fs,item):
            if item=="put":
                if len(self.data_cache)<self.data_cache_len:
                    return self.__putdata_to_cache
                else:
                    self.__putcache_to_db()
                    return self.__putdata_to_cache
            return self.fs.__getattribute__(item)
        else:
            raise Exception("gridfs did not support -> %s <- operation!"%item)

    def __del__(self):
        if hasattr(self,"mongoclient"):
            if self.data_cache:
                self.__putcache_to_db()
            self.mongoclient.close()
            print("mongoclient has closed")
        else:
            print("mongoclient did not existed")



if __name__ == '__main__':
    s=gridfsProcessor.from_setting(COL="test1")
    ss=s.from_setting(COL="test2")
    sss=s.from_setting(COL="test1")

    for i in range(51):
        with open('E:\\Data_test\\sayhello_to_girdfs.docx','rb') as fl:
            data=fl.read()
        ss.put(data)
        s.put(data)

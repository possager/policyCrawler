import logging
from logging import handlers
import time
import os




class L_logging:
    def __init__(self,name):
        if not os.path.exists('Log'):
            os.mkdir('Log')
        self.logger=logging.getLogger(name)
        self.formatter= logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger.addHandler(handlers.RotatingFileHandler(maxBytes=1024*1024*10,filename='Log/%s_%s.log'%(name,time.strftime("%Y_%m-%d_%H_%M_%S",time.localtime(time.time())))).setFormatter(self.formatter))
        # self.logger.addHandler(logging.FileHandler(filename='Log/%s_%s.log'%(name,time.strftime("%Y_%m-%d_%H_%M_%S",time.localtime(time.time())))))
        # self.logger.addFilter()
        self.logger.setLevel(logging.INFO)



if __name__ == '__main__':
    logger1=L_logging(name='hello')
    logger1.logger.info(msg='hello')
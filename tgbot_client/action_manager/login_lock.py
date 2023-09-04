'''
定义锁，完成对login前的锁定
'''

import asyncio
class login_lock:
  
    lock = asyncio.Lock()
    
    
    def unlock():
        print('释放锁！！')
        login_lock.lock.release() # 释放锁
        
    async def acquire_lock():
        print('加把锁先！！')
        await login_lock.lock.acquire()

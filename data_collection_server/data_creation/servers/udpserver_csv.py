import SocketServer as socketserver
import time 
import datetime

date=str(datetime.datetime.today()).replace(" ","_").replace("/","_").replace(".","_").replace("-","_").replace(":","_")
exercise='bcurl'

#[spress=Shoulder Press, cpress = Chest Press, jmpjck = Jumping Jack, runip,triext,ovhtri]

testtrain='train'

path='/Users/christopherhedenberg/Documents/Recess/rep_models/data/%s/%s/raw/%s_%s.txt' %(testtrain,exercise,exercise,date)


rep_file=open(path,'w') 
start=time.time()

class MyUDPHandler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        data_out=data.decode("utf-8") +'\n'
        print (data_out)
        rep_file.write(data_out)
        socket.sendto(data.upper(), self.client_address)

if __name__ == "__main__":
    HOST, PORT = "", 8888
    server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()
    

    
    
    
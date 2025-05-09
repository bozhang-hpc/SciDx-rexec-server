import logging
import zmq
import dill
import dxspaces
import rexec.remote_obj

class RExecServer:
    rexec.remote_obj.DSDataObj.ctx = "server"

    def __init__(self, args):
        self.zmq_addr = "tcp://" + args.broker_addr + ":" + args.broker_port
        self.zmq_context = zmq.Context()
        self.zmq_socket = self.zmq_context.socket(zmq.REP)
        self.zmq_socket.connect(self.zmq_addr)
        logging.info(f"Connected to {self.zmq_addr}")
        
        if(args.dspaces_api_addr):
            dspaces_client = dxspaces.DXSpacesClient(args.dspaces_api_addr)
            logging.info("Connected to DataSpaces API.")
            rexec.remote_obj.DSDataObj.dspaces_client = dspaces_client
    
    def fn_recv_exec(self):
        while(True):
            zmq_msg = self.zmq_socket.recv_multipart()
            fn = dill.loads(zmq_msg[0])

            args = dill.loads(zmq_msg[1])

            try:
                ret = fn(*args)
            except Exception as e:
                ret = f"An unexpected error occurred: {e}"

            pret = dill.dumps(ret)

            self.zmq_socket.send(pret)

    def run(self):
        try:
            logging.info(f"Start to receive functions...")
            self.fn_recv_exec()
        except KeyboardInterrupt:
            print("W: interrupt received, stopping rexec server...")
        finally:
            self.zmq_socket.disconnect(self.zmq_addr)
            self.zmq_socket.close()
            self.zmq_context.destroy()
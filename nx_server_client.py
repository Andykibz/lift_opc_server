from opcua import Client, Server
from threading import Thread
import time

class UpdateNodes(object):
    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node, val)

def bridge():
    while True:
        disp_c.set_value( disp_s.get_value() ) # Set Cloud OPC with local values from NX
        lvel_s.set_value( lspd_c.get_value() ) # Set NX's local OPC with valiues from the cloud
        # print(lvel_s.get_value())
        time.sleep(.2)
        

elevator_opc_info = {
    'ep_url'    : "opc.tcp://IntersectWinPC:4840/elevator/pid/",
    'uri'       : "http://thaintersect.com",
}
nx_server_info = {
    "ep_url"    :   "opc.tcp://localhost:4940/nx/pid/",
    "name"      :   "Elevator_OPC_to_NX",
    "uri"       :   "localhost"  
}

if __name__ == "__main__":    

    Elevator_client =  Client( elevator_opc_info['ep_url'] )

    try:
        Elevator_client.connect()
    except Exception as identifier:
        print("Failed to connect to the OPC Server")
        print(identifier)
    else:
        print("Conected to: ", elevator_opc_info['ep_url'])
        # Elevator_client.load_type_definitions()
        

    disp_c =  Elevator_client.get_node("ns=2;i=3")
    aspd_c =  Elevator_client.get_node("ns=2;i=4")
    lspd_c =  Elevator_client.get_node("ns=2;i=5")
    up_c   =  Elevator_client.get_node("ns=2;i=7")

    nx_server = Server()
    nx_server.set_endpoint( nx_server_info['ep_url'] )
    nx_server.set_server_name( nx_server_info['name'] )

    nidx = nx_server.register_namespace(nx_server_info['uri']) 

    objects = nx_server.get_objects_node()

    nx = objects.add_object(nidx, 'NX')

    disp_s = nx.add_variable( nidx, "Displacement", 0.0 )
    disp_s.set_writable()
    avel_s = nx.add_variable(nidx, "Angular_Velocity", 0.0)
    avel_s.set_writable()
    lvel_s = nx.add_variable(nidx, "Linear_Velocity", 0.0)
    lvel_s.set_writable()
    up_s = nx.add_variable(nidx, "GoingUp", True)
    up_s.set_writable()


    # handler = UpdateNodes()
    # sub = Elevator_client.create_subscription(200, handler)
    # handle = sub.subscribe_data_change(myvar)
    # time.sleep(0.1)

    print("Address at: ",nx_server_info['ep_url'])
    coms = Thread(target=bridge )
    nx_server.start()
    coms.start()
    



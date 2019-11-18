from snap7.client import Client as SnapClient
from opcua import Client
from threading import Thread
from snap7.snap7types import areas
from snap7.util import *
import sys,time

try:
    from IPython import embed
except ImportError:
    import code

    def embed():
        vars = globals()
        vars.update(locals())
        shell = code.InteractiveConsole(vars)
        shell.interact()

opc_url = "opc.tcp://localhost:4840/elevator/pid/"
opc_client = Client( opc_url )
opc_uri = "http://thaintersect.com"
updateThread =  True

global plc
plc = SnapClient()

def updates():
    while True:
        # Set Speed Value on OPC Server
        lspd.set_value(get_real( plc.read_area(areas['MK'], 0, 40, 4), 0)) # MD4
        direction = get_bool( plc.read_area( areas['MK'], 0, 20,1 ),0,1 ) # M20.1
        goingup.set_value(direction) 
        # if direction:
        #     lspd.set_value(aspd.get_value() )
        # else:
        #     lspd.set_value( -aspd.get_value() )
            

        
        # Set Distance variable in the PLC
        # disp_reading = plc.read_area(areas['MK'], 0, 0, 4) # read MD0 
        # set_real( disp_reading , 0, disp.get_value() )
        # plc.write_area( areas['MK'], 0, 0, disp_reading )

        # Set Setpoint in PLC PID
        # dest_reading = plc.read_area(areas['MK'], 0, 8, 4) # read MD8/old setpoint/destinateion
        # set_real( dest_reading , 0, dest.get_value() ) # set the destination value
        # plc.write_area( areas['MK'], 0, 8, dest_reading ) # Write Back the new value

        '''
            The next few lines of code assume that a Limit Switch is used for each individual
            floor
        '''
        read_b12 = plc.read_area( areas['MK'],0,12,1 )
        
        set_bool(read_b12,0,0,f_floor.get_value())
        plc.write_area( areas['MK'], 0,12,read_b12 )

        set_bool(read_b12,0,1,s_floor.get_value())
        plc.write_area( areas['MK'], 0,12,read_b12 )

        set_bool(read_b12,0,2,t_floor.get_value())
        plc.write_area( areas['MK'], 0,12,read_b12 )

        time.sleep(.01)

if __name__ == "__main__":
    try:
        opc_client.connect()
    except Exception as identifier:
        print("OPCUA Error:")
        print(identifier)
    else:
        opc_client.load_type_definitions()
        root = opc_client.get_root_node()
        objects = opc_client.get_objects_node()
        idx = opc_client.get_namespace_index(opc_uri)

        obj = root.get_child(["0:Objects", "{}:PLC_S71200".format(idx)])

        # dest =  root.get_child(["0:Objects", "{}:PLC_S71200".format(idx), "{}:Destination".format(idx)])
        dest = opc_client.get_node("ns=2;i=6")
        # disp = root.get_child(["0:Objects", "{}:PLC_S71200".format(idx), "{}:Displacement".format(idx)])
        disp = opc_client.get_node("ns=2;i=3")

        # spd = root.get_child(["0:Objects", "{}:PLC_S71200".format(idx), "{}:Speed".format(idx)])
        aspd = opc_client.get_node("ns=2;i=4")
        lspd = opc_client.get_node("ns=2;i=5")

        f_floor = opc_client.get_node("ns=2;i=13")
        s_floor = opc_client.get_node("ns=2;i=14")
        t_floor = opc_client.get_node("ns=2;i=15")

        goingup = opc_client.get_node("ns=2;i=7")    

        try:
            plc.connect('192.168.0.1', 0, 1)
            plc.get_connected()
        except Exception as msg:
            print(msg)
            sys.exit()
        else:
            t = Thread(target=updates,args=() )
            t.start()
            embed()
            



        

    
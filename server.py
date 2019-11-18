from opcua import Server, ua

try:
    from IPython import embed
except ImportError:
    import code

    def embed():
        myvars = globals()
        myvars.update(locals())
        shell = code.InteractiveConsole(myvars)
        shell.interact()

def findAvg(parent, sumVal, num):
    return sumVal/num



if __name__ == "__main__":
    server = Server()
    # server.set_endpoint("opc.tcp://0.0.0.0:4840/elevator/pid/")
    server.set_endpoint("opc.tcp://0.0.0.0:4840/elevator/pid/")

    server.set_server_name("PID Controlled Elevator")

    uri = "http://thaintersect.com"
    idx = server.register_namespace(uri) 

    objects = server.get_objects_node()

    # Declare PLC object 
    plc =  objects.add_object(idx,"PLC_S71200")

    # Declare MCU object 
    mcu =  objects.add_object(idx,"MCU")

    '''
        Definition of OPC Server Variables
    '''
    disp = mcu.add_variable(idx, "Displacement",0.0 )
    disp.set_writable()
    avel = mcu.add_variable(idx, "Angular_Velocity", 0.0)
    avel.set_writable()
    lvel = mcu.add_variable(idx, "Linear_Velocity", 0.0)
    lvel.set_writable()
    
    up = plc.add_variable(idx, "GoingUp", True, ua.VariantType.Boolean)
    up.set_writable()

    dest = plc.add_variable(idx, "Setpoint", 0.0)
    dest.set_writable()

    motion = plc.add_variable(idx, "InMotion", False, ua.VariantType.Boolean)
    motion.set_writable()

    curFloor = plc.add_variable(idx, "Current_Floor",1 , ua.VariantType.Int16)
    curFloor.set_writable()

    mcall1 = plc.add_variable(idx, "Call_First_Floor", False, ua.VariantType.Boolean)
    mcall1.set_writable()
    mcall2 = plc.add_variable(idx, "Call_Second_Floor", False, ua.VariantType.Boolean)
    mcall2.set_writable()
    mcall0 = plc.add_variable(idx, "Call_Third_Floor", False , ua.VariantType.Boolean)
    mcall0.set_writable()

    LS1 = plc.add_variable(idx, "First_Floor", False, ua.VariantType.Boolean)
    LS1.set_writable()
    LS2 = plc.add_variable(idx, "Second_Floor", False, ua.VariantType.Boolean)
    LS2.set_writable()
    LS3 = plc.add_variable(idx, "Third_Floor", False , ua.VariantType.Boolean)
    LS3.set_writable()

    # myobj = objects.add_object(idx, "MyObject")
    avg_func = mcu.add_method(idx, "Find Average", findAvg, [ua.VariantType.Int64], [ua.VariantType.Boolean])


    print("Address at: opc.tcp://localhost:4840/elevator/pid/")
    server.start()
    # embed()



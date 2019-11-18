from opcua.ua import VariantType
# Define opc vars that will be affected by the MCU
mcu_vars = {
    'displacement'  :   {
        'name'  :   "Displacement",
        'type'  :   VariantType.Int16,
        'value' :   0,
    },
    'avel'         :   {
        'name'  :   "Angular_Velocity",
        'type'  :   VariantType.Int16,
        'value' :   0,
    },
    'lvel'         :   {
        'name'  :   "Linear_Velocity",
        'type'  :   VariantType.Int16,
        'value' :   0,
    }
}

plc_vars = {
    'dir'   : {
        'name'  :   "Up",
        'type'  :   VariantType.Boolean,
        'value' :   True
    },
    'motion'    : {
        'name'  :   "InMotion",
        'type'  :   VariantType.Boolean,
        'value' :   False
    },
    'curFloor'  : {
        'name'  :   "Current Floor",
        'type'  :   VariantType.Int16,
        'value' :   0
    }
}
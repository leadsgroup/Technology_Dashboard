
from . import * 

def generate_Energy_X_aircraft_flight_ops_panel(US_Temperature_F): 
    BDL_flight_ops_aircraft_L_D                         = select_flight_ops_BDL_aircraft_L_D() 
    BDL_flight_ops_aircraft_weight                      = select_flight_ops_BDL_aircraft_weight() 
    BDL_aircraft_max_power                              = select_BDL_aircraft_max_power()     
    BDL_flight_ops_batt_mass_frac                       = select_flight_ops_BDL_batt_mass_frac()   
    BDL_flight_ops_month                                = select_flight_ops_month_BDL(US_Temperature_F)
    BDL_flight_ops_fleet_adoption                       = select_flight_ops_BDL_fleet_adoption() 
    BDL_aircraft_system_voltage                         = select_BDL_system_voltage() 
    BDL_propulsive_efficiency                           = select_BDL_propulsive_efficiency()  
    BDL_cost_of_electricity                             = select_BDL_cost_of_electricity()
    
    flight_ops_aircraft_panel = dbc.Card([
                                        BDL_flight_ops_aircraft_weight, 
                                        BDL_flight_ops_aircraft_L_D,
                                        BDL_aircraft_max_power,
                                        BDL_propulsive_efficiency,
                                        BDL_flight_ops_batt_mass_frac,
                                        BDL_aircraft_system_voltage, 
                                        BDL_flight_ops_fleet_adoption,
                                        BDL_flight_ops_month,
                                        BDL_cost_of_electricity],body=True,)   
    return  flight_ops_aircraft_panel

def generate_Energy_X_battery_panel():    
    BDL_cell_voltage                                    = select_BDL_max_cell_voltage()   
    BDL_cell_capacity                                   = select_BDL_max_cell_capacity()  
    BDL_cell_max_C                                      = select_BDL_max_cell_max_C()  
    BDL_cell_specific_energy                            = select_BDL_specific_energy()  
    BDL_cell_temperature_range                          = select_BDL_temperature_range()            
    
    flight_ops_aircraft_panel = dbc.Card([    
                                        BDL_cell_capacity,
                                        BDL_cell_voltage,      
                                        BDL_cell_max_C,          
                                        BDL_cell_specific_energy,
                                        BDL_cell_temperature_range],body=True,)   
    return  flight_ops_aircraft_panel
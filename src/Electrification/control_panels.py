
from . import * 

def generate_battery_metrics_panel(Commercial_Batteries):  
    
    battery_brand_metrics      = select_battery_brand_metrics(Commercial_Batteries)
    battery_chemistry_metrics  = select_battery_chemistry_metrics(Commercial_Batteries)
    battery_x_axis_metrics     = select_battery_x_axis_metrics(Commercial_Batteries)   
    battery_y_axis_metrics     = select_battery_y_axis_metrics(Commercial_Batteries)     

    battery_metrics_panel = dbc.Card([battery_brand_metrics,
                                        battery_chemistry_metrics,
                                        battery_x_axis_metrics,
                                        battery_y_axis_metrics, 
                                        ],body=True,)

    return battery_metrics_panel


def generate_motor_metrics_panel(Electric_Motor_Development):  
    
    motor_manfacturers_metrics = select_motor_manfacturers_metrics(Electric_Motor_Development)
    motor_type_metrics         = select_motor_type_metrics(Electric_Motor_Development)
    motor_x_axis_metrics       = select_motor_x_axis_metrics(Electric_Motor_Development)   
    motor_y_axis_metrics       = select_motor_y_axis_metrics(Electric_Motor_Development)     

    motor_metrics_panel = dbc.Card([motor_manfacturers_metrics,
                                        motor_type_metrics,
                                        motor_x_axis_metrics,
                                        motor_y_axis_metrics, 
                                        ],body=True,)

    return motor_metrics_panel

def generate_battery_comparison_panel(Commercial_Batteries):

    battery_1_option         = select_battery_1(Commercial_Batteries) 
    battery_2_option         = select_battery_2(Commercial_Batteries) 
    battery_3_option         = select_battery_3(Commercial_Batteries) 
    battery_comparison_panel = dbc.Card([battery_1_option,battery_2_option,battery_3_option], body=True,) 
    
    return battery_comparison_panel   

 
def generate_battery_development_panel(Battery_Development):   
    battery_industry_dev_panel  = select_battery_industry_dev_panel(Battery_Development)
    battery_type_dev_panel      = select_battery_type_dev_panel(Battery_Development)      
    battery_development_panel   = dbc.Card([battery_industry_dev_panel,
                                        battery_type_dev_panel],body=True,)

    return battery_development_panel 

def generate_flight_ops_aircraft_panel(Commercial_Batteries,US_Temperature_F): 
    flight_ops_electric_aircraft                    = select_flight_ops_electric_aircraft()   
    flight_ops_electric_aircraft_batt_mass_frac     = select_flight_ops_electric_aircraft_batt_mass_frac()   
    flight_ops_time_of_year                         = select_flight_ops_month_electric_aircraft(US_Temperature_F)
    flight_ops_fleet_adoption                       = select_flight_ops_electric_fleet_adoption() 
    electric_aircraft_system_voltage                = select_electric_aircraft_system_voltage() 
    electric_aircraft_propulsive_efficiency         = select_electric_aircraft_propulsive_efficiency() 
    electric_aircraft_battery                       = select_flight_ops_electric_aircraft_battery(Commercial_Batteries) 
    cost_of_electricity                             = select_cost_of_electricity()
    
    flight_ops_aircraft_panel = dbc.Card([flight_ops_electric_aircraft,
                                        electric_aircraft_battery, 
                                        flight_ops_electric_aircraft_batt_mass_frac,
                                        electric_aircraft_system_voltage,
                                        electric_aircraft_propulsive_efficiency,
                                        cost_of_electricity,
                                        flight_ops_fleet_adoption,
                                        flight_ops_time_of_year],body=True,)   
    return  flight_ops_aircraft_panel
 

from . import * 

def generate_saf_metrics_panel(Commercial_SAF):  
    
    saf_process            = select_saf_process(Commercial_SAF)
    saf_feedstock          = select_saf_feedstock(Commercial_SAF)
    saf_x_axis_metrics     = select_saf_x_axis_metrics(Commercial_SAF)   
    saf_y_axis_metrics     = select_saf_y_axis_metrics(Commercial_SAF)   
    saf_metrics_panel = dbc.Card([saf_process,
                                        saf_feedstock,
                                        saf_x_axis_metrics,
                                        saf_y_axis_metrics, 
                                        ],body=True,)

    return saf_metrics_panel

 
def generate_saf_development_panel(Commercial_SAF):   
    saf_sector_dev_panel    = select_saf_sector_dev_panel(Commercial_SAF)
    saf_process_panel       = select_saf_process_dev_panel(Commercial_SAF)      
    saf_development_panel   = dbc.Card([saf_sector_dev_panel,
                                        saf_process_panel],body=True,)

    return saf_development_panel  

def generate_saf_flight_ops_fuel_panel(Commercial_SAF):
    saf_selection_1, saf_selection_2    = select_fuels_list(Commercial_SAF)  
    saf_flight_ops_fuel_panel= dbc.Card( [ 
            dbc.Row( [ 
                    dbc.Col([saf_selection_1], width=6), 
                    dbc.Col([saf_selection_2] , width=6), 
                ]),              
        ],body=True,className="border-0 bg-transparent") 
    
    return  saf_flight_ops_fuel_panel
  
def generate_saf_flight_ops_states_panel(): 
    States_1,States_2,States_3,States_4,States_5,States_6 = select_saf_feedstock_states() 
    
    saf_flight_ops_states_panel= dbc.Card( [ 
            dbc.Row( [ 
                    dbc.Col([States_1], width=2), 
                    dbc.Col([States_2], width=2), 
                    dbc.Col([States_3], width=2), 
                    dbc.Col([States_4], width=2), 
                    dbc.Col([States_5], width=2), 
                    dbc.Col([States_6], width=2), 
                ] )            
        ],body=True, className="border-0 bg-transparent")  
    return  saf_flight_ops_states_panel
    
 

from . import * 
 
 
#def generate_h2_development_panel(Hydrogen):   
    #h2_sector_dev_panel    = select_h2_sector_dev_panel(Hydrogen)
    #h2_process_panel       = select_h2_process_dev_panel(Hydrogen)      
    #h2_development_panel   = dbc.Card([h2_sector_dev_panel,
                                        #h2_process_panel],body=True,)

    #return h2_development_panel  

def generate_h2_flight_ops_fuel_panel(Hydrogen):
    h2_selection_1, h2_selection_2    = select_h2_list(Hydrogen)  
    h2_flight_ops_fuel_panel= dbc.Card( [ 
            dbc.Row( [ 
                    dbc.Col([h2_selection_1], width=6), 
                    dbc.Col([h2_selection_2] , width=6), 
                ]),              
        ],body=True,className="border-0 bg-transparent") 
    
    return  h2_flight_ops_fuel_panel 
    
 
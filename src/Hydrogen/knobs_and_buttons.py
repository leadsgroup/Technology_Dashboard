from dash import html, dcc  
import dash_bootstrap_components as dbc  


# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Panel 2 
# ---------------------------------------------------------------------------------------------------------------------------------------------------  
#def select_h2_sector_dev_panel(Hydrogen):
    #All = ['All']
    #feedstock_list = All + list(Hydrogen['Feedstock'][1:].unique())
    #h2_industry = html.Div(
        #[
            #dbc.Label("Select h2 Feedstock"), 
            #dcc.Dropdown(feedstock_list,
                #value = 'All',
                #placeholder = 'All', 
                #disabled = False,
                #clearable=False,
                #style = {'display': True, 'color': 'black'},
                #id="h2_feedstock_sector",   
            #),
        #],
        #className="mb-4",
    #) 
    #return h2_industry

#def select_h2_process_dev_panel(Hydrogen): 
    #All = ['All']
    #process_list = All +   list(Hydrogen['Process'][1:].unique())
    #h2_type  = html.Div(
        #[
            #dbc.Label("Select h2 Production Process"),
            #dcc.Dropdown(process_list,
                #value = 'All',
                #placeholder = 'All', 
                #disabled = False,
                #clearable=False,
                #style = {'display': True, 'color': 'black'},
                #id="h2_process_sector",
            #),
        #],
        #className="mb-4",
    #) 
    #return h2_type
 
# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Panel  
# ---------------------------------------------------------------------------------------------------------------------------------------------------  
def select_h2_list(Hydrogen):
    h2_list_1 = list(Hydrogen["H2 Fuel Name"])[:13]
    h2_list_2 = Hydrogen["H2 Fuel Name"][13:]
    h2_selection_1 = html.Div( [ dcc.Checklist(options=h2_list_1 , value=h2_list_1[0:3],
                                                id="h2_selection_list_1", ), ],className="mb-4", )  
    h2_selection_2 = html.Div( [ dcc.Checklist(options=h2_list_2 , value=h2_list_2[0:2],
                                                id="h2_selection_list_2", ), ], className="mb-4",) 
    return h2_selection_1, h2_selection_2   
 
def select_h2_fleet_adoption(): 
    fleet_adoption = html.Div(
        [
            dbc.Label("Fleet Adoption"),
            dcc.Slider(0, 100, 10,
                value=20,
                id="h2_percent_adoption", 
            ),
        ],
        className="mb-4",
    )
    return  fleet_adoption 


def select_h2_airports(): 
    airport_names = [" Top 5 Airports"," Top 10 Airports"," Top 20 Airports", " Top 50 Airports",  " All Airports"]
    airpots = html.Div(  [  dbc.Label("Select Hydrogen Airport Hubs"), dcc.RadioItems( options = airport_names, value   = " Top 10 Airports", 
                           id="h2_airports",  ),  ], className="mb-4", )   
    return airpots

def select_h2_cost(): 
    h2_cost = html.Div(
        [
            dbc.Label("Hydrogen Cost ($/gal)"),
            dcc.Slider(2, 20, 2,
                value=8,
                id="h2_dollars_per_gal", 
            ),
        ],
        className="mb-4",
    )
    return h2_cost

def select_h2_altitude(): 
    h2_alt = html.Div(
        [
            dbc.Label("Cruise Altitude (ft)"),
            dcc.Slider(15000, 35000, 5000,
                value=35000,
                id="h2_cruise_alt", 
            ),
        ],
        className="mb-4",
    )
    return h2_alt


def select_h2_vol_fraction(): 
    h2_volume = html.Div(
        [
            dbc.Label("Fuselage Cabin Volume Fraction"),
            dcc.Slider(5, 50, 5,
                value=15,
                id="h2_volume", 
            ),
        ],
        className="mb-4",
    )
    return h2_volume

def select_h2_engine_SFC(): 
    h2_engine_SFC = html.Div(
        [
            dbc.Label("Hydrogen Engine SFC"),
            dcc.Slider(0.1, 0.5, 0.1,
                value=15,
                id="h2_SFC", 
            ),
        ],
        className="mb-4",
    )
    return h2_engine_SFC
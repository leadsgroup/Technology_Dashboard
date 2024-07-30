from dash import html, dcc  
import dash_bootstrap_components as dbc  

# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Panel 1 
# ---------------------------------------------------------------------------------------------------------------------------------------------------  
def select_saf_process(Commercial_SAF):
    All = ['All']
    process_list = All + list(Commercial_SAF['Process'][1:].unique())
    saf_process  = html.Div(
        [
            dbc.Label("Select SAF Production Process"),
            dcc.Dropdown(process_list,
                value = 'All',
                placeholder = 'All', 
                disabled = False,
                clearable=False,
                style = {'display': True, 'color': 'black'},
                id="saf_process_metrics",   
            ),
        ],
        className="mb-4",
    ) 
    return saf_process

 
def select_saf_feedstock(Commercial_SAF): 
    All = ['All']
    process_list = All + list(Commercial_SAF['Feedstock'][1:].unique())
    saf_process = html.Div(
        [
            dbc.Label("Select SAF Feedstock"),
            dcc.Dropdown(process_list,
                value = 'All',
                placeholder = 'All', 
                disabled = False,
                clearable=False,
                style = {'display': True, 'color': 'black'},
                id="saf_feedstock_metrics",   
            ),
        ],
        className="mb-4",
    ) 
    return saf_process
 
def select_saf_x_axis_metrics(Commercial_SAF): 
    saf_x_axis = html.Div(
        [
            dbc.Label("X-Axis"),
            dcc.Dropdown(list(Commercial_SAF.columns.values)[10:39],
                value = 'Boiling Point (°C)',
                placeholder = 'Select Indicator', 
                disabled = False,
                clearable=False,
                style = {'display': True, 'color': 'black'},
                id="saf_x_axis_metrics",   
            ),
        ],
        className="mb-4",
    ) 
    
    return saf_x_axis 


def select_saf_y_axis_metrics(Commercial_SAF):
    saf_y_axis = html.Div(
        [
            dbc.Label("Y-Axis"),
            dcc.Dropdown(list(Commercial_SAF.columns.values)[10:39],
                value = 'Flash Point (°C)',
                placeholder = 'Select Indicator', 
                disabled = False,
                clearable=False,
                style = {'display': True, 'color': 'black'},
                id="saf_y_axis_metrics",   
            ),
        ],
        className="mb-4",
    ) 
    return saf_y_axis
 
 
# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Panel 2 
# ---------------------------------------------------------------------------------------------------------------------------------------------------  
def select_saf_sector_dev_panel(Commercial_SAF):
    All = ['All']
    feedstock_list = All + list(Commercial_SAF['Feedstock'][1:].unique())
    saf_industry = html.Div(
        [
            dbc.Label("Select SAF Feedstock"), 
            dcc.Dropdown(feedstock_list,
                value = 'All',
                placeholder = 'All', 
                disabled = False,
                clearable=False,
                style = {'display': True, 'color': 'black'},
                id="saf_feedstock_sector",   
            ),
        ],
        className="mb-4",
    ) 
    return saf_industry

def select_saf_process_dev_panel(Commercial_SAF): 
    All = ['All']
    process_list = All +   list(Commercial_SAF['Process'][1:].unique())
    saf_type  = html.Div(
        [
            dbc.Label("Select SAF Production Process"),
            dcc.Dropdown(process_list,
                value = 'All',
                placeholder = 'All', 
                disabled = False,
                clearable=False,
                style = {'display': True, 'color': 'black'},
                id="saf_process_sector",
            ),
        ],
        className="mb-4",
    ) 
    return saf_type
 
# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Panel  
# ---------------------------------------------------------------------------------------------------------------------------------------------------  
def select_fuels_list(Commercial_SAF):
    saf_list_1 = list(Commercial_SAF["Fuel Name"])[:35]
    saf_list_2 = Commercial_SAF["Fuel Name"][35:]
    saf_selection_1 = html.Div( [ dcc.Checklist(options=saf_list_1 , value=saf_list_1[0:4],
                                                id="fuel_selection_list_1", ), ],className="mb-4", )  
    saf_selection_2 = html.Div( [ dcc.Checklist(options=saf_list_2 , value=saf_list_2[0:3],
                                                id="fuel_selection_list_2", ), ], className="mb-4",) 
    return saf_selection_1, saf_selection_2  

def select_saf_feedstock_states(): 
    
    states_1  = ["Alabama","Arizona","Arkansas","California","Colorado", "Connecticut","Delaware","Florida"]  
    states_2  = ["Georgia","Idaho","Illinois", "Indiana","Iowa","Kansas","Kentucky","Louisiana"] 
    states_3  = ["Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana"] 
    states_4  = ["Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York", "North Carolina","Ohio"] 
    states_5  = ["Oklahoma","Oregon","Pennsylvania", "Rhode Island","South Carolina","South Dakota","North Dakota","Tennessee"]
    states_6  = ["Texas","Utah",  "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]  
    
    state_list_1 = html.Div([ dcc.Checklist( options = states_1, value  =["Arkansas","California","Colorado"], id="feedstock_states_1", ), ],className="mb-4",) 
    state_list_2 = html.Div([ dcc.Checklist( options = states_2, value  =["Illinois", "Indiana","Iowa","Kansas","Kentucky"], id="feedstock_states_2", ), ],className="mb-4",)
    state_list_3 = html.Div([ dcc.Checklist( options = states_3, value  = ["Missouri", "Nebraska"], id="feedstock_states_3", ), ],className="mb-4",)
    state_list_4 = html.Div([ dcc.Checklist( options = states_4, value  =  ["Ohio","Oklahoma"], id="feedstock_states_4", ), ],className="mb-4",) 
    state_list_5 = html.Div([ dcc.Checklist( options = states_5, value  =  [""]     , id="feedstock_states_5", ), ],className="mb-4",)    
    state_list_6 = html.Div([ dcc.Checklist( options = states_6, value  =  [""]     , id="feedstock_states_6", ), ],className="mb-4",)      
        
    return state_list_1 ,state_list_2 ,state_list_3 ,state_list_4,state_list_5 ,state_list_6
 
def select_saf_fleet_adoption(): 
    fleet_adoption = html.Div(
        [
            dbc.Label("Fleet Adoption"),
            dcc.Slider(0, 100, 10,
                value=20,
                id="saf_percent_adoption", 
            ),
        ],
        className="mb-4",
    )
    return  fleet_adoption 


def select_saf_airports(): 
    airport_names = [" Top 5 Airports"," Top 10 Airports"," Top 20 Airports", " Top 50 Airports",  " All Airports"]
    airpots = html.Div(  [  dbc.Label("Select SAF Airport Hubs"), dcc.RadioItems( options = airport_names, value   = " Top 10 Airports", 
                           id="saf_airports",  ),  ], className="mb-4", )   
    return airpots

def select_feedstock_source(Commercial_SAF):  
    process_list =  list(Commercial_SAF['Source'][1:].unique())
    saf_process = html.Div(
        [
            dbc.Label("Select SAF Feedstock Crop"),
            dcc.Dropdown(process_list,
                value = 'Canola',
                placeholder = 'Canola', 
                disabled = False,
                clearable=False,
                style = {'display': True, 'color': 'black'},
                id="saf_feedstock_source",   
            ),
        ],
        className="mb-4",
    ) 
    return saf_process

def select_saf_cost(): 
    saf_cost = html.Div(
        [
            dbc.Label("SAF Cost ($/gal)"),
            dcc.Slider(2, 20, 2,
                value=8,
                id="SAF_dollars_per_gal", 
            ),
        ],
        className="mb-4",
    )
    return saf_cost
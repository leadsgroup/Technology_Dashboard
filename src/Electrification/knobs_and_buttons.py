from dash import html, dcc  
import dash_bootstrap_components as dbc 

# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Panel 1 
# ---------------------------------------------------------------------------------------------------------------------------------------------------  
def select_battery_brand_metrics(Commercial_Batteries):
    All = ['All']
    brand_list = All + list(Commercial_Batteries['Brand'][1:].unique())
    battery_brand = html.Div(
        [
            dbc.Label("Select Battery Brand"),
            dcc.Dropdown(brand_list,
                value = 'All',
                placeholder = 'All', 
                disabled = False,
                clearable=False,
                style = {'display': True, 'color': 'black'},
                id="battery_brand_metrics",   
            ),
        ],
        className="mb-4",
    ) 
    return battery_brand
 
def select_battery_chemistry_metrics(Commercial_Batteries): 
    All = ['All']
    chemistry_list = All + list(Commercial_Batteries['Chemistry'][1:].unique())
    battery_chemistry = html.Div(
        [
            dbc.Label("Select Battery Chemistry"),
            dcc.Dropdown(chemistry_list,
                value = 'All',
                placeholder = 'All', 
                disabled = False,
                clearable=False,
                style = {'display': True, 'color': 'black'},
                id="battery_chemistry_metrics",   
            ),
        ],
        className="mb-4",
    ) 
    return battery_chemistry

def select_battery_x_axis_metrics(Commercial_Batteries): 
    battery_x_axis = html.Div(
        [
            dbc.Label("X-Axis"),
            dcc.Dropdown(list(Commercial_Batteries.columns.values)[5:19],
                value = list(Commercial_Batteries.columns.values)[5:19][7],
                placeholder = 'Select Indicator', 
                disabled = False,
                clearable=False,
                style = {'display': True, 'color': 'black'},
                id="battery_x_axis_metrics",   
            ),
        ],
        className="mb-4",
    ) 
    
    return battery_x_axis 


def select_battery_y_axis_metrics(Commercial_Batteries):
    battery_y_axis = html.Div(
        [
            dbc.Label("Y-Axis"),
            dcc.Dropdown(list(Commercial_Batteries.columns.values)[5:19],
                value = list(Commercial_Batteries.columns.values)[5:19][9],
                placeholder = 'Select Indicator', 
                disabled = False,
                clearable=False,
                style = {'display': True, 'color': 'black'},
                id="battery_y_axis_metrics",   
            ),
        ],
        className="mb-4",
    ) 
    return battery_y_axis
 
 

# ---------------------------------------------------------------------------------------------------------------------------------------------------
#  Motor 1 
# ---------------------------------------------------------------------------------------------------------------------------------------------------  
def select_motor_manfacturers_metrics(Electric_Motor_Development): 
    All = ['All']
    manufacturers_list = All + list(Electric_Motor_Development['Manufacturer'][1:].unique()) 
    manufacturers= html.Div(
        [
            dbc.Label("Select Manufacturer"),
            dcc.Dropdown(manufacturers_list,
                value = 'All',
                placeholder = 'All', 
                disabled = False,
                clearable=False,
                style = {'display': True, 'color': 'black'},
                id="motor_manufacturer_metrics",   
            ),
        ],
        className="mb-4",
    ) 
    return manufacturers

def select_motor_type_metrics(Electric_Motor_Development):
    All = ['All']
    motor_type_list = All + list(Electric_Motor_Development['Motor Type'][1:].unique())
    motor_type  = html.Div(
        [
            dbc.Label("Select Type"),
            dcc.Dropdown(motor_type_list,
                value = 'All',
                placeholder = 'All', 
                disabled = False,
                clearable=False,
                style = {'display': True, 'color': 'black'},
                id="motor_type_metrics",   
            ),
        ],
        className="mb-4",
    ) 
    return motor_type


def select_motor_x_axis_metrics(Electric_Motor_Development): 
    motor_x_axis = html.Div(
        [
            dbc.Label("X-Axis"),
            dcc.Dropdown(list(Electric_Motor_Development.columns.values)[4:14],
                value = list(Electric_Motor_Development.columns.values)[4:14][1],
                placeholder = 'Select Indicator', 
                disabled = False,
                clearable=False,
                style = {'display': True, 'color': 'black'},
                id="motor_x_axis_metrics",   
            ),
        ],
        className="mb-4",
    ) 
    
    return motor_x_axis 


def select_motor_y_axis_metrics(Electric_Motor_Development):
    motor_y_axis = html.Div(
        [
            dbc.Label("Y-Axis"),
            dcc.Dropdown(list(Electric_Motor_Development.columns.values)[4:14],
                value = list(Electric_Motor_Development.columns.values)[4:14][2],
                placeholder = 'Select Indicator', 
                disabled = False,
                clearable=False,
                style = {'display': True, 'color': 'black'},
                id="motor_y_axis_metrics",   
            ),
        ],
        className="mb-4",
    ) 
    return motor_y_axis


# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Panel 2 
# ---------------------------------------------------------------------------------------------------------------------------------------------------  
def select_battery_1(Commercial_Batteries): 
    battery_1_selection  = html.Div(
        [  
            dbc.Label("Select Battery Cell 1"),
            dcc.Dropdown(list(Commercial_Batteries['Battery Name'][1:].unique()),
                value       = list(Commercial_Batteries['Battery Name'][1:].unique())[17],
                placeholder = 'Select Battery', 
                disabled    = False,
                clearable=False,
                style       = {'display': True, 'color': 'black'},
                id          = "battery_1",   
            ),
        ],
        className="mb-4", 
    ) 
    return battery_1_selection 

def select_battery_2(Commercial_Batteries):
    battery_2_selection   = html.Div(
        [ 
            dbc.Label("Select Battery Cell 2"),
            dcc.Dropdown(list(Commercial_Batteries['Battery Name'][1:].unique()),
                value        = list(Commercial_Batteries['Battery Name'][1:].unique())[8],
                placeholder  = 'Select Battery', 
                disabled     = False,
                clearable=False,
                style        = {'display': True, 'color': 'black'},
                id           ="battery_2",   
            ),
        ],
        className="mb-4", 
    ) 
    return battery_2_selection 

def select_battery_3(Commercial_Batteries):
    battery_3_selection   = html.Div(
        [ 
            dbc.Label("Select Battery Cell 3"),
            dcc.Dropdown(list(Commercial_Batteries['Battery Name'][1:].unique()),
                value        = list(Commercial_Batteries['Battery Name'][1:].unique())[0],
                placeholder  = 'Select Battery',
                disabled     = False,
                clearable=False,
                style        = {'display': True, 'color': 'black'},
                id           ="battery_3",   
            ),
        ],
        className="mb-4", 
    ) 
    return battery_3_selection 
 
# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Panel 3 
# ---------------------------------------------------------------------------------------------------------------------------------------------------  
def select_battery_industry_dev_panel(Battery_Development):
    All = ['All']
    sector_list = All + list(Battery_Development['Sector'][1:].unique())
    battery_industry = html.Div(
        [
            dbc.Label("Select Sector"), 
            dcc.Dropdown(sector_list,
                value = 'All',
                placeholder = 'All', 
                disabled = False,
                clearable=False,
                style = {'display': True, 'color': 'black'},
                id="battery_sector",   
            ),
        ],
        className="mb-4",
    ) 
    return battery_industry

def select_battery_type_dev_panel(Battery_Development): 
    type_list =  ['All','Li-Ion','Li-Sulphur','Metal-Air','Li-Silicon']
    battery_type = html.Div(
        [
            dbc.Label("Select Battery Type"),
            dcc.Dropdown(type_list,
                value = 'All',
                placeholder = 'All', 
                disabled = False,
                clearable=False,
                style = {'display': True, 'color': 'black'},
                id="battery_type",
            ),
        ],
        className="mb-4",
    ) 
    return battery_type 


# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Panel 4 
# ---------------------------------------------------------------------------------------------------------------------------------------------------  
def select_battery_industry_dev_panel(Battery_Development):
    All = ['All']
    sector_list = All + list(Battery_Development['Sector'][1:].unique())
    battery_industry = html.Div(
        [
            dbc.Label("Select Sector"), 
            dcc.Dropdown(sector_list,
                value = 'All',
                placeholder = 'All', 
                disabled = False,
                clearable=False,
                style = {'display': True, 'color': 'black'},
                id="battery_sector",   
            ),
        ],
        className="mb-4",
    ) 
    return battery_industry

def select_battery_type_dev_panel(Battery_Development): 
    type_list =  ['All','Li-Ion','Li-Sulphur','Metal-Air','Li-Silicon']
    battery_type = html.Div(
        [
            dbc.Label("Select Battery Type"),
            dcc.Dropdown(type_list,
                value = 'All',
                placeholder = 'All', 
                disabled = False,
                clearable=False,
                style = {'display': True, 'color': 'black'},
                id="battery_type",
            ),
        ],
        className="mb-4",
    ) 
    return battery_type




# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Flight Ops Panel 
# ---------------------------------------------------------------------------------------------------------------------------------------------------  
def select_flight_ops_electric_aircraft_battery(Commercial_Batteries):
    electric_aircraft_battery = html.Div(
        [ 
            dbc.Label("Battery Cell"),
            dcc.Dropdown(list(Commercial_Batteries['Battery Name'][1:].unique()),
                value        = Commercial_Batteries['Battery Name'][36],
                placeholder  = Commercial_Batteries['Battery Name'][36], 
                disabled     = False,
                clearable=False,
                style        = {'display': True, 'color': 'black'},
                id           ="electric_aircraft_battery",   
            ),
        ],
        className="mb-4", 
    )  
    return electric_aircraft_battery 
  
def select_flight_ops_electric_aircraft():
    flight_ops_electric_aircraft = html.Div(
        [
            dbc.Label("All-Electric Aircraft Model"),
            dcc.Dropdown(
                ['ATR 72-600','Embraer 190','Boeing 737 MAX-8','Airbus A320 neo'],
                value = 'Boeing 737 MAX-8',
                placeholder = 'Boeing 737 MAX-8',  
                disabled = False,
                clearable=False,
                style = {'display': True, 'color': 'black'},
                id="electric_aircraft_type",   
            ),
        ],
        className="mb-4",
    ) 
    return flight_ops_electric_aircraft


def select_flight_ops_electric_aircraft_batt_mass_frac():
    
    battery_mass_fraction = html.Div(
        [
            dbc.Label("Battery Mass Fraction (%)"),
            dcc.Slider(10, 90, 10,
                value= 30,
                id="battery_mass_fraction", 
            ),
        ],
        className="mb-4",
    )
    return  battery_mass_fraction

def select_flight_ops_electric_fleet_adoption(): 
    fleet_adoption = html.Div(
        [
            dbc.Label("Fleet Adoption (%)"),
            dcc.Slider(0, 100, 10,
                value=100,
                id="electric_aircraft_percent_adoption", 
            ),
        ],
        className="mb-4",
    )
    return  fleet_adoption

def select_cost_of_electricity(): 
    charging_cost = html.Div(
        [
            dbc.Label("Cost of Electricity ($/kWh)"),
            dcc.Slider(0.1, 1, 0.1,
                value=0.3,
                id="electric_aircraft_charging_cost", 
            ),
        ],
        className="mb-4",
    ) 
    return charging_cost


def select_electric_aircraft_system_voltage():
    system_voltage = html.Div(
        [
            dbc.Label("System Voltage (kV)"),
            dcc.Slider(0.6, 2, 0.2,
                value=1,
                id="electric_aircraft_system_voltage", 
            ),
        ],
        className="mb-4",
    ) 
    return system_voltage 
def select_electric_aircraft_propulsive_efficiency():
    propulsive_efficiency = html.Div(
        [
            dbc.Label("Propulsive Efficiency (%)"),
            dcc.Slider(50, 100, 5,
                value=95,
                id="electric_aircraft_efficiency", 
            ),
        ],
        className="mb-4",
    )  
    return propulsive_efficiency

def select_flight_ops_month_electric_aircraft(US_Temperature_F):
    
    battery_dev_year = html.Div(
        [
            dbc.Label("Month"), 
            dcc.Slider(0, 11, 1,
                value=4, 
                marks = {
                    0:{'label': "Jan"},
                    1:{'label': "Feb"}, 
                    2:{'label': "Mar"},  
                    3:{'label': "Apr"}, 
                    4:{'label': "May"},
                    5:{'label': "Jun"},
                    6:{'label': "Jul"},
                    7:{'label': "Aug"}, 
                    8:{'label': "Sep"},  
                    9:{'label': "Oct"}, 
                    10:{'label': "Nov"}, 
                    11:{'label': "Dec"},                    
                 },
                id="electric_aircraft_month",
            ),
        ],
        className="mb-4",
    )
    return  battery_dev_year

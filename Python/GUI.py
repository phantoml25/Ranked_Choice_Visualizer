import math    
import PySimpleGUI as sg
from Candidate_Permutations import *    

def DrawPieChart(graph,percentages,labels,colors,previous_graph_items=0):
    if previous_graph_items is list:
        for x in range(len(previous_graph_items)):
            graph.delete_figure(previous_graph_items[x])
    print("erased previous graphs")
    
    current_graph_items = []
    
    if len(percentages) != len(labels):
        print("mismatched percents and labels!")
        return 1
    if len(percentages) > len(colors):
        print("Not enough colors!")
        return 1

    start_angle = 90
    for x in range(len(percentages)):
        angle = -(360 * percentages[x])
        radian = (start_angle+(angle/2)) * (math.pi/180)
        current_graph_items.append(graph.DrawArc((-100,100),(100,-100),angle,start_angle,style="pieslice",fill_color=colors[x]))
        if percentages[x] != 0:
            current_graph_items.append(graph.DrawText(labels[x],((math.cos(radian)*50),(math.sin(radian)*50)),color="black"))
        start_angle += angle
    
    return current_graph_items


def Switch_Tabs(opened_tab):
    tab_list = ['input_tab','loading_screen','results_tab']
    for x in tab_list:
        if opened_tab != x:
            window[x].update(visible = False)
        else:
            window[x].update(visible = True)
    return 0

def PrepareResults(cand,results,population,visible=False):
    if visible:
        Switch_Tabs('loading_screen')
        window['completion'].update(value='0')
        window["progress_description"].update(value="Preparing Results")
    first_percentages = []
    total_percentages = []
    for x in range(len(results[0])):
        if results[len(results)-1][x] != 0:
            temp_percent = 0
            for y in range(1,len(results)):
                temp_percent += results[y][x]
            total_percentages.append(temp_percent/population)
        else:
            total_percentages.append(0)
        first_percentages.append(results[1][x]/population)
        if visible:
            window['progress'].update(current_count= x, max=population)
            window['completion'].update(value=int((x/population)*100))
            window.refresh()
    
    
    rows = [[cand[0],results[1][0],results[2][0],results[3][0],round(total_percentages[0]*100,2)],
            [cand[1],results[1][1],results[2][1],results[3][1],round(total_percentages[1]*100,2)],
            [cand[2],results[1][2],results[2][2],results[3][2],round(total_percentages[2]*100,2)],
            [cand[3],results[1][3],results[2][3],results[3][3],round(total_percentages[3]*100,2)]]

    rows_right = [[cand[0],results[1][0],round(first_percentages[0]*100,2)],
                [cand[1],results[1][1],round(first_percentages[1]*100,2)],
                [cand[2],results[1][2],round(first_percentages[2]*100,2)],
                [cand[3],results[1][3],round(first_percentages[3]*100,2)]]
    return first_percentages,total_percentages,rows,rows_right

'''Begin Constants'''
Colors = ["red","light blue","green","yellow","orange","purple"]
toprow = ['Candidate', '1st Choice', '2nd Choice', '3rd choice','Final Vote Percent']
toprow_right = ['Candidate','Votes','Vote Percent']
'''End Constants'''

'''Begin Placeholder Data Generation'''
left_percentages = [.25,.1,.6,.05]
right_percentages = [.3,.3,.1,.3]
cand = ['Abe','Beckket','Calliway','Abby']
population = 32800
cand = ['Abe','Beckket','Calliway','Abby']
comb = [['B','C'],
        ['A','C'],
        ['A','B']]
first_Choice = [.31,.1,.29,.30]
results = [['Abby', 'Abe', 'Beckket', 'Calliway'], [10195, 3290, 9518, 9797], [3448, 0, 7864, 349], [518, 0, 1257, 0]]
difference = [['Ranked Choice', '1 Choice'], ['Beckket', 'Abby'], [18639, 10195]]

first_percentages, total_percentages, rows,rows_right = PrepareResults(cand,results,population,visible=False)
'''End Data Generation, Begin display generation'''

tbl1 = sg.Table(values=rows, headings=toprow,
   auto_size_columns=True,
   display_row_numbers=False,
   justification='center', key='table_bl',
   selected_row_colors='red on yellow',
   enable_events=True,
   expand_x=False,
   expand_y=False,
 enable_click_events=True)

tbl2 = sg.Table(values=rows_right, headings=toprow_right,
   auto_size_columns=True,
   display_row_numbers=False,
   justification='center', key='table_br',
   selected_row_colors='red on yellow',
   enable_events=True,
   expand_x=True,
   expand_y=True,
 enable_click_events=True)

layout_results = [[sg.Graph(canvas_size=(400, 400), graph_bottom_left=(-105,-105), graph_top_right=(105,105), background_color='white', key='graph_tl'),
          sg.Graph(canvas_size=(400, 400), graph_bottom_left=(-105,-105), graph_top_right=(105,105), background_color='white', key='graph_tr')],
          [tbl1,tbl2]]    

layout_input = [[sg.Button(button_text="Add Candidate"),sg.Button(button_text="Calculate Results")],
                [sg.Text("Enter Population"),sg.Input(key="Population")],
                [sg.Text("Enter Candidate Name",expand_x=True),sg.Text("Weight",expand_x=True),sg.Text("Preferred Next Candidate",expand_x=True)],
                [sg.Multiline(size=(30,30),expand_x=True,autoscroll=True,no_scrollbar=True,auto_refresh=True,key="Candidates_table"),
                 sg.Multiline(size=(30,30),expand_x=True,autoscroll=True,no_scrollbar=True,auto_refresh=True,key="Weights_table"),
                 sg.Multiline(size=(30,30),expand_x=True,autoscroll=True,no_scrollbar=True,auto_refresh=True,key="Next_Table")]]
layout_loading=[[sg.Text("",key="progress_description")],
                [sg.ProgressBar(max_value=population,size=(100,30),orientation='horizontal',key='progress'),sg.Text("0",key='completion'),sg.Text("/100")]]


button_group = [[sg.Button(button_text="Input",key="input_button"),
                sg.Button(button_text="Results",key="results_button")]]
tab_group = [
            [sg.pin(sg.Column(layout_input,   p=0, key="input_tab",visible=True))],
            [sg.pin(sg.Column(layout_loading, p=0, key="loading_screen", visible=False))],
            [sg.pin(sg.Column(layout_results, p=0, key="results_tab",visible=False))]
            ]

full_layout = [[button_group],[tab_group]]

window = sg.Window('Graph of Sine Function', full_layout,auto_size_text=True,
                   auto_size_buttons=True,resizable=True,location=(200,200),finalize=True)  
left_graph = window['graph_tl']
right_graph = window['graph_tr'] 
left_graph_items = []
right_graph_items = []
left_graph_items = DrawPieChart(graph=left_graph,percentages=total_percentages,labels=cand,colors=Colors)
right_graph_items = DrawPieChart(graph=right_graph,percentages=first_percentages,labels=cand,colors=Colors)

current_tab = 'input_tab'

"""theme_name_list = sg.theme_list()
print(theme_name_list)"""
while True:
    event, values = window.read()
    print("event:", event, "values:", values)
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    if type(event) != int:
        if 'input_button' in event:
            Switch_Tabs('input_tab')
            pass
        if event == 'results_button':
            Switch_Tabs('results_tab')
        if '+CLICKED+' in event:
            if len(event) >=3:
                sg.popup("You clicked row:{} Column: {}".format(event[2][0], event[2][1]))
        if event == "Calculate Results":
            '''Split multiline inputs on \n'''
            cand = values["Candidates_table"]
            population = int(values["Population"])
            first_Choice = values["Weights_table"]
            
            cand = cand.split("\n")
            print(cand)
            first_Choice = first_Choice.split("\n")
            
            for x in range(len(first_Choice)):
                first_Choice[x] = float(first_Choice[x])
            print(first_Choice)
            
            
            
            Switch_Tabs('loading_screen')
            results,difference = Biased_Ranked_Choice_method(cand,population,first_Choice,window=window)
            first_percentages, total_percentages, rows,rows_right = PrepareResults(cand,results,population,visible=True)
            Switch_Tabs('results_tab')
            left_graph_items = DrawPieChart(graph=left_graph,percentages=total_percentages,labels=cand,colors=Colors,previous_graph_items=left_graph_items)
            right_graph_items = DrawPieChart(graph=right_graph,percentages=first_percentages,labels=cand,colors=Colors,previous_graph_items=right_graph_items)
            
    else:
        pass
window.close()

event, values = window.read()
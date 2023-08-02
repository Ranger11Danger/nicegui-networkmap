from nicegui import ui, Client
import pprint

@ui.page('/')
async def page(client: Client):

    chart = ui.chart({
        'title': False,
        'chart': {'type': 'networkgraph', 'marginTop':80},
        'plotOptions':{'networkgraph': {"keys":['from', 'to']}},
        'series':[{
            'link':{'linkLength':200},
            'layoutAlgorithm':{'enableSimulation': True, 'integration':'euler', 'linkLength':"50"},
            'dataLabels':{'enabled':True, 'linkFormat':'','allowOverlap':True, 'style':{'fontSize':'20px', 'textOutline':False}},
            'marker':{'radius':50},
            "data": [
            ],
            'nodes':[
            ]
        }] 
        },extras=["networkgraph",'accessibility']).classes('w-full').style("height:75vh")
    

    async def add_node(name, color="red"):
        my_nodes = chart.options['series'][0]["nodes"]
        my_nodes.append({'id':name, 'color':color})
        name_field.value=""
        color_field.value=""
        await ui.run_javascript('''
        const chart = getElement(''' + str(chart.id) + ''').chart;
        chart.update({
        series: {
        nodes:'''+str(my_nodes)+''',
        } 
        })
                                ''', respond=False)
    async def del_node(node_id):
        my_data = chart.options['series'][0]["data"]
        my_nodes = chart.options['series'][0]["nodes"]
        new_nodes = [x for x in my_nodes if x["id"] != node_id]
        new_data = [x for x in my_data if x[0] != node_id and x[1] != node_id]
        chart.options['series'][0]["data"] = new_data 
        chart.options['series'][0]["nodes"] = new_nodes
        del_name_field.value=""
        await ui.run_javascript('''
        const chart = getElement(''' + str(chart.id) + ''').chart;
        chart.update({
        series: {
        nodes:'''+str(new_nodes)+''',
        data:'''+str(new_data)+''',
        } 
        })
                                ''', respond=False)
    async def clear_nodes():
        chart.options['series'][0]["data"] = [] 
        chart.options['series'][0]["nodes"] = [] 
        await ui.run_javascript('''
        const chart = getElement(''' + str(chart.id) + ''').chart;
        chart.update({
        series: {
        data: [],
        nodes: [],
        } 
        })
        chart.redraw()
                                ''', respond=False)
    async def add_connection(link1, link2):
        my_data = chart.options['series'][0]["data"]
        my_data.append([link1, link2])
        from_field.value=""
        to_field.value=""
        await ui.run_javascript('''
        const chart = getElement(''' + str(chart.id) + ''').chart;
        chart.update({
        series: {
        data:'''+str(my_data)+''',
        } 
        })
                                ''', respond=False)

    await client.connected()

    with ui.row():
        with ui.card():
            ui.label("Add Node")
            name_field = ui.input(label="Name", placeholder="Node ID")
            color_field = ui.input(label="Color", placeholder="Node Color")
            ui.button("Submit", on_click=lambda: add_node(name_field.value, color_field.value))

        with ui.card():
            ui.label("Remove Node")
            del_name_field = ui.input(label="Name", placeholder="Node ID")
            ui.button("Submit", on_click=lambda: del_node(del_name_field.value))
            ui.button("Clear All", on_click=clear_nodes)

        with ui.card():
            ui.label("Add Link")
            from_field = ui.input(label="From", placeholder="From ID")
            to_field = ui.input(label="To", placeholder="To ID")
            ui.button("Submit", on_click=lambda: add_connection(from_field.value, to_field.value))

ui.run()

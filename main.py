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
                ['Node1', 'Node2'],
            ],
            'nodes':[
                {'id':'Node1', 'color':'green'},
                {'id':'Node2', 'color':'green'},
            ]
        }] 
    },extras=["networkgraph",'accessibility']).classes('w-full h-screen')
    

    async def add_node():
        my_nodes = chart.options['series'][0]["nodes"]
        my_nodes.append({'id':'test', 'color':'red'})
        my_data = chart.options['series'][0]["data"]
        my_data.append(['test','Node2'])
        await ui.run_javascript('''
        const chart = getElement(''' + str(chart.id) + ''').chart;
        chart.update({
        series: {
        nodes:'''+str(my_nodes)+''',
        data:'''+str(my_data)+''',
        } 
        })
                                ''', respond=False)
    await client.connected()
    ui.button("Update", on_click=add_node)


ui.run()

from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/home.jinja2')
def my_view(request):
    return {
        'triesTotal': '646',
        'triesPassed': '33',
        'lastTeam': 'nms (guess who)',
        'lastTask': 'A',
        'lastTime': '1:20:03',
    }

from django.shortcuts import render

def model(request):
    if request.method == 'GET':
        return render(request, 'model/model.html', {})
    if request.method == 'POST':
        restrictions = request.POST.get('restrictions')
        variables = request.POST.get('variables')
        operation = request.POST.get('operation')
        context = {
            'showModel': True,
            'operation': operation,
            'restrictions': {
                'value': int(restrictions),
                'range': range(1, int(restrictions)+1)
            },
            'variables': {
                'value': int(variables),
                'range': range(1, int(variables)+1)
            }
        }
        return render(request, 'model/model.html', context)

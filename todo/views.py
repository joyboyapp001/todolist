from django.shortcuts import render
from .models import Todo
# Create your views here.


def todo(request, id):
    todo = None
    try:
        todo = Todo.objects.get(id=id)
    except Exception as e:
        print(e)
    return render(request, 'todo/todo.html', {'todo': todo})


def todolist(request):
    todos = None
    user = request.user
    if user.is_authenticated:
        todos = Todo.objects.filter(user=user)

    return render(request, 'todo/todolist.html', {'todos': todos})

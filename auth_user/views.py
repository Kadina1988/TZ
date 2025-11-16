from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response

from auth_user.models import User 


import pdb 

@api_view(['POST'])
def register(request):
    if request.data['password'] != request.data['password_confirm']:
        return Response({'error': 'Пароли не совпадают'})
    
    user = User.objects.create(
        name = request.data['name'],
        email = request.data['email'],
        password = request.data['password']
    )
    
    return Response({
        'user': {
            'id': user.pk,
            'name': user.name,
            'email': user.email,
        }
    })

@api_view()
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
        if not user.is_active:
            raise ObjectDoesNotExist

    except ObjectDoesNotExist:
        return Response({"error": "Не верный id или пользователь был удален"})
    
    return Response({
        'user': {
            'id': user.pk,
            'name': user.name,
            'email': user.email
        }
    })
    

@api_view(['PATCH', 'PUT'])
def user_update(request, pk):
    try:
        user = User.objects.get(pk=pk)
        if not user.is_active:
            raise ObjectDoesNotExist

    except ObjectDoesNotExist:
        return Response({"error": "Не верный id или пользователь был удален"})
    
    user.name = request.data['name']
    user.email = request.data['email']
    user.save()
    
    return Response({
        'user': {
            'id': user.pk,
            'name': user.name,
            'email': user.email
        }
    })    
    

@api_view(['DELETE'])    
def delete_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
        if not user.is_active:
            raise ObjectDoesNotExist

    except ObjectDoesNotExist:
        return Response({"error": "Не верный id или пользователь был удален"})
    
    user.is_active = False 
    user.save()
    
    return Response({"message": "Пользователь был удален"})   


@api_view(["POST"])
def login(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email, is_active=True)
        except:
            return render(request, 'auth_user/login_form.html', {'message': 'Несуществующий пользователь'})
        
        if user.password == password:
            request.session['user_id'] = user.pk 
            return HttpResponseRedirect('/user_detail/')
        else:
            return render(request, 'auth_user/login_form.html', {'message': 'Неверный пароль'})
    
    return render(request, 'auth_user/login_form.html')


def logout(request):
    request.session['user_id'] = None 
    return HttpResponseRedirect('/login/')

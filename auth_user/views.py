from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response

from auth_user.models import AccessToken, User 


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
    try:
        user = User.objects.get(email=request.data['email'], is_active=True)
    except ObjectDoesNotExist:
        return Response({"error": "Пользователь с таким email не найден"})
    
    if request.data['password'] == user.password:
        AccessToken.objects.create(user=user)
        return Response({'token': user.accesstoken.token})
    else:
        return Response({'error': 'Не верный пароль'})


@api_view(["POST"])
def logout(request):
    token = request.headers['Authorization'].replace("Bearer ", '')
    try:
        AccessToken.objects.get(token=token).delete()
    except:
        return Response({"message": "Unauthorized"}, status=401)

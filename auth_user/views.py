from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from auth_user.models import AccessToken, User, Role


BOOKS = [{'id': 1,'name': 'Pushkin'}, {'id': 2, 'name': 'Maugli'}, {'id': 3, 'name': 'Tarzan'}] 


@api_view(['POST'])
def register(request):
    '''
    Метод для регистрации пользователя
    '''
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
            'email': user.email,
            'role': {
                'id': user.role.pk,
                'name': user.role.name
            }
        }
    })
    

@api_view(['PATCH', 'PUT'])
def user_update(request):
    try:
        user = get_authorized_user(request)
        if not user.is_active:
            raise ObjectDoesNotExist

    except ObjectDoesNotExist:
        return Response({"error": "Не верный id или пользователь был удален"})
    except:
        return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
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
def delete_user(request):
    try:
        user = get_authorized_user(request)
        if not user.is_active:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist:
        return Response({"error": "Не верный id или пользователь был удален"})
    except: 
        return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
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
        return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response({'message': 'sign out'})
    
    
@api_view()
def roles_list(request):
    try:
        user = get_authorized_user(request)
    except:
        return Response({"message": "Нужно войти в систему"}, status=status.HTTP_401_UNAUTHORIZED)
    
    if not user.role.name == 'admin':
        return Response({"error": "Forbidden error"}, status=status.HTTP_403_FORBIDDEN)
    
    roles = Role.objects.all()
    json_roles = list(roles.values('id', 'name'))
    return Response({'roles': json_roles})
    
    
@api_view()
def users_list(request): 
    try:
        user = get_authorized_user(request)
    except:
        return Response({"message": "Нужно войти в систему"}, status=status.HTTP_401_UNAUTHORIZED)
        
    if not user.role.name == 'admin':
        return Response({"error": "Forbidden error"}, status=status.HTTP_403_FORBIDDEN)
        
    u = User.objects.all()
    users = list(u.values('id', 'email', 'name', 'role_id'))
    return Response({'users': users})


@api_view(['PUT'])
def change_role(request, pk):
    try:
        user = get_authorized_user(request)
    except:
        return Response({"message": "Нужно войти в систему"}, status=status.HTTP_401_UNAUTHORIZED)
        
    if not user.role.name == 'admin':
        return Response({"error": "Forbidden error"}, status=status.HTTP_403_FORBIDDEN)
    
    role = Role.objects.get(pk=request.data['role_id'])
    user = User.objects.get(pk=pk)
    user.role = role
    user.save()

    return Response({'user': {
        'id': user.pk,
        'name': user.name,
        'email': user.email,
        'role_id': user.role.pk
    }})
    
    
@api_view()
def books_list(request):
    try:
        get_authorized_user(request)
    except:
        return Response({"message": "Нужно войти в систему"}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({"books": BOOKS})


@api_view()
def book_detail(request, pk):
    try:
        user = get_authorized_user(request)
    except:
        return Response({"message": "Нужно войти в систему"}, status=status.HTTP_401_UNAUTHORIZED)
    
    if user.role.name == 'user':
        return Response({"error": "Forbidden error"}, status=status.HTTP_403_FORBIDDEN)
    
    book = next(filter(lambda x: x['id'] == pk, BOOKS), None)
    return Response({"book": book})


@api_view(['POST'])
def book_change(request, pk):
    try:
        user = get_authorized_user(request)
    except:
        return Response({"message": "Нужно войти в систему"}, status=status.HTTP_401_UNAUTHORIZED)
    
    if not user.role.name == 'admin':
        return Response({"error": "Forbidden error"}, status=status.HTTP_403_FORBIDDEN)
    
    book = next(filter(lambda x: x['id'] == pk, BOOKS), None)
    book['name'] = request.data['name']
    return Response({"book": book})


def get_authorized_user(request):
    token = request.headers['Authorization'].replace("Bearer ", '')
    return User.objects.get(accesstoken__token=token)
    

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from celery.result import AsyncResult

from ..tasks import scrape_task

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def scrape_view(request):
    user = request.user
    if not user.ke_num:
        return Response({'error': 'KE number not found'}, status=400)
    # In your view or wherever you dispatch the task
    task = scrape_task.delay(user.id)
    task_id = task.id  # This is the task ID you can store or send to the frontend

    response = {
        'message': 'Scraping initiated',
        'task_id': task_id
    }
    return Response(response, status=202)

@api_view(['GET'])
def get_task_status(request):
    task_id = request.query_params.get('task_id')
    task_result = AsyncResult(task_id)
    return Response({
        'task_id': task_id,
        'status': task_result.status,
        'result': task_result.result  # This will be None if the task is not finished
    })

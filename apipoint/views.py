from .models import TaskModel
from .serializer import TaskSerializer
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action


from rest_framework import permissions

class IsAdminOrSuperAdmin(permissions.BasePermission):
    """
    Custom permission to allow only 'admin' or 'superadmin' users.
    """
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        
        # Check if the user's role is admin or if they are a superuser
        return user.role == 'admin' or user.is_superuser



class TaskViewSet(viewsets.ModelViewSet):
    queryset = TaskModel.objects.all()
    serializer_class = TaskSerializer
    def get_queryset(self):
        user = self.request.user
        return TaskModel.objects.filter(assignedto=user)

    @action(detail=True, methods=['get'])
    def report(self, request, pk=None):
        try:
            task = TaskModel.objects.get(id=pk)
        except TaskModel.DoesNotExist:
            return Response({"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

        if task.status == 'Completed':
            task.status = 'Reported'
            task.save()
            return Response(
                {
                    'message': 'Report submitted successfully.',
                    'report': task.completionreport,
                    'worked_hours': task.workedhours
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detail": "Task must be completed before it can be reported."},
                status=status.HTTP_400_BAD_REQUEST
            )
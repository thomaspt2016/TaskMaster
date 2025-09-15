from rest_framework import serializers
from apipoint.models import TaskModel

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = ['id', 'title', 'description', 'assignedto', 'duedate', 'status', 'completionreport', 'workedhours', 'supervisor']
        read_only_fields = ['id', 'supervisor']
    
    def validate(self, attrs):
        if self.instance and self.instance.status == 'Completed':
            raise serializers.ValidationError(
                {"detail": "This task has already been completed and cannot be updated."}
            )

        status = attrs.get('status', self.instance.status if self.instance else None)
        worked_hours = attrs.get('workedhours', self.instance.workedhours if self.instance else None)
        completion_report = attrs.get('completionreport', self.instance.completionreport if self.instance else None)
        if status == 'Completed':
            if worked_hours is None or worked_hours <= 0:
                raise serializers.ValidationError(
                    {"workedhours": "Worked hours must be greater than 0 for completed tasks."}
                )
            
            if not completion_report:
                raise serializers.ValidationError(
                    {"completionreport": "A completion report is required for completed tasks."}
                )
        
        return attrs
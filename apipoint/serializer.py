from rest_framework import serializers
from apipoint.models import TaskModel

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = ['id', 'title', 'description', 'assignedto', 'duedate', 'status', 'completionreport', 'workedhours', 'supervisor']
        read_only_fields = ['id', 'supervisor']
    
    def validate(self, attrs):
        """
        Check that worked hours and a completion report are provided
        if the status is "Completed".

        """

        if self.instance and self.instance.status == 'Completed':
            if 'status' not in attrs or attrs['status'] != 'Completed':
                raise serializers.ValidationError(
                    {"detail": "This task has already been completed and cannot be updated."}
                )
        status = attrs.get('status')
        worked_hours = attrs.get('workedhours')
        completion_report = attrs.get('completionreport')

        if status == 'Completed':
            # Check for worked hours and completion report when status is completed
            if worked_hours is None or worked_hours <= 0:
                raise serializers.ValidationError(
                    {"workedhours": "Worked hours must be greater than 0 for completed tasks."}
                )
            
            if not completion_report: # Checks for empty string or None
                raise serializers.ValidationError(
                    {"completionreport": "A completion report is required for completed tasks."}
                )
        
        return attrs
        

class CompletedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = ['id','title', 'description', 'assignedto', 'duedate', 'status', 'completionreport', 'workedhours', 'supervisor']


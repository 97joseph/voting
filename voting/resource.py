from import_export import resources
from .models import Student


class StudentResource(resources.ModelResource):

    class Meta:
        model = Student
        skip_unchanged = True
        report_skipped = False
        fields = ('first_name', 'last_name', 'email', 'username', 'level', 'faculty', 'session')

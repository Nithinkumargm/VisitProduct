from django.http import JsonResponse
from rest_framework import filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Dairy, Taluk, Village, Employee, VisitType, Visit, Photo
from .serializers import DairySerializer, TalukSerializer, VillageSerializer, EmployeeSerializer, VisitTypeSerializer, VisitSerializer


class DairyAPIView(APIView):
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']

    def get(self, request, name=None):
        if name:
            dairy = Dairy.objects.filter(name__iexact=name).first()
            if not dairy:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = DairySerializer(dairy)
            return Response(serializer.data)
        else:
            queryset = Dairy.objects.all()
            serializer = DairySerializer(queryset, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = DairySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, name=None):
        dairy = Dairy.objects.filter(name__iexact=name).first()
        if not dairy:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = DairySerializer(dairy, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name=None):
        dairy = Dairy.objects.filter(name__iexact=name).first()
        if not dairy:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        dairy.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TalukAPIView(APIView):
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']

    def get(self, request, name=None):
        if name:
            taluk = Taluk.objects.filter(name__iexact=name).first()
            if not taluk:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = TalukSerializer(taluk)
            return Response(serializer.data)
        else:
            queryset = Taluk.objects.all()
            serializer = TalukSerializer(queryset, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = TalukSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, name=None):
        taluk = Taluk.objects.filter(name__iexact=name).first()
        if not taluk:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = TalukSerializer(taluk, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name=None):
        taluk = Taluk.objects.filter(name__iexact=name).first()
        if not taluk:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        taluk.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class VillageAPIView(APIView):
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'taluk__name']
    ordering_fields = ['name', 'taluk__name']

    def get(self, request, name=None, taluk_name=None):
        if name and taluk_name:
            taluk = Taluk.objects.filter(name__iexact=taluk_name).first()
            if not taluk:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            villages = Village.objects.filter(name__iexact=name, taluk=taluk)
            if not villages.exists():
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = VillageSerializer(villages, many=True)
            return Response(serializer.data)
        elif name:
            villages = Village.objects.filter(name__iexact=name)
            if not villages.exists():
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = VillageSerializer(villages, many=True)
            return Response(serializer.data)
        elif taluk_name:
            taluk = Taluk.objects.filter(name__iexact=taluk_name).first()
            if not taluk:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            villages = Village.objects.filter(taluk=taluk)
            serializer = VillageSerializer(villages, many=True)
            return Response(serializer.data)
        else:
            queryset = Village.objects.all()
            serializer = VillageSerializer(queryset, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = VillageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, name=None, taluk_name=None):
        if name and taluk_name:
            taluk = Taluk.objects.filter(name__iexact=taluk_name).first()
            if not taluk:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            villages = Village.objects.filter(name__iexact=name, taluk=taluk)
            if not villages.exists():
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

            updated_data = request.data
            for village in villages:
                serializer = VillageSerializer(village, data=updated_data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({'message': 'Updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Name and Taluk are required for update'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name=None, taluk_name=None):
        if name and taluk_name:
            taluk = Taluk.objects.filter(name__iexact=taluk_name).first()
            if not taluk:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            villages = Village.objects.filter(name__iexact=name, taluk=taluk)
            if not villages.exists():
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            villages.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'Name and Taluk are required for deletion'}, status=status.HTTP_400_BAD_REQUEST)

class EmployeeAPIView(APIView):
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'role']
    ordering_fields = ['name', 'role']

    def get(self, request, name=None, role=None):
        if name and role:
            employee = Employee.objects.filter(name__iexact=name, role__iexact=role).first()
            if not employee:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)
        else:
            queryset = Employee.objects.all()
            serializer = EmployeeSerializer(queryset, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, name=None, role=None):
        employee = Employee.objects.filter(name__iexact=name, role__iexact=role).first()
        if not employee:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name=None, role=None):
        employee = Employee.objects.filter(name__iexact=name, role__iexact=role).first()
        if not employee:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class VisitTypeAPIView(APIView):
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']

    def get(self, request, name=None):
        if name:
            visit_type = VisitType.objects.filter(name__iexact=name).first()
            if not visit_type:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = VisitTypeSerializer(visit_type)
            return Response(serializer.data)
        else:
            queryset = VisitType.objects.all()
            serializer = VisitTypeSerializer(queryset, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = VisitTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, name=None):
        visit_type = VisitType.objects.filter(name__iexact=name).first()
        if not visit_type:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = VisitTypeSerializer(visit_type, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name=None):
        visit_type = VisitType.objects.filter(name__iexact=name).first()
        if not visit_type:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        visit_type.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class VisitAPIView(APIView):
    def get(self, request, employee_name=None):
        if employee_name:
            employee = Employee.objects.filter(name__iexact=employee_name).first()
            if not employee:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            visits = Visit.objects.filter(employee=employee)
            serializer = VisitSerializer(visits, many=True)
            return Response(serializer.data)
        else:
            queryset = Visit.objects.all()
            serializer = VisitSerializer(queryset, many=True)
            return Response(serializer.data)

    def post(self, request):
        employee_name = request.data.get('employee_name')
        if not employee_name:
            return Response({"error": "Employee name is required"}, status=status.HTTP_400_BAD_REQUEST)

        employee = Employee.objects.filter(name__iexact=employee_name).first()
        if not employee:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        visit_data = request.data.copy()
        visit_data['employee'] = employee.id

        photos_data = request.FILES.getlist('photos')

        serializer = VisitSerializer(data=visit_data)
        if serializer.is_valid():
            visit = serializer.save()

            for photo_data in photos_data:
                Photo.objects.create(visit=visit, image=photo_data)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, employee_name=None):
        if not employee_name:
            return Response({"error": "Employee name is required"}, status=status.HTTP_400_BAD_REQUEST)

        employee = Employee.objects.filter(name__iexact=employee_name).first()
        if not employee:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        visit_id = request.data.get('visit_id')
        if not visit_id:
            return Response({"error": "Visit ID is required for update"}, status=status.HTTP_400_BAD_REQUEST)

        visit = Visit.objects.filter(id=visit_id, employee=employee).first()
        if not visit:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        photos_data = request.FILES.getlist('photos')

        serializer = VisitSerializer(visit, data=request.data, partial=True)
        if serializer.is_valid():
            updated_visit = serializer.save()

            updated_visit.photos.all().delete()  # Remove existing photos
            for photo_data in photos_data:
                Photo.objects.create(visit=updated_visit, image=photo_data)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, employee_name=None):
        if not employee_name:
            return Response({"error": "Employee name is required"}, status=status.HTTP_400_BAD_REQUEST)

        employee = Employee.objects.filter(name__iexact=employee_name).first()
        if not employee:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        visit_id = request.data.get('visit_id')
        if not visit_id:
            return Response({"error": "Visit ID is required for delete"}, status=status.HTTP_400_BAD_REQUEST)

        visit = Visit.objects.filter(id=visit_id, employee=employee).first()
        if not visit:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        visit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def load_taluks(request):
    employee_id = request.GET.get('employee_id')
    if employee_id:
        try:
            employee = Employee.objects.get(id=employee_id)
            taluks = employee.taluks.all()
        except Employee.DoesNotExist:
            taluks = Taluk.objects.none()
    else:
        taluks = Taluk.objects.none()

    data = list(taluks.values('id', 'name'))
    return JsonResponse(data, safe=False)

def load_villages(request):
    taluk_id = request.GET.get('taluk_id')
    if taluk_id:
        try:
            taluk = Taluk.objects.get(id=taluk_id)
            villages = Village.objects.filter(taluk=taluk).values('id', 'name')
        except Taluk.DoesNotExist:
            villages = Village.objects.none()
    else:
        villages = Village.objects.none()

    return JsonResponse(list(villages), safe=False)

def load_dairies(request):
    village_id = request.GET.get('village_id')
    if village_id:
        try:
            village = Village.objects.get(id=village_id)
            dairies = Dairy.objects.filter(village=village).values('id', 'name')
        except Village.DoesNotExist:
            dairies = Dairy.objects.none()
    else:
        dairies = Dairy.objects.none()

    return JsonResponse(list(dairies), safe=False)
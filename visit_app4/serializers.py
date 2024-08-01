from rest_framework import serializers
from .models import Dairy, Taluk, Village, Employee, VisitType, Photo, Visit

class DairySerializer(serializers.ModelSerializer):
    village = serializers.SlugRelatedField(queryset=Village.objects.all(), slug_field='name')

    class Meta:
        model = Dairy
        fields = '__all__'

    def validate(self, data):
        village = data['village']
        name = data['name']
        if Dairy.objects.filter(name__iexact=name, village=village).exclude(
                id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError(
                f"A dairy with the name '{name}' already exists in the village '{village.name}'.")
        return data

class TalukSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taluk
        fields = '__all__'

class VillageSerializer(serializers.ModelSerializer):
    taluk = serializers.SlugRelatedField(queryset=Taluk.objects.all(), slug_field='name')

    class Meta:
        model = Village
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    taluks = serializers.SlugRelatedField(queryset=Taluk.objects.all(), slug_field='name', many=True)

    class Meta:
        model = Employee
        fields = ['id', 'name', 'role', 'taluks']

    def create(self, validated_data):
        taluks_data = validated_data.pop('taluks')
        employee = Employee.objects.create(**validated_data)
        employee.taluks.set(taluks_data)
        return employee

    def update(self, instance, validated_data):
        taluks_data = validated_data.pop('taluks', None)
        instance.name = validated_data.get('name', instance.name)
        instance.role = validated_data.get('role', instance.role)
        instance.save()

        if taluks_data is not None:
            instance.taluks.set(taluks_data)
        return instance

class VisitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitType
        fields = ['id', 'name']

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['image', 'date_taken', 'gps']


class VisitSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, required=False)
    visit_types = serializers.SlugRelatedField(
        queryset=VisitType.objects.all(), slug_field='name', many=True, required=False)
    employee = serializers.SlugRelatedField(
        queryset=Employee.objects.all(), slug_field='name')
    taluk = serializers.SlugRelatedField(
        queryset=Taluk.objects.all(), slug_field='name')
    village = serializers.SerializerMethodField()
    dairy = serializers.SlugRelatedField(
        queryset=Dairy.objects.all(), slug_field='name')

    class Meta:
        model = Visit
        fields = '__all__'

    def get_village(self, obj):
        village = Village.objects.get(name=obj.village.name, taluk=obj.taluk)
        return VillageSerializer(village).data

    def create(self, validated_data):
        photos_data = self.context['request'].FILES.getlist('photos')
        visit_types_data = validated_data.pop('visit_types', [])
        village_name = self.context['request'].data.get('village')
        taluk = validated_data['taluk']

        validated_data['village'] = Village.objects.get(name=village_name, taluk=taluk)

        visit = Visit.objects.create(**validated_data)
        for photo_data in photos_data:
            Photo.objects.create(visit=visit, image=photo_data)
        visit.visit_types.set(visit_types_data)
        return visit

    def update(self, instance, validated_data):
        photos_data = self.context['request'].FILES.getlist('photos')
        visit_types_data = validated_data.pop('visit_types', [])
        village_name = self.context['request'].data.get('village')
        taluk = validated_data['taluk']

        validated_data['village'] = Village.objects.get(name=village_name, taluk=taluk)

        instance.summary = validated_data.get('summary', instance.summary)
        instance.gps = validated_data.get('gps', instance.gps)
        instance.employee = validated_data.get('employee', instance.employee)
        instance.taluk = validated_data.get('taluk', instance.taluk)
        instance.village = validated_data.get('village', instance.village)
        instance.dairy = validated_data.get('dairy', instance.dairy)
        instance.save()

        instance.photos.all().delete()
        for photo_data in photos_data:
            Photo.objects.create(visit=instance, image=photo_data)
        instance.visit_types.set(visit_types_data)
        return instance

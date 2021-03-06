from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.validators import ValidationError
from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""
        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        method = self.context["request"].method
        all_subj = Advertisement.objects.filter(creator=self.context["request"].user)\
            .filter(status='OPEN').count() + 1
        print(f'ALL SUBJ {all_subj}')
        if method == 'POST':
            try:
                if data['status'] == 'OPEN':
                    if all_subj > 10:
                        raise ValidationError('Слишком много активных объявлений!')
            except KeyError:
                if all_subj > 10:
                    raise ValidationError('Слишком много активных объявлений!')
        elif method == 'PATCH':
            try:
                if data['status'] == 'OPEN':
                    if all_subj > 10:
                        raise ValidationError('Слишком много активных объявлений!')
            except KeyError:
                pass

        return data



from rest_framework import serializers
from notes.models import NeofiUser, Note, NoteEdit, NoteShare

class NeofiUserSignupSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = NeofiUser
        fields = ['email', 'username', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        # return super().create(validated_data)
        return NeofiUser.objects.create_user(**validated_data)
    
class NeofiUserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = NeofiUser
        fields = ['email', 'password']

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'content', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class NoteEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteEdit
        fields = ['note', 'previous_content', 'edited_content', 'edited_by', 'edit_timestamp']


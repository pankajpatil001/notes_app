from rest_framework import serializers
from notes.models import NeofiUser, Note, NoteEdit

class NeofiUserSignupSerializer(serializers.ModelSerializer):
    """
    Serializer for user signup.
    """

    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = NeofiUser
        fields = ['email', 'username', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        """
        Validate password and confirm_password fields.
        """
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        """
        Create a new user.
        """
        validated_data.pop('confirm_password')
        # return super().create(validated_data)
        return NeofiUser.objects.create_user(**validated_data)
    
class NeofiUserLoginSerializer(serializers.ModelSerializer):
    """
    Serializer for user login.
    """

    email = serializers.EmailField(max_length=255)
    class Meta:
        model = NeofiUser
        fields = ['email', 'password']

class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer for Note model.
    """

    class Meta:
        model = Note
        fields = ['id', 'content', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class NoteEditSerializer(serializers.ModelSerializer):
    """
    Serializer for NoteEdit model.
    """
    
    class Meta:
        model = NoteEdit
        fields = ['note', 'previous_content', 'edited_content', 'edited_by', 'edit_timestamp']


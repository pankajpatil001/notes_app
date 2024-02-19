from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from notes.models import NeofiUser, Note, NoteEdit, NoteShare
from rest_framework.authtoken.models import Token
from notes.serializers import NeofiUserSignupSerializer, NeofiUserLoginSerializer, NoteSerializer, NoteEditSerializer #, NoteShareSerializer


@api_view(['POST'])
def signup(request):
    """
    Signup a new user with custom user model.

    Method: POST
    URL: /signup/

    Required parameters in request.data:
        - email: Valid email address of the user to be signed up.
        - username: Username for the user.
        - password: Password for the user.
        - confirm_password: Repeat the password for the user.

    Returns:
        - Response with status code 201 CREATED and success message if the user signup is successful.
        - Response with status code 400 BAD REQUEST and the errors if:
            - Email address is not valid,
            - User with given email address already exists,
            - Any of the above parameters is missing,
            - Both the passwords do not match
        - Response with status code 405 METHOD NOT ALLOWED if the request is made with any method other than POST
    """
    serializer = NeofiUserSignupSerializer(data=request.data) # create the serializer with incoming data
    if serializer.is_valid():
        serializer.save() # save the user once it is validated
        return Response({'message': 'User signup successful.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    """
    Login a valid user.

    Method: POST
    URL: /login/
    Required parameters in request.data:
        - email: Valid email address of the user to be logged in.
        - password: Password for the user.

    Returns:
        - Response with status code 200 OK and success message if the user signup is successful.
            - User details including username and email,
            - 'token' which can be used in other requests for authentication.
        - Response with status code 401 UNAUTHORIZED and the errors if:
            - Email address is not valid,
            - Password is not valid,
            - Any of the above parameters is missing
        - Response with status code 405 METHOD NOT ALLOWED if the request is made with any method other than POST
    """
    serializer = NeofiUserLoginSerializer(data=request.data) # create the serializer with incoming data
    print('Serializer:', serializer)
    if serializer.is_valid():
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password) # authenticate the user with given credentials
        if user is not None: 
            token, created = Token.objects.get_or_create(user=user) # create a token if the user is authenticated
            return Response({'message': 'User login successful.', 'user': {'email': user.email, 'username': user.username}, 'token': token.key}, status=status.HTTP_200_OK)
        return Response({'message': 'User login failed', 'errors': 'Email or Password is not valid.'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_notes(request):
    """
    Create a new note for the authenticated user.

    Method: POST
    URL: /notes/create/

    Required HTTP Headers:
        - Authorization: Token 91a2daac859262cc4560b2706b2579ddc44bc79e

    Required parameters in request.data:
        - content: the content of the note (string)

    Returns:
        - Response with status code 201 CREATED and success message if the note creation is successful
            - message: Note creation successful.
            - note_id: id of the note created.
            - owner: email and username of the owner of the note
        - Response with status code 400 BAD REQUEST and the errors if:
            - content is not a string,
            - content is not present
        - Response with status code 401 UNAUTHORIZED if:
            - Authentication token is not provided
        - Response with status code 405 METHOD NOT ALLOWED if the request is made with any method other than POST
    """
    serializer = NoteSerializer(data=request.data) # create the serializer with incoming data
    if not serializer.is_valid(): # return 400 if incoming data is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save(owner=request.user) # save the note if data is valid
    note_id = serializer.data.get('id')
    NoteShare.objects.create(note_id=note_id, user=request.user) # create a note share object with the given note and user
    NoteEdit.objects.create(note_id=note_id, edited_by=request.user, previous_content='', edited_content=serializer.data.get('content')) # create a note edit object with given note and other details
    return Response({'message': 'Note creation successful.', 'note_id': note_id, 'owner': {'email': request.user.email, 'username': request.user.username}}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def share_note(request):
    """
    Share a note with other users (by authenticated owner).

    Method: POST
    URL: /notes/share/

    Required HTTP Headers:
        - Authorization: Token 91a2daac859262cc4560b2706b2579ddc44bc79e

    Required parameters in request.data:
        - note_id: id of the note to be shared
        - user_ids: list of ids of the users to share note with

    Returns:
        - Response with status code 200 OK and success message if the note sharing is successful
            - message: Note share successful.

        - Response with status code 400 BAD REQUEST and the error message if:
            - any of the required parameters is missing,

        - Response with status code 401 UNAUTHORIZED if:
            - Authentication token is not provided
            - The authenticated user is not the owner of the note

        - Response with status code 405 METHOD NOT ALLOWED if the request is made with any method other than POST
    """
    note_id = request.data.get('note_id')
    user_ids = request.data.get('user_ids')
    if not note_id or not isinstance(user_ids, list) or not user_ids: # if note_id or user_ids are not valid, return 400 with the error message
        return Response({'message': 'Note id and list of User ids are needed for sharing a note'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        note = Note.objects.get(id=note_id, owner=request.user) # save the note with the logged in user
    except Note.DoesNotExist:
        return Response({'message': 'You are not authorized to share this note.'}, status=status.HTTP_401_UNAUTHORIZED)

    print('Note:', note)
    user_notes = []
    non_existent_users = []
    for user_id in user_ids: # share the note with all ids mentioned in user_ids list
        try:
            user = NeofiUser.objects.get(id=user_id)
            if not NoteShare.objects.filter(note_id=note_id, user=user).exists(): # to avoid duplicacy of note share object
                user_notes.append(NoteShare(note_id=note_id, user=user))
        except NeofiUser.DoesNotExist:
            non_existent_users.append(str(user_id))
    
    if not non_existent_users: # create all note share objects only if all users in the user_ids list are valid
        NoteShare.objects.bulk_create(user_notes)
    else: # else give the list of invalid user ids
        return Response({'message': f'Users do not exist for user id(s): {", ".join(non_existent_users)}'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'message': 'Note share successful.'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def note_version_history(request, id):
    """
    Get the version history of a note (by authenticated owner).

    Method: GET
    URL: /notes/version-history/{note-id}/

    Required HTTP Headers:
        - Authorization: Token 91a2daac859262cc4560b2706b2579ddc44bc79e

    Required parameters in url:
        - note_id: id of the note for getting the version history

    Returns:
        - Response with status code 200 OK and list of edits which include:
            - note: id of the note,
            - previous_content: content prior to editing (blank if it has not been edited after creation),
            - edited_content: edited content,
            - edited_by: id of the user who edited the note,
            - edit_timestamp: timestamp when the note was edited

        - Response with status code 401 UNAUTHORIZED if:
            - Authentication token is not provided
            - The authenticated user is not the owner of the note
            
        - Response with status code 405 METHOD NOT ALLOWED if the request is made with any method other than GET
    """
    shared_notes = NoteShare.objects.filter(note_id=id, user=request.user) # check if the note is shared with the logged in user
    if not shared_notes.exists():
        return Response({'message': 'You are not authorized to view the version history for this note.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        note = Note.objects.get(id=id)
    except Note.DoesNotExist:
        return Response({'message': 'Note does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    
    note_versions = NoteEdit.objects.filter(note=note) # get the version history for the note
    serializer = NoteEditSerializer(note_versions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class NoteRetriveUpdate(APIView):
    """
    Retrieve, update and delete a note (by authenticated user).
    """
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        """
            For retrieving a note:
            Method: GET
            URL: /notes/{note-id}/

            Required HTTP Headers:
                - Authorization: Token 91a2daac859262cc4560b2706b2579ddc44bc79e

            Required parameters in url:
                - note-id: id of the note for getting the content of the note

            Returns:
                - Response with status code 200 OK and:
                    - id: id of the note,
                    - content: current content of the note,
                    - created_at: timestamp when the note was created,
                    - updated_at: timestamp when the note was updated

                - Response with status code 404 NOT FOUND if:
                    - the note with given id does not exist

                - Response with status code 401 UNAUTHORIZED if:
                    - Authentication token is not provided
                    - The authenticated user is either not the owner of the note or the note is not shared with this user
                    
                - Response with status code 405 METHOD NOT ALLOWED if the request is made with any method other than GET
        """
        try:
            note = Note.objects.get(id=id)
        except Note.DoesNotExist:
            return Response({'message': 'Note does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        shared_notes = NoteShare.objects.filter(note_id=id, user=request.user)
        
        if shared_notes.exists(): # check if the note is shared with the logged in user
            serializer = NoteSerializer(note)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'You are not authorized to view the note.'}, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, id):
        """
            For updating a note:
            Method: PUT
            URL: /notes/{note-id}/

            Required HTTP Headers:
                - Authorization: Token 91a2daac859262cc4560b2706b2579ddc44bc79e

            Required parameters in url:
                - note-id: id of the note for updating the content of the note

            Required parameters in request.data:
                - content: additional lines in the note (after existing lines)

            Returns:
                - Response with status code 200 OK and success message if the updation is successful:
                    - id: id of the note updated,
                    - content: current content of the note,
                    - created_at: timestamp when the note was created,
                    - updated_at: timestamp when the note was updated

                - Response with status code 400 BAD REQUEST if:
                    - the content is not a string

                - Response with status code 403 FORBIDDEN if:
                    - the content is not an extension to the previous note (only new lines can be added, existing ones cannot be edited or removed.)

                - Response with status code 404 NOT FOUND if:
                    - the note with given id does not exist

                - Response with status code 401 UNAUTHORIZED if:
                    - Authentication token is not provided
                    - The authenticated user is either not the owner of the note or the note is not shared with this user
                    
                - Response with status code 405 METHOD NOT ALLOWED if the request is made with any method other than GET
        """
        try:
            note = Note.objects.get(id=id)
        except Note.DoesNotExist:
            return Response({'message': f"Note does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        shared_notes = NoteShare.objects.filter(note_id=id, user=request.user)
        
        if not shared_notes.exists(): # check if the note is shared with the logged in user
            return Response({'message': 'You are not authorized to edit the note.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = NoteSerializer(note, data=request.data)
        if not serializer.is_valid(): # check if the note is valid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        edited_note = request.data.get('content', '')
        previous_content = note.content
        
        if not edited_note.startswith(previous_content): # existing note content cannot be edited, but only appended
            return Response({'message': 'Note update failed.', 'error': 'You can only add the new lines after the existing lines.'}, status=status.HTTP_403_FORBIDDEN)
        
        note.content = edited_note
        note.save() # save the note with the change
        context = {
            'note': note.id,
            'previous_content': previous_content,
            'edited_content': edited_note,
            'edited_by': request.user.id
            }
        note_edit_serializer = NoteEditSerializer(data=context) # create an entry for version history
        if not note_edit_serializer.is_valid():
            return Response({'message': 'Note update successful but saving note versions history failed.', 'error': 'Failed to save note version history.'}, status=status.HTTP_206_PARTIAL_CONTENT)

        note_edit_serializer.save()
        return Response({'message': 'Note update successful.', 'data': serializer.data}, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        """
            For deleting a note:
            Method: DELETE
            URL: /notes/{note-id}/

            Required HTTP Headers:
                - Authorization: Token 91a2daac859262cc4560b2706b2579ddc44bc79e

            Required parameters in url:
                - note-id: id of the note to be deleted

            Returns:
                - Response with status code 204 NO CONTENT if the deletion is successful

                - Response with status code 404 NOT FOUND if:
                    - the note with given id does not exist

                - Response with status code 401 UNAUTHORIZED if:
                    - Authentication token is not provided
                    - The authenticated user is either not the owner of the note or the note is not shared with this user

                - Response with status code 405 METHOD NOT ALLOWED if the request is made with any method other than DELETE
        """
        try:
            note = Note.objects.get(id=id)

        except Note.DoesNotExist:
            return Response({'message': f"Note does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        shared_notes = NoteShare.objects.filter(note_id=id, user=request.user)
        
        if not shared_notes.exists(): # check if the note is shared with the logged in user
            return Response({'message': 'You are not authorized to delete the note.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Delete note and related items
        note.delete()
        NoteShare.objects.filter(note_id=id).delete()
        NoteEdit.objects.filter(note_id=id).delete()
        
        return Response({'message': 'Note deleted'}, status=status.HTTP_204_NO_CONTENT)

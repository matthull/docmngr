from django.db.models import Q
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from docmngr.models import Document, DocumentSerializer, Folder, FolderSerializer


class FoldersView(APIView):
    @staticmethod
    def _folder_objects():
        """Get a folder manager that excludes deleted objects.

        We won't show those in the API.
        """
        return Folder.without_deleted()

    def get(self, request, pk=None):
        """Returns a folder along with its children.

        If no parent is supplied, return the top folders in the hierarchy.

        This is intended to be convenient for a client application that
        will be browsing the folder hierarchy from the top down.

        If a matching folder exists: Returns 200
        If a matching folder does not exist: Returns 404
        If no pk was specified and no folders exist: Returns 200
        """
        if pk:
            folders = self._folder_objects().filter(Q(pk=pk) | Q(parent_folder=pk))
        else:
            folders = self._folder_objects().filter(parent_folder=None)

        if not folders.exists() and pk is not None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = FolderSerializer(folders, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Create a new folder.

        If folder was successfully created: Returns 201 and created folder
        If folder was not created due to validation errors: Returns 400 and list of errors
        """

        serializer = FolderSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """Change a folder's attributes.

        If change was successful: Returns 200 and updated folder
        If folder does not exist or was deleted: Return 404
        If change failed due to validation errors: Returns 400 and list of errors
        """
        try:
            folder = self._folder_objects().get(pk=pk)
        except Folder.DoesNotExist:
            raise Http404

        serializer = FolderSerializer(folder, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocumentsView(APIView):
    @staticmethod
    def _document_objects():
        """Get a document manager that excludes deleted objects.

        We won't show those in the API.
        """
        return Document.without_deleted()

    def get(self, request, pk):
        """Gets a single document."""
        try:
            document = self._document_objects().get(pk=pk)
        except Document.DoesNotExist:
            raise Http404

        document = self._document_objects().get(pk=pk)
        serializer = DocumentSerializer(document)

        return Response(serializer.data)

    def put(self, request, pk):
        """Change a document's attributes.

        If change was successful: Returns 200 and updated document
        If document does not exist or was deleted: Return 404
        If change failed due to validation errors: Returns 400 and list of errors
        """
        try:
            document = self._document_objects().get(pk=pk)
        except document.DoesNotExist:
            raise Http404

        serializer = DocumentSerializer(document, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

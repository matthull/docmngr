from abc import ABC, abstractmethod, abstractproperty

from django.db.models import Q
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from docmngr.models import Document, DocumentSerializer, Folder, FolderSerializer


class BaseView(APIView, ABC):
    """This base view contains the common logic that's used across various concrete views."""

    @staticmethod
    @abstractmethod
    def _get_objects():
        """Get a queryset for the main model this view does CRUD on.

        Should return a Django QuerySet.
        """

    @staticmethod
    @abstractproperty
    def serializer_class():
        """The DRF serializer class associated with this view's main model."""

    @staticmethod
    @abstractproperty
    def model_class():
        """The Django model class associated with this view's main model."""

    def post(self, request):
        """Create a new object.

        If object was successfully created: Returns 201 and created object
        If object was not created due to validation errors: Returns 400 and list of errors
        """

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """Change an object's attributes.

        If change was successful: Returns 200 and updated folder
        If object does not exist or was deleted: Return 404
        If change failed due to validation errors: Returns 400 and list of errors
        """
        try:
            obj = self._get_objects().get(pk=pk)
        except self.model_class.DoesNotExist:
            raise Http404

        serializer = self.serializer_class(obj, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FoldersView(BaseView):
    model_class = Folder
    serializer_class = FolderSerializer

    @staticmethod
    def _get_objects():
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
            folders = self._get_objects().filter(Q(pk=pk) | Q(parent_folder=pk))
        else:
            folders = self._get_objects().filter(parent_folder=None)

        if not folders.exists() and pk is not None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(folders, many=True)
        return Response(serializer.data)


class DocumentsView(BaseView):
    serializer_class = DocumentSerializer
    model_class = Document

    @staticmethod
    def _get_objects():
        """Get a document manager that excludes deleted objects.

        We won't show those in the API.
        """
        return Document.without_deleted()

    def get(self, request, pk):
        """Gets a single document."""
        try:
            document = self._get_objects().get(pk=pk)
        except Document.DoesNotExist:
            raise Http404

        serializer = self.serializer_class(document)

        return Response(serializer.data)

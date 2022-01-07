from django.db import models

from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


# #########################
# ####     Folders      ###
# #########################


class Folder(models.Model):
    """Part of a nested hierarchy organizing documents."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=240, blank=False, unique=True, null=False)
    parent_folder = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, related_name="children"
    )
    is_deleted = models.BooleanField(default=False)

    @classmethod
    def without_deleted(self):
        """Returns a queryset that doesn't include delete folders.

        Rationale: From many perspectives like the client API we treat deleted
        folders like they don't exist

        Example: Folder.filtered_objects.filter(parent_folder=parent_folder)
        """
        return self.objects.filter(is_deleted=False)


class FolderSerializer(BaseSerializer):
    def create(self, data):
        return Folder.objects.create(**data)

    class Meta:
        model = Folder
        fields = ["id", "name", "parent_folder", "created_at", "updated_at"]


# #########################
# ####    Documents     ###
# #########################


class Document(models.Model):
    """Stores a user-created rich text document.

    The end user creates and modifies documents using a rich text editor. A document generally
    contains some operational information that helps people do their jobs
    e.g. a procedure on how to use a piece of software.
    """

    @classmethod
    def without_deleted(self):
        """Returns a queryset that doesn't include deleted documents.

        Rationale: From many perspectives like the client API we treat deleted
        documents like they don't exist

        Example: Document.filtered_objects.filter(folder=folder)
        """
        return self.objects.filter(is_deleted=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=240, blank=False)
    content = models.TextField(blank=False)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)


class DocumentSerializer(BaseSerializer):
    class Meta:
        model = Document
        fields = ["id", "title", "content", "folder", "created_at", "updated_at"]

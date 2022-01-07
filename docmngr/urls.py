"""docmngr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

from docmngr import views

urlpatterns = [
    path(
        "openapi",
        get_schema_view(
            title="Doc Manager API",
            description="API that manages docs",
            version="0.1.0",
        ),
        name="openapi-schema",
    ),
    path(
        "swagger-ui/",
        TemplateView.as_view(
            template_name="swagger-ui.html",
            extra_context={"schema_url": "openapi-schema"},
        ),
        name="swagger-ui",
    ),
    path("folders/", views.FoldersView.as_view()),
    path("folders/<int:pk>/", views.FoldersView.as_view()),
    path("folders/<int:folder_pk>/documents/", views.get_documents_for_folder),
    path("documents/<int:pk>/", views.DocumentsView.as_view()),
    path("documents/", views.DocumentsView.as_view()),
    path("topics/<int:pk>/", views.TopicsView.as_view()),
    path("topics/<int:topic_pk>/documents/", views.get_documents_for_topic),
    path("topics/", views.TopicsView.as_view()),
    path(
        "documents/<int:document_pk>/topics/<int:topic_pk>/",
        views.modify_document_topics,
    ),
]

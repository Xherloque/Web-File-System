from django.urls import path
from . import views

app_name = "files"

urlpatterns = [
    path('', views.list_folders, name='list_folders'),
    path('create-folder/', views.create_folder, name='create_folder'),
    path('upload-file/', views.upload_file, name='upload_file_no_folder'),  # No folder ID
    path('upload-file/<int:folder_id>/', views.upload_file, name='upload_file'),  # With folder ID
    path('folder/<int:folder_id>/', views.list_files, name='list_files'),
    path('delete-folder/', views.delete_folder, name='delete_folder_no_folder'),  # No folder ID
    path('delete-folder/<int:folder_id>/', views.delete_folder, name='delete_folder'),
    path('rename-folder/<int:folder_id>/', views.rename_folder, name='rename_folder'),
    path('rename-folder/', views.rename_folder, name='rename_folder_no_folder'),  # No folder ID
    path('delete-file/<int:file_id>/', views.delete_file, name='delete_file'),
    path('delete-file/', views.delete_file, name='delete_file_no_file'),  # No folder ID
    path('rename-file/<int:file_id>/', views.rename_file, name='rename_file'),
    path('rename-file/', views.rename_file, name='rename_file_no_file'),  # No folder ID
    path('trash/', views.trash, name='trash'),
    path('restore-folder/<int:folder_id>/', views.restore_folder, name='restore_folder'),
    path('restore-file/<int:file_id>/', views.restore_file, name='restore_file'),
    path('permanently-delete-folder/<int:folder_id>/', views.permanently_delete_folder, name='permanently_delete_folder'),
    path('permanently-delete-file/<int:file_id>/', views.permanently_delete_file, name='permanently_delete_file'),
    path('ajax/delete-folder/<int:folder_id>/', views.ajax_delete_folder, name='ajax_delete_folder'),
    path('ajax/rename-folder/<int:folder_id>/', views.ajax_rename_folder, name='ajax_rename_folder'),
    path('ajax/delete-file/<int:file_id>/', views.ajax_delete_file, name='ajax_delete_file'),

]

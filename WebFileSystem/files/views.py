from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Folder, UploadedFile
from .forms import FolderForm, FileUploadForm
from django.contrib import messages
from django.utils.timezone import now
from django.http import JsonResponse
import psutil

@login_required
def list_folders(request):
    folders = Folder.objects.filter(user=request.user, parent_folder__isnull=True, is_deleted=False)
    return render(request, 'files/list_folders.html', {'folders': folders})

@login_required
def create_folder(request):
    """
    Handles the creation of new folders for the logged-in user.
    """
    if request.method == "POST":
        form = FolderForm(request.POST)
        if form.is_valid():
            # Save the folder, ensuring it's linked to the logged-in user
            folder = form.save(commit=False)
            folder.user = request.user
            folder.save()
            messages.success(request, "Folder created successfully!")
            return redirect('files:list_folders')
        else:
            messages.error(request, "Failed to create folder. Please try again.")
    else:
        form = FolderForm()
    
    # Fetch only the folders belonging to the current user
    user_folders = Folder.objects.filter(user=request.user)
    
    return render(request, 'files/create_folder.html', {'form': form, 'folders': user_folders})



@login_required
def upload_file(request, folder_id=None):
    """
    Handles file uploads. If no folder_id is provided, upload to the default folder.
    """
    # Handle case where folder_id is None
    folder = None
    if folder_id:
        folder = get_object_or_404(Folder, id=folder_id, user=request.user)
    else:
        folder, created = Folder.objects.get_or_create(user=request.user, name="Default Folder")

    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.folder = folder
            uploaded_file.user = request.user
            uploaded_file.original_name = request.FILES['file'].name
            uploaded_file.save()
            messages.success(request, "File uploaded successfully!")
            return redirect('files:list_folders')  # Redirect after success
        else:
            messages.error(request, "Failed to upload file. Please check the form.")
    else:
        form = FileUploadForm(initial={'folder': folder})

    return render(request, 'files/upload_file.html', {'form': form, 'folder': folder})



@login_required
def delete_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)
    folder.subfolders.update(is_deleted=True, deleted_at=now())
    folder.files.update(is_deleted=True, deleted_at=now())
    folder.is_deleted = True
    folder.deleted_at = now()
    folder.save()
    messages.success(request, f"Folder '{folder.name}' moved to Trash.")
    return redirect('/')

@login_required
def rename_folder(request, folder_id = None):
    folder = None
    if folder_id:
        folder = get_object_or_404(Folder, id=folder_id, user=request.user)
    else:
        pass
    if request.method == 'POST':
        new_name = request.POST.get('name')
        if new_name:
            folder.name = new_name
            folder.save()
            messages.success(request, f"Folder renamed to '{new_name}'.")
            return redirect('/')
    return render(request, 'files/rename_folder.html', {'folder': folder})


@login_required
def list_files(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)
    subfolders = folder.subfolders.filter(is_deleted=False)  # Exclude deleted subfolders
    files = folder.files.filter(is_deleted=False)  # Exclude deleted files

    # Check if the folder has any files
    if not files:
        message = "This folder is empty."
    else:
        message = None

    return render(request, 'files/list_files.html', {
        'folder': folder,
        'subfolders': subfolders,
        'files': files,
        'message': message,
    })



@login_required
def delete_file(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id, folder__user=request.user)
    file.mark_as_deleted()
    messages.success(request, f"File '{file.original_name}' moved to Trash.")
    return redirect('files:list_folders')

@login_required
def rename_file(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id, folder__user=request.user)
    if request.method == 'POST':
        new_name = request.POST.get('name')
        if new_name:
            file.name = new_name
            file.save()
            messages.success(request, f"File renamed to '{new_name}'.")
            return redirect('files:list_folders')
    return render(request, 'files/rename_file.html', {'file': file})

@login_required
def trash(request):
    folders = Folder.objects.filter(user=request.user, is_deleted=True)
    files = UploadedFile.objects.filter(folder__user=request.user, is_deleted=True)
    return render(request, 'files/trash.html', {'folders': folders, 'files': files})

@login_required
def restore_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user, is_deleted=True)
    folder.is_deleted = False
    folder.deleted_at = None
    folder.save()
    messages.success(request, f"Folder '{folder.name}' restored.")
    return redirect('files:trash')

@login_required
def restore_file(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id, folder__user=request.user, is_deleted=True)
    file.restore()
    messages.success(request, f"File '{file.name}' restored.")
    return redirect('files:trash')

@login_required
def permanently_delete_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user, is_deleted=True)
    folder.delete()
    messages.success(request, f"Folder '{folder.name}' permanently deleted.")
    return redirect('files:trash')

@login_required
def permanently_delete_file(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id, folder__user=request.user, is_deleted=True)
    file.delete()
    messages.success(request, f"File '{file.name}' permanently deleted.")
    return redirect('files:trash')


@staff_member_required
def system_monitoring(request):
    # Get system statistics
    disk_usage = psutil.disk_usage('/')
    cpu_usage = psutil.cpu_percent(interval=1)

    context = {
        'disk_total': disk_usage.total // (1024 ** 3),  # Total disk space in GB
        'disk_used': disk_usage.used // (1024 ** 3),   # Used disk space in GB
        'disk_free': disk_usage.free // (1024 ** 3),   # Free disk space in GB
        'disk_percent': disk_usage.percent,           # Disk usage percentage
        'cpu_percent': cpu_usage,                     # CPU usage percentage
    }
    return render(request, 'files/system_monitoring.html', context)


# AJAX folder deletion view
def ajax_delete_folder(request, folder_id):
    if request.method == "POST" and request.user.is_authenticated:
        # Fetch the folder object
        folder = get_object_or_404(Folder, id=folder_id, user=request.user)
        
        # Delete the folder and its contents
        folder.delete()
        
        # Return a JSON response indicating success
        return JsonResponse({"success": True, "message": "Folder deleted successfully."})
    
    # If request is invalid or user is not authenticated
    return JsonResponse({"success": False, "message": "Invalid request."})



# AJAX folder renaming view
def ajax_rename_folder(request, folder_id):
    if request.method == "POST" and request.user.is_authenticated:
        new_name = request.POST.get("new_name")
        if new_name:
            folder = get_object_or_404(Folder, id=folder_id, user=request.user)
            folder.name = new_name
            folder.save()
            return JsonResponse({"success": True, "message": "Folder renamed successfully."})
        return JsonResponse({"success": False, "message": "Invalid folder name."})
    return JsonResponse({"success": False, "message": "Invalid request."})


# AJAX file deletion view
def ajax_delete_file(request, file_id):
    if request.method == "POST" and request.user.is_authenticated:
        # Get the file object
        file = get_object_or_404(UploadedFile, id=file_id, user=request.user)
        
        # Delete the file
        file.delete()
        
        return JsonResponse({"success": True, "message": "File deleted successfully."})
    
    return JsonResponse({"success": False, "message": "Invalid request."})


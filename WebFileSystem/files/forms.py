from django import forms
from .models import Folder, UploadedFile

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name', 'parent_folder']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'parent_folder': forms.Select(attrs={'class': 'form-control'}),
        }

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['folder', 'file']
        widgets = {
            'folder': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

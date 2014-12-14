# -*- coding: utf-8 -*-
from django import forms

class DocumentForm(forms.Form):
	docfile = forms.FileField(
		label='Select a file'
	)
	docfile1 = forms.FileField(
		label='Select a file 2'
	)
	docfile2 = forms.FileField(
		label='Select a file 3'
	)
	docfile3 = forms.FileField(
	label='Select a file 4'
	)
	docfile4 = forms.FileField(
		label='Select a file 5'
	)

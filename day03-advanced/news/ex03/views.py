from django.shortcuts import redirect
from django.utils.translation import activate
from django.views import View


class SetLanguageView(View):
    ALLOWED_LANGUAGES = ['en', 'fr', 'es']
    
    def get(self, request, language_code):
        if language_code in self.ALLOWED_LANGUAGES:
            activate(language_code)
            request.session['django_language'] = language_code
        
        return redirect('articles')

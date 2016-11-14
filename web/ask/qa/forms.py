from django import forms
from qa.models import Question, Answer

class AskForm(forms.Form):
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    def save(self):
        question = Question(**self.cleaned_data)
        question.author_id = 1 # TODO hardcoded for now
        question.save()
        return question

class AnswerForm(forms.Form):
    text = forms.CharField(label='Your answer', widget=forms.Textarea(attrs={'class': 'form-control'}))
    question = forms.IntegerField(widget=forms.HiddenInput)

    def clean_question(self):
        question = self.cleaned_data['question']
        try:
            if int(question) < 1:
                raise ValueError
            question = Question.objects.get(id=question)
        except (Question.DoesNotExist, ValueError):
            raise ValidationError(u'Incorrect question ID', code="qid_error")

        return question

    def save(self):
        answer = Answer(**self.cleaned_data)
        answer.author_id = 2 # TODO hardcoded for now
        answer.save()
        return answer

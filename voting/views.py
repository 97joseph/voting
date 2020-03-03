from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from .models import *
from .forms import *
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.contrib.auth import logout
from .decorators import admin_required, student_required
from django.http import JsonResponse




# Admin Dashboard when they logs in

@login_required
def home(request):
    
    if request.user.is_student == False:
        students = Student.objects.all().count()
        total_votes = Student.objects.filter(has_voted=True).count()
        candidates = Candidate.objects.all().count()
        position = Position.objects.all().count()
        
        context = {
            "total_votes": total_votes, 
            "candidates": candidates, 
            "position": position,
            "students": students, 
        }

        return render(request, 'db/dashboard.html', context)
    
    else:
        return redirect('election_home')


# DISPLAYS STUDENT LIST ON THE ADMINS PAGE
@method_decorator([login_required, admin_required], name="dispatch")
class StudentList(ListView):
    
    

    template = 'stu/student_list.html'
    context_object_name = 'students'

    def get_queryset(self):
        return Student.objects.all()


# CREATE STUDENT ON THE ADMINS PAGE
@method_decorator([login_required, admin_required], name="dispatch")
class StudentCreate(CreateView):
    model = Student
    form_class = StudentAddForm
    template_name = 'voting/student_form.html'
    
    def form_valid(self, form):
        user = form.save()
        return redirect('student-list')


# CREATES POSITION ON THE ADMINS PAGE
@method_decorator([login_required, admin_required], name="dispatch")
class PositionCreate(CreateView):
    model = Position
    fields = ['election', 'text']


# DISPLAYS POSITION LIST ON THE ADMINS PAGE
@login_required
@admin_required()
def position_list(request):
    """ Show list of all registered Positions in the system """
    positions = Position.objects.all()
    context = {
        "positions": positions, 
        }
    return render(request, 'voting/position_list.html', context)


# CREATES CANDIDATE ON THE ADMINS PAGE
@method_decorator([login_required, admin_required], name="dispatch")
class CandidateCreate(CreateView):
    model = Candidate
    fields = ['position', 'name', 'level', 'faculty', 'picture', 'election']


@login_required
@admin_required()
def candidate_list(request):
    """ Show list of all registered Positions in the system """
    candidates = Candidate.objects.all()
    context = {
        "candidates": candidates, 
        }
    return render(request, 'voting/candidate_list.html', context)

# get election and show them
@login_required
def election_home(request):

    # check if user is a student, if so, display current polls
    if request.user.is_student == True:

        # check if student has already voted,
        # if so logs them out and return to results page

        if request.user.student.has_voted == False:
            latest = Election.objects.order_by('id')
            context = {'latest': latest,}
            return render(request, 'stu/election.html', context)

        else:
            
            logout_view(request)
            return redirect('live')
        
    else:
        return redirect('home')
    

# view candidates for verified user to vote

@login_required
def voting(request, election_id):

    # chck if logged in user is a student
    if request.user.is_student == True:

        if request.user.student.has_voted == False:
            
            try:
                election = Election.objects.get(pk=election_id)
                position = Position.objects.all()
                total_votes = Student.objects.filter(has_voted=True).count()

                print(position)
                
                context = {
                    'election': election,
                    'position': position,
                    'total_votes': total_votes
                    }
            
            except Election.DoesNotExist:
                raise Http404("Election Does Not Exist")
            
            return render(request, 'stu/index.html', context)

        else:
            logout_view(request)
            return redirect('live')
    else:
        return redirect('home')

        
        
# A VIEW FOR STUDENTS/USERS TO CAST THEIR VOTE
# IT CHECKS IF CURRENT USER IS A STUDENT OR HAS VOTED   
@login_required
def vote(request, election_id):
    if not request.user.is_student == False:
        if request.user.student.has_voted == False:
            
            election = get_object_or_404(Election, pk=election_id)
            current_student = request.user.student
            try:
                selected_President = election.candidate_set.get(pk=request.POST['PRESIDENT'])
                selected_PRO = election.candidate_set.get(pk=request.POST['PRO'])
                selected_Wocom = election.candidate_set.get(pk=request.POST['WOCOM'])
                selected_Treasurer = election.candidate_set.get(pk=request.POST['TREASURER'])
                selected_Secretary = election.candidate_set.get(pk=request.POST['SECRETARY'])
                student_to_update = Student.objects.get(pk = current_student.id)

            except (KeyError, Candidate.DoesNotExist):

                # Redisplay the election voting form.
                return render(request, 'stu/index.html', {
                    'election': election,
                    'error_message': "You didn't select a candidate.",
                })
            else:
                selected_President.votes += 1
                selected_President.save()

                selected_PRO.votes += 1
                selected_PRO.save()

                selected_Treasurer.votes += 1
                selected_Treasurer.save()

                selected_Secretary.votes += 1
                selected_Secretary.save()

                selected_Wocom.votes += 1
                selected_Wocom.save()

                student_to_update.has_voted = True
                student_to_update.save()
                
                # Always return an HttpResponseRedirect after successfully dealing
                # with POST data. This prevents data from being posted twice if a
                # user hits the Back button.
                return HttpResponseRedirect(reverse('election_home', ))
        else:
            # if usr has already voted redirects the person to success page
            return HttpResponseRedirect(reverse('election_home', ))
    else:
        return redirect('home')


# LIVE COUNT CONTAINING TOTAL
#  NUMBER OF STUDENTS AND THOSE WHO HAVE VOTED. 
# DONT NEED NEED ANY SPECIAL AUTH TO ACCESS THIS PAGE

def results_list(request):
    total_student = Student.objects.filter().count()
    total_votes = Student.objects.filter(has_voted=True).count()
    candidates = Candidate.objects.all()
    latest = Position.objects.order_by('id')
    
    
    context = {
        'total_student': total_student,
        'total_votes': total_votes,
        'candidates': candidates,
        'latest': latest,
        }
    
    return render(request, 'stu/results_list.html', context)

# Get question and display results
def results(request, election_id):
  election = get_object_or_404(Position, pk=election_id)
  return render(request, 'stu/results.html', { 'election': election })


# USING ZINGCHART TO DISPLAY RESULTS 
# TO USERS AFTER VOTE HAS BEEN CASTED
def resultsData(request, obj):
    votedata = []

    election = Position.objects.get(id=obj)
    votes = election.candidate_set.all()

    for i in votes:
        votedata.append({i.name:i.votes})

    # print(votedata)
    return JsonResponse(votedata, safe=False)



# A SIMPLE LOGOUT VIEW TO LOGOUT STUDENTS AFTER VOTING
def logout_view(request):
    logout(request)
    

# A VIEW TO GENERATE REPORT FOR USERS 
# A DETAILED REPORT STATING THE NUMBER
# OF STUDENTS THAT HAS VOTED
def report(request):

    election_details = Election.objects.all()
    total_student = Student.objects.filter().count()

    # total students based on level
    lvl_100 = Student.objects.filter(level=100).count()
    lvl_200 = Student.objects.filter(level=200).count()
    lvl_300 = Student.objects.filter(level=300).count()
    lvl_400 = Student.objects.filter(level=400).count()

    # total students based on level that has voted
    lvl_100_voted = Student.objects.filter(level=100, has_voted=True).count()
    lvl_200_voted = Student.objects.filter(level=200, has_voted=True).count()
    lvl_300_voted = Student.objects.filter(level=300, has_voted=True).count()
    lvl_400_voted = Student.objects.filter(level=400, has_voted=True).count()

    # total studens based on faculty
    total_bit = Student.objects.filter(faculty='INFORMATICS').count()
    total_bte = Student.objects.filter(faculty='ENGINEERING').count()
    total_bus = Student.objects.filter(faculty='BUSINESS').count()

    total_votes = Student.objects.filter(has_voted=True).count()
    candidates = Candidate.objects.all()
    
    
    context = {
        'total_student': total_student,
        'total_votes': total_votes,
        'candidates': candidates,
        'election_details': election_details,

        'lvl_100': lvl_100,
        'lvl_200': lvl_200,
        'lvl_300': lvl_300,
        'lvl_400': lvl_400,

        'lvl_100_voted': lvl_100_voted,
        'lvl_200_voted': lvl_200_voted,
        'lvl_300_voted': lvl_300_voted,
        'lvl_400_voted': lvl_400_voted,

        'total_bit': total_bit,
        'total_bte': total_bte,
        'total_bus': total_bus,
        
        }
    

    return render(request, 'db/report.html', context)
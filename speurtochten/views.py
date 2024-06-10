from django.shortcuts import render, redirect
from .models import Speurtocht, Question, Player, GelopenTocht, Vraag
from django.http import HttpResponse
from .util import code_generator, trial_code_check
import datetime
import json
from django.core.mail import send_mail


def index(request):
    """
    Renders a welcome page with introduction and links to stuff
    """
    n = Speurtocht.objects.filter(is_active=True).order_by('pk')
    newest_items = n.reverse()[:6]
    return render(request, "speurtochten/index.html", {
        "newest_items": newest_items
    })


def over(request):
    """
    Renders a page with info about the company
    """
    return render(request, "speurtochten/over.html")


def contact(request):
    """
    Renders a page with options to get in touch
    """
    return render(request, "speurtochten/contact.html")


def overzicht(request):
    """
    Renders an overview of all speurtochten
    """
    alle = Speurtocht.objects.filter(is_active=True)

    return render(request, "speurtochten/overzicht.html", {
        "alle": alle
    })


def speurtocht(request, stad):
    """
    Renders a page with the specifications of the selected speurtocht
    """    
    tochtje = Speurtocht.objects.get(stad=stad)

    return render(request, "speurtochten/speurtocht.html", {
        "speurtocht": tochtje
    })    


def bestellen(request, name):
    """
    Renders a page where the user fills in their email address
    """    
    speurtocht = Speurtocht.objects.get(title=name)
    if request.method == "POST":
        user_mail = request.POST["user-mail"]
        new_player = Player.objects.create(email=user_mail)
        new_player.save()
        code_tocht = code_generator(name)
        gelopen_tocht = GelopenTocht.objects.create(player=new_player, speurtocht=speurtocht, gt_code=code_tocht)
        gelopen_tocht.save()
        """
        Hier moet het betalingssysteem komen. 
        Voor nu is het gratis en is het payment.id hetzelfde als de code_tocht
        Zie github voor ontbrekende code
        """
        gelopen_tocht.payment_id = code_tocht
        gelopen_tocht.save(update_fields=['payment_id'])
        gelopen_tocht.paid_for = True
        gelopen_tocht.save(update_fields=['paid_for'])
        send_mail(
            'Code stadsspeurtocht',
            f"Bedankt voor je bestelling. Je code is {gelopen_tocht.gt_code}.",
            None,
            [f"{new_player.email}"]
			)    

    else:
        return render(request, "speurtochten/bestellen.html", {
        "speurtocht": speurtocht
        }) 



def verdergaan(request, name):
    """
    Renders a page where the user can fill in their code to continue the speurtocht
    """
    if request.method == "POST":
        code_tocht = request.POST["code-tocht"]
        # Check if tocht was started
        if GelopenTocht.objects.filter(gt_code=code_tocht).exists():
            gelopen_tocht = GelopenTocht.objects.get(gt_code=code_tocht)
            if gelopen_tocht.paid_for == False:
                error_message = "Deze speurtocht is nog niet betaald. Neem contact met ons op als je wel betaald hebt."
                return render(request, "speurtochten/verdergaan.html", {
                    "title": name,
                    "error_message": error_message
                })   
            else:
                if gelopen_tocht.finished == True:
                    return redirect('speurtochten/finish', name=name, gt_code=code_tocht)
                elif gelopen_tocht.started == False:
                    return redirect('speurtochten/begin', name=name, gt_code=code_tocht)    
                elif gelopen_tocht.last_answered is None:
                    first_question = Vraag.objects.get(gelopen_tocht=gelopen_tocht, number=gelopen_tocht.first_question)
                    data_question = Question.objects.get(pk=first_question.question_id)
                    return redirect('speurtochten/map', name=name, gt_code=gelopen_tocht.gt_code, num=data_question.number, pk=first_question.pk)
                else:    
                    last_answered = Vraag.objects.get(gelopen_tocht=gelopen_tocht, number=gelopen_tocht.last_answered)
                    data_question = Question.objects.get(pk=last_answered.question_id)
                    next_question = data_question.next_question
                    new_pk = Vraag.objects.get(question=next_question, gelopen_tocht=gelopen_tocht)
                    return redirect('speurtochten/map', name=name, gt_code=gelopen_tocht.gt_code, num=next_question.number, pk=new_pk.pk)
        elif trial_code_check(code_tocht):  
            new_player = Player.objects.create()
            new_player.save()
            speurtocht = Speurtocht.objects.get(title=name)
            gelopen_tocht = GelopenTocht.objects.create(player=new_player, speurtocht=speurtocht, gt_code=code_tocht)
            gelopen_tocht.paid_for = True
            gelopen_tocht.save()
            return redirect('speurtochten/begin', name=name, gt_code=gelopen_tocht.gt_code)
        else:              
            error_message = "Ongeldige code. Probeer het nog eens of neem contact met ons op." 
            return render(request, "speurtochten/verdergaan.html", {
                "title": name,
                "error_message": error_message
            })                   
    else:
        return render(request, "speurtochten/verdergaan.html", {
            "title": name
        })


def begin(request, name, gt_code):
    """
    Renders an info page after payment where player can choose a name and starting point
    """
    gelopen_tocht = GelopenTocht.objects.get(gt_code=gt_code)

    # TODO Hier ontbreekt code, zie github  

    if request.method=="POST":
        gelopen_tocht = GelopenTocht.objects.get(gt_code=gt_code)
        if gelopen_tocht.started == True:
            if gelopen_tocht.finished == True:
                return redirect('speurtochten/finish', name=name, gt_code=gelopen_tocht)
            else:
                last_answered = Vraag.objects.get(gelopen_tocht=gelopen_tocht, number=gelopen_tocht.last_answered)
                data_question = Question.objects.get(last_answered.question)
                next_question = data_question.next_question
                new_pk = Vraag.objects.get(question=next_question, gelopen_tocht=gelopen_tocht)
                return redirect('speurtochten/map', name=name, gt_code=gt_code, num=next_question, pk=new_pk)
        else:    
            speurtocht = Speurtocht.objects.get(title=name)
            starting_point = int(request.POST["starting-point"])
            if starting_point <= 0 or starting_point > speurtocht.no_of_start_points:
                error_message = "Vul het nummer in van de locatie waar je wilt beginnen"
                return render(request, "speurtochten/begin.html", {
                    "speurtocht": speurtocht,
                    "gtcode": gt_code,
                    "error_message": error_message
                })
            start_question = Question.objects.get(speurtocht=speurtocht, starting_point=starting_point)    
            gelopen_tocht.first_question = start_question.number
            player_name = request.POST["team-name"]
            player = gelopen_tocht.player
            player.name = player_name
            player.save(update_fields=['name'])
            gelopen_tocht.started = True
            gelopen_tocht.time_started = datetime.datetime.now()
            gelopen_tocht.save(update_fields=['first_question', 'started', 'time_started'])
            all_questions = Question.objects.filter(speurtocht=speurtocht)
            for q in all_questions:
                vraag = Vraag.objects.create(question=q, number=q.number, gelopen_tocht=gelopen_tocht, gt_code=gt_code)
                vraag.save() 
            vraag_pk = Vraag.objects.get(gelopen_tocht=gelopen_tocht, number=start_question.number)  
            return redirect('speurtochten/map', name=name, gt_code=gt_code, num=start_question.number, pk=vraag_pk.pk)
    else:
        speurtocht = Speurtocht.objects.get(title=name)
        return render(request, "speurtochten/begin.html", {
            "speurtocht": speurtocht,
            "gtcode": gt_code
        })


def map(request, gt_code, name, num, pk):
    vraag = Vraag.objects.get(pk=pk, gt_code=gt_code)
    question = vraag.question
    loc_map = question.map_coords
    loc_marker = question.marker
    location = question.route
    title = question.title
    return render(request, "speurtochten/map.html", {
        "name": name,
        "num": num,
        "pk": pk,
        "locmap": loc_map,
        "locmark": loc_marker,
        "location": location,
        "gtcode": gt_code,
        "title": title
    })


def question(request, name, gt_code, num, pk):
    """
    Renders a page with a question and possible answers
    """
    vraag = Vraag.objects.get(pk=pk, gt_code=gt_code)
    data_question = vraag.question
    if vraag.answered == True:
        return redirect('speurtochten/answer', name=name, gt_code=gt_code, num=num, pk=pk)
    else:
        if request.method == "POST":
            given_answer = request.POST["given-answer"]
            int_answer = int(given_answer)
            vraag.answered = True
            if int_answer == data_question.correct_answer:
                vraag.answer_correct = True
            else:
                vraag.answer_correct = False
            vraag.save(update_fields=['answer_correct', 'answered'])
            return redirect('speurtochten/answer', name=name, gt_code=gt_code, num=num, pk=pk)        
        else:
            return render(request, "speurtochten/question.html", {
                "question": data_question,
                "name": name,
                "gtcode": gt_code,
                "num": num,
                "pk": pk
            })


def answer(request, name, gt_code, num, pk):
    """
    Renders a page with the given answer, correct answer and some additional info
    """
    current_question = Vraag.objects.get(pk=pk, gt_code=gt_code)

    if current_question.answered == True:
        data_question = current_question.question
        answer_correct = current_question.answer_correct
        next_question = data_question.next_question
        next_vraag = Vraag.objects.get(number=next_question.number, gt_code=gt_code)
        gelopen_tocht = current_question.gelopen_tocht
        gelopen_tocht.last_answered = current_question.number
        gelopen_tocht.save(update_fields=['last_answered'])
        if next_vraag.answered == True:
            finished = True
            gelopen_tocht.finished = True
            gelopen_tocht.save(update_fields=['finished'])
            return render(request, "speurtochten/answer.html", {
                "question": data_question,
                "correct": answer_correct,
                "finished": finished,
                "name": name,
                "gtcode": gt_code
            })
        else:
            new_vraag = Vraag.objects.get(number=next_question.number, gt_code=gt_code)
            new_pk = new_vraag.pk
            finished = False
            return render(request, 'speurtochten/answer.html', {
                "question": data_question,
                "correct": answer_correct,
                "finished": finished,
                "name": name,
                "gtcode": gt_code,
                "num": next_question.number,
                "pk": new_pk
            })
    else: 
        return redirect('speurtochten/question', name=name, gt_code=gt_code, num=num, pk=pk)    


def finish(request, name, gt_code):
    """
    Renders the final page of the speurtocht with the result and an overview of the given answers
    """
    gelopen_tocht = GelopenTocht.objects.get(gt_code=gt_code)
    gelopen_tocht.time_finished = datetime.datetime.now()
    vragen = Vraag.objects.filter(gt_code=gt_code)
    total_questions = len(vragen)
    amount_correct = 0
    overview_list = []
    for vraag in vragen:
        question = vraag.question
        vraag_dict = {'number': vraag.number, 'subject':question.title, 'answered': vraag.answered, 'correct': vraag.answer_correct}
        overview_list.append(vraag_dict)
        if vraag.answer_correct:
            amount_correct = amount_correct+1
    gelopen_tocht.overview = json.dumps(overview_list) 
    gelopen_tocht.save(update_fields=['time_finished', 'overview'])       
    return render(request, "speurtochten/finish.html", {
        "name": name,
        "vragen": overview_list,
        "amount": amount_correct,
        "total": total_questions
    })
    

def algemenevoorwaarden(request):
    """
    Renders the page with terms and conditions
    """
    return render(request, "speurtochten/algemene-voorwaarden.html")
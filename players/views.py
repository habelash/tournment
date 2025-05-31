from django.shortcuts import render
from registration.models import Payment
from django.shortcuts import render
from collections import defaultdict
from registration.models import TournamentRegistration
from django.http import HttpResponse
from django.template.loader import get_template
import pdfkit  # Or use WeasyPrint or xhtml2pdf
# Create your views here.

def registered_players(request):
    payments = Payment.objects.select_related('registration')  # Efficient join
    context = {
        'payments': payments
    }
    return render(request, "registered_players.html", context)

def all_registrations_view(request):
    registrations = TournamentRegistration.objects.all()
    return render(request, 'players_details.html', {'registrations': registrations})

def download_all_registrations_pdf(request):
    registrations = TournamentRegistration.objects.all()
    template = get_template('players_detailspdf.html')
    html = template.render({'registrations': registrations})

    # Convert HTML to PDF
    pdf = pdfkit.from_string(html, False)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="all_registrations.pdf"'
    return response

def fixture_view(request):
    registrations = TournamentRegistration.objects.all()
    fixtures = defaultdict(list)

    for reg in registrations:
        category = reg.category

        if category == 'singles':
            team = reg.player_name
        elif category in ['beginner_men_doubles', 'intermediate_men_doubles',
                          'intermediate_plus_mens_doubles', 'womens_doubles', 'mixed_doubles']:
            team = f"{reg.player_name} & {reg.partner_name}"
        elif category == 'triplets':
            team = f"{reg.player_name} & {reg.partner_name} & {reg.partner_2_name}"
        else:
            team = reg.player_name

        fixtures[category].append(team)

    # Prepare fixtures grouped in rounds (simple Round 1 bracket logic)
    bracket_data = {}
    for category, teams in fixtures.items():
        rounds = []
        round1 = []
        # Pair up teams into Round 1 matches
        for i in range(0, len(teams), 2):
            if i + 1 < len(teams):
                match = f"{teams[i]} vs {teams[i+1]}"
            else:
                match = f"{teams[i]} (bye)"
            round1.append(match)
        rounds.append(('Round 1', round1))
        bracket_data[category] = rounds

    return render(request, 'fixtures_chat.html', {'bracket_data': bracket_data})
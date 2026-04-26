from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from .models import Reponse
import pandas as pd
import plotly
import plotly.express as px
import json

main = Blueprint('main', __name__)

@main.route('/')
def accueil():
    return render_template('./html/accueil.html')

@main.route('/formulaire', methods = ['GET','POST'])
def formulaire():

    erreur = None

    if request.method == 'POST':

        genre = request.form.get('genre')
        age = request.form.get('age')
        filiere = request.form.get('filiere')
        annee = request.form.get('annee')
        niveau_stress = request.form.get('niveau_stress')
        cause_stress = request.form.get('cause_stress')
        heures_sommeil = request.form.get('heures_sommeil')
        fait_sport = request.form.get('fait_sport')
        songe_abandon = request.form.get('songe_abandon')
        gestion_stress = request.form.get('gestion_stress')

        reponses = Reponse(genre=genre, age=age, filiere=filiere, annee = annee, niveau_stress=niveau_stress, cause_stress=cause_stress,heures_sommeil=heures_sommeil,fait_sport=fait_sport,songe_abandon=songe_abandon,gestion_stress=gestion_stress)

        db.session.add(reponses)
        db.session.commit()

        return redirect(url_for('main.merci'))


    return render_template('./html/formulaire.html')

@main.route('/merci')
def merci():
    return render_template('./html/merci.html')

@main.route('/analyse')
def analyse():
    reponses = Reponse.query.all()

    data = [{
        'genre': r.genre,
        'age': r.age,
        'niveau_stress': r.niveau_stress,
        'cause_stress': r.cause_stress,
        'heures_sommeil': r.heures_sommeil,
        'fait_sport': r.fait_sport,
        'songe_abandon': r.songe_abandon,
        'gestion_stress': r.gestion_stress
    } for r in reponses]

    df = pd.DataFrame(data)

    moyenne_niveau_stress = df['niveau_stress'].mean()
    mediane = df['niveau_stress'].median()
    mode = df['niveau_stress'].mode()[0]
    nombre_total_reponses = len(df)

    layout_style = dict(
        paper_bgcolor='#1a1a2e',
        plot_bgcolor='#383849',
        font=dict(family='JetBrains Mono', color='#fff'),
        title_font=dict(size=18, color='#058d97'),
        legend=dict(
            bgcolor='#383849',
            bordercolor='#058d97',
            borderwidth=1,
            font=dict(color='#fff')
        )
    )

    # Diagramme 1 — Camembert des causes de stress
    fig1 = px.pie(df, names='cause_stress', title='Causes du stress',
        color_discrete_sequence=['#058d97', '#405386', '#383849', '#1a1a2e', '#fff']
    )
    fig1.update_layout(**layout_style)
    graphe1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    # Diagramme 2 — Barres du niveau de stress par genre
    fig2 = px.bar(df.groupby('genre')['niveau_stress'].mean().reset_index(),
                x='genre', y='niveau_stress',
                title='Niveau de stress moyen par genre',
                color_discrete_sequence=['#058d97']
    )
    fig2.update_layout(**layout_style)
    fig2.update_traces(marker_line_color='#405386', marker_line_width=2)
    graphe2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    # Diagramme 3 — Barres des heures de sommeil
    fig3 = px.bar(df['heures_sommeil'].value_counts().reset_index(),
                x='heures_sommeil', y='count',
                title='Heures de sommeil des étudiants',
                color_discrete_sequence=['#405386']
    )
    fig3.update_layout(**layout_style)
    fig3.update_traces(marker_line_color='#058d97', marker_line_width=2)
    graphe3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('./html/analyse.html', 
        moy_stress=round(moyenne_niveau_stress, 2), 
        mediane=mediane, 
        mode=mode, 
        total_reponse=nombre_total_reponses, 
        graphe1=graphe1, 
        graphe2=graphe2, 
        graphe3=graphe3
    )
from dash import html, callback, Input, Output, State, ctx, dcc, no_update
from voc_exam import *
import plotly.express as px
import random
from pandas import DataFrame


# data initialization
WORDS_FILE = 'words/words_V1.0.0.xlsx'
SERIES_HISTO_FILE = 'words/series_history.csv'
df_quiz: DataFrame = pd.DataFrame()
right_answer_count = 0

df_series_score = pd.read_csv(SERIES_HISTO_FILE, sep=';')[-5:]
df_series_score['score'] = 0
df_series_score['score'] = df_series_score['serie_score']/df_series_score['serie_size']


@callback(Output('quiz-container', 'children'),
          Output('quiz-starter', 'className'),
          Input('start-button', 'n_clicks'),
          State('serie-size', 'value'),
          State('quiz-starter', 'className'),
          prevent_initial_call=True)
def start_quiz(n_clicks, serie_size, quiz_starter_current_class):
    global df_quiz
    df_quiz = get_series(get_dataframe(WORDS_FILE), int(serie_size))
    df_quiz['asked'] = False
    df_quiz['answered'] = False
    # tell the df that the first element has been asked
    df_quiz.iloc[0, df_quiz.columns.get_loc('asked')] = True
    # condition to see which element has been asked but not answered
    condition = (df_quiz['answered'] == False) & (df_quiz['asked'] == True)
    if df_quiz.loc[condition, 'fr_to_eng'].values[0]:
        asking_direction = ['answer', 'question']
        index_asking_direction = random.random()
        index_asking_direction = round(index_asking_direction)
        question = df_quiz.loc[condition, asking_direction[index_asking_direction]].values[0]
    else:
        question = df_quiz.loc[condition, 'question'].values[0]
    asked_count = df_quiz.loc[condition, 'asked_count'].values[0]
    if asked_count == 0:
        score = 'not asked yet'
    else:
        score = str(df_quiz.loc[condition, 'right_answer_count'].values[0]) + '/' + str(asked_count)

    if df_quiz.loc[condition, 'fr_to_eng'].values[0]:
        fr_to_eng = 'fr to eng?'
    else:
        fr_to_eng = ''

    # Add display none to quiz starter menu
    updated_class = quiz_starter_current_class + " d-none"

    return get_quiz_layout(question, score, fr_to_eng), updated_class


@callback(
    Output('answer-label', 'children'),
    Input('show-answer', 'n_clicks'),
    Input('question-container', 'children'),
    prevent_initial_call=True)
def show_answer(n_clicks, question_value):
    global df_quiz
    # condition to see which element has been asked but not answered
    condition = (df_quiz['answered'] == False) & (df_quiz['asked'] == True)
    if question_value == df_quiz.loc[condition, 'question'].values[0]:
        answer = df_quiz.loc[condition, 'answer']
    else:
        answer = df_quiz.loc[condition, 'question']
    return answer


@callback(Output('quiz_layout', 'children'),
          Output('quiz-starter', 'className', allow_duplicate=True),
          Input('right-answer-button', 'n_clicks'),
          Input('wrong-answer-button', 'n_clicks'),
          State('quiz-starter', 'className'),
          State('fr-to-eng-checklist', 'value'),
          State('answer-label', 'children'),
          prevent_initial_call=True)
def display_next_question(n_clicks_right, n_clicks_wrong, quiz_starter_current_class, fr_to_eng_check, answer):
    if (n_clicks_right is None) & (n_clicks_wrong is None):
        return no_update
    global df_quiz
    global right_answer_count
    condition = (df_quiz['answered'] == False) & (df_quiz['asked'] == True)

    # Change fr_to_eng col according to if the checklist is checked
    if 'fr to eng?' in fr_to_eng_check:
        df_quiz.loc[condition, 'fr_to_eng'] = True
    else:
        df_quiz.loc[condition, 'fr_to_eng'] = False

    # Update the word's row interval and the date according to the answer
    if ctx.triggered_id == 'right-answer-button':
        df_quiz.update(update_row(df_quiz[condition], 1))
        right_answer_count += 1
    else:
        df_quiz.update(update_row(df_quiz[condition], 0))
    df_quiz.loc[condition, 'answered'] = True

    # See if answered column is full of True
    if len(df_quiz['answered'].unique()) == 1:
        df = get_dataframe(WORDS_FILE)
        save_series_score(df_quiz.shape[0], right_answer_count)
        save_series(df, df_quiz, WORDS_FILE)
        # Remove display none from the quiz start classes
        updated_class = quiz_starter_current_class.replace(" d-none", "")
        return html.Div(['Series complete '+ str(right_answer_count)+'/'+str(df_quiz.shape[0])],
                        className='h2 d-flex justify-content-center mt-5 mb-5'), updated_class

    result = df_quiz.loc[df_quiz['asked'] == False]
    result.iloc[0, result.columns.get_loc('asked')] = True
    df_quiz.update(result)

    if result.iloc[0, result.columns.get_loc('fr_to_eng')]:
        asking_direction = ['answer', 'question']
        index_asking_direction = random.random()
        index_asking_direction = round(index_asking_direction)
        question = result.iloc[0, result.columns.get_loc(asking_direction[index_asking_direction])]
    else:
        question = result.iloc[0, result.columns.get_loc('question')]

    if result.iloc[0, result.columns.get_loc('asked_count')] == 0:
        score = 'not asked yet'
    else:
        score = str(result.iloc[0, result.columns.get_loc('right_answer_count')])+'/'+str(result.iloc[0, result.columns.get_loc('asked_count')])

    if result.iloc[0, result.columns.get_loc('fr_to_eng')]:
        fr_to_eng = 'fr to eng?'
    else:
        fr_to_eng = ''

    return get_quiz_layout(question, score, fr_to_eng), quiz_starter_current_class


def get_quiz_layout(input_text, score, fr_to_eng):
    quiz_layout = html.Div([
        html.Div([
            html.Div(input_text, id='question-container', className='form-label text-center my-5 h4'),
        ], className='row'),
        html.Div([
            html.Div([
                html.Div([
                    dcc.Input(type='text', className='form-control'),
                ], className='col-md-8'),
                html.Div([
                    html.Button(id='show-answer', children='Answer', className='btn btn-primary'),
                ], className='col-md-2'),
                html.Div(score, className='col-md-2'),
            ], className='row'),
            html.Div([
                dcc.Checklist(['fr to eng?'], [fr_to_eng], id='fr-to-eng-checklist')
            ], className='row'),
            html.Div([
                html.Div(id='answer-label', className='form-label'),
            ], className='row'),
        ], className='row'),
        html.Div([
            html.Div([
                html.Button(id='right-answer-button', children='Good', className='btn btn-success mx-2 px-5'),
            ], className='col-md-6 d-flex justify-content-center'),
            html.Div([
                html.Button(id='wrong-answer-button', children='Wrong', className='btn btn-danger mx-2 px-5' ),
            ], className='col-md-6 d-flex justify-content-center'),
        ], className='row my-5'),
    ], id='quiz_layout')
    return quiz_layout


# score graphe
def get_scores_graph():
    fig = px.bar(df_series_score, x="date", y="score", width=500, height=250, color='date', text='serie_size')
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=1),
        yaxis=dict(range=[0, 1], title=''),
        xaxis=dict(title='', tickformat='%B-%d'))
    fig.update_layout(showlegend=False)
    return fig

"""Tests use synthetic data only."""
from app.services.parser_service import parse_chat, participants
from app.services.personality_service import analyze_style
from app.services.retrieval_service import retrieve_examples

def test_parse_multiline_and_participants():
    rows=parse_chat('12/08/2026, 21:32 - Alex: bro what are you doing 😭\ncontinued\n12/08/2026, 21:33 - Me: nothing lol')
    assert len(rows)==2 and 'continued' in rows[0]['message']
    assert participants(rows)==['Alex','Me']

def test_style():
    profile=analyze_style(['bro no way 😭','lol nah bro'])
    assert profile.uses_slang and profile.uses_emojis

def test_retrieval():
    rows=[{'message_id':1,'sender':'Me','message':'what happened'},{'message_id':2,'sender':'Alex','message':'bro 😭'}]
    assert retrieve_examples(rows,'what happened','Alex')[0]['target']=='bro 😭'

def test_empty():
    assert parse_chat('') == []
    assert analyze_style([]).average_message_length == 0

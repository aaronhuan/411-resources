from contextlib import contextmanager
import re
import sqlite3

import pytest

from boxing.boxing.models.ring_model import RingModel
from boxing.boxing.models.boxers_model import Boxer

@pytest.fixture()
def ring_model():
    """Fixture to provide a new instance of RingModel for each test."""
    return RingModel()

@pytest.fixture
def sample_boxer1():
    return Boxer(0, 'Boxer 1',150, 3, 10, 20)

@pytest.fixture
def sample_boxer2():
    return Boxer(1, 'Boxer 2', 200, 4, 2.0, 35)


##################################################
# Add / Remove Ring Management Test Cases
##################################################

def test_clear_ring_1(ring_model,sample_boxer1):
    """Test clearing the ring with a boxer in the ring initially.

    """
    ring_model.enter_ring(sample_boxer1)

    ring_model.clear_ring()
    assert len(ring_model.ring) == 0, "Ring should be empty after clearing"


def test_clear_empty_ring(ring_model):
    """Test clearing the ring with no boxers in the ring initially.

    """
    assert len(ring_model.ring)==0
    ring_model.clear_ring()
    assert len(ring_model.ring)==0, "Ring already cleared"

def test_enter_ring(ring_model,sample_boxer1):
    """Test adding a boxer into the ring.

    """
    ring_model.enter_ring(sample_boxer1)
    assert len(ring_model.ring)==1
    assert ring_model.ring[0].name =='Boxer 1'


def test_enter_ring_invalid_type(ring_model):
    """Test adding a boxer that is not an instance of Boxer class into the ring.

    """
    fakeBoxer = 1
    with pytest.raises(TypeError, match=f"Invalid type: Expected 'Boxer'"):
        ring_model.enter_ring(fakeBoxer)


def test_enter_ring_more_than_2(ring_model, sample_boxer1, sample_boxer2):
    """Test adding more than two boxers into the ring.

    """
    ring_model.enter_ring(sample_boxer1)
    ring_model.enter_ring(sample_boxer2)
    sample_boxer3 = Boxer(3, 'Boxer 3', 200, 6, 3, 29)
    with pytest.raises(ValueError, match="Ring is full, cannot add more boxers"):
        ring_model.enter_ring(sample_boxer3)


def test_get_boxers(ring_model, sample_boxer1, sample_boxer2):
    """Test retrieving boxers inside the ring.

    """
    ring_model.enter_ring(sample_boxer1)
    ring_model.enter_ring(sample_boxer2)
    boxers = ring_model.get_boxers()
    assert len(ring_model.get_boxers())== 2
    assert boxers[0].name== 'Boxer 1'
    assert boxers[1].name== 'Boxer 2'


def test_get_fighting_skill(ring_model, sample_boxer1):
    """Test obtaining a boxer's skill.

    """
    skill = ring_model.get_fighting_skill(sample_boxer1)
    assert type(skill) == float


def test_fight_success(mocker, ring_model, sample_boxer1, sample_boxer2):
    """Test fight with two boxers in the ring.

    """
    ring_model.enter_ring(sample_boxer1)
    ring_model.enter_ring(sample_boxer2)
    mocker.patch("boxing.boxing.models.ring_model.get_random", return_value=0.6)
    mock_update = mocker.patch("boxing.boxing.models.ring_model.update_boxer_stats")

    boxer_winner = ring_model.fight()
    assert len(ring_model.ring) == 0 
    assert boxer_winner in [sample_boxer1.name, sample_boxer2.name]
     

def test_invalid_number_of_boxers_fight(ring_model, sample_boxer1):
    """Test invalid number of boxers in the ring.

    """
    ring_model.enter_ring(sample_boxer1)
    with pytest.raises(ValueError, match="There must be two boxers to start a fight."):
        ring_model.fight()

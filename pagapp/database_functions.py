"""Functions to operate with whole database."""

from pagapp.models import db


def create_database():
    """Creates database schema"""
    db.create_all()

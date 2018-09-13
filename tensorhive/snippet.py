from sqlalchemy import create_engine, Column, DateTime, Integer, CheckConstraint, ForeignKey
from sqlalchemy.orm import sessionmaker, validates, relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime
import sqlalchemy
from sqlalchemy_utils import create_database, drop_database, database_exists
from tensorhive.models.reservation_event.ReservationEventModel import ReservationEventModel
from tensorhive.models.user.UserModel import UserModel
from tensorhive.database import Base, engine, init_db, db_session as session

import names
import random
import click

'''
Description:

1. pip install names
2. Put this file anywhere within tensorhive package (root is preferred)
3. Fill in SET_OF_GPU_UUIDS to suit your needs

Commands:
pip -m tensorhive.snippet generate both

generate users
generate users --amount 100

generate events
generate events --amount 10

generate both
generate both --amount 10
'''
SET_OF_GPU_UUIDS = [
    # These would be picked randomly
    'GPU-ed1715ac-a9f1-20e0-ed61-557dbe8f62a6', # des12
    'GPU-c6d01ed6-8240-2e11-efe9-aa32794b8273', # des13
    'GPU-f23b26cd-8f45-cf7d-e06e-356f0f1fad1e', # des15
    'GPU-19a852f2-bb08-b292-283b-8d032531a70d', # des17
    # Add more here if needed
]

@click.group()
def main():
    pass

@main.group()
def generate():
    pass

@generate.command()
@click.option('--amount', default=5, help='Users to generate.')
def users(amount):
    init_db()

    click.echo('Generating {} users:'.format(amount))
    [create_new_user() for _ in range(amount)]
    
@generate.command()
@click.option('--amount', default=5, help='Reservation events to generate')
def events(amount):
    init_db()
    
    click.echo('----------')
    click.echo('Generating {} reservation events:'.format(amount))
    all_users = list(session.query(UserModel).all())
    for _ in range(amount):
        random_user = random.choice(all_users)
        create_new_reservation(random_user)

@generate.command()
@click.option('--amount', default=5, help='Amount of users and reservation events to generate.')
def both(amount):
    init_db()
    
    click.echo('----------')
    click.echo('Generating {} users:'.format(amount))
    [create_new_user() for _ in range(amount)]

    click.echo('----------')
    click.echo('Generating {} reservation events:'.format(amount))
    all_users = list(session.query(UserModel).all())
    for _ in range(amount):
        random_user = random.choice(all_users)
        create_new_reservation(random_user)

@main.command()
def drop():
    drop_database(engine.url)

def persist(model_instance):
    if model_instance.save_to_db():
        print('Successfully created: ', model_instance)
    else:
        print('Failed to create: ', model_instance)


def create_new_user():
    new_user = UserModel(username=names.get_full_name())
    persist(new_user)


def create_new_reservation(user, min_duration=30, max_duration=40):
    '''Creates reservation for a random user. It lasts <min_duration, max_duration> minutes'''
    
    event_duration_in_minutes = random.randint(min_duration, max_duration)
    current_time = datetime.datetime.utcnow()
    event_end_time = current_time + datetime.timedelta(minutes=event_duration_in_minutes)

    new_reservation = ReservationEventModel(
        title='Title for {}'.format(user.username),
        user_id=user.id,
        description='Example description',
        resource_id=random.choice(SET_OF_GPU_UUIDS),
        start=current_time,
        end=event_end_time
    )
    persist(new_reservation)
    
    
if __name__ == '__main__':
    main()

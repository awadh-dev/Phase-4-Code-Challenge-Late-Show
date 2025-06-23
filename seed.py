import csv
from app import app, db
from models import Guest, Episode, Appearance

with app.app_context():
    db.drop_all()
    db.create_all()

    with open('seed.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        episodes_dict = {}
        guests_dict = {}

        count = 1  # Episode number

        for row in reader:
            show_date = row["Show"]
            guest_name = row["Raw_Guest_List"]
            occupation = row["GoogleKnowlege_Occupation"]

            # Create or reuse episode
            if show_date not in episodes_dict:
                episode = Episode(date=show_date, number=count)
                db.session.add(episode)
                episodes_dict[show_date] = episode
                count += 1
            else:
                episode = episodes_dict[show_date]

            # Create or reuse guest
            if guest_name not in guests_dict:
                guest = Guest(name=guest_name, occupation=occupation)
                db.session.add(guest)
                guests_dict[guest_name] = guest
            else:
                guest = guests_dict[guest_name]

            # Create appearance (assign random rating 1–5)
            appearance = Appearance(
                rating=3,
                guest=guest,
                episode=episode
            )
            db.session.add(appearance)

        db.session.commit()
        print("Database seeded successfully!")

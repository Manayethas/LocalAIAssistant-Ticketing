from app import create_app, db
from app.models.user import User

def create_test_users():
    app = create_app()
    with app.app_context():
        # Check if users already exist
        if not User.query.filter_by(username='demo_user').first():
            # Create regular user
            user = User(
                username='demo_user',
                email='demo@example.com',
                is_technician=False
            )
            user.set_password('demo123')
            db.session.add(user)
            print('Created regular user:')
            print('   Username: demo_user')
            print('   Password: demo123')
        else:
            print('Regular user already exists')
        
        if not User.query.filter_by(username='tech_support').first():
            # Create technician
            tech = User(
                username='tech_support',
                email='tech@example.com',
                is_technician=True
            )
            tech.set_password('tech123')
            db.session.add(tech)
            print('\nCreated technician:')
            print('   Username: tech_support')
            print('   Password: tech123')
        else:
            print('Technician already exists')
        
        db.session.commit()

if __name__ == '__main__':
    create_test_users() 
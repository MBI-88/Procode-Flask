# Script to run the app 
# Packages 
import sys,os,click,unittest
from app import create_app,db
from app.models import User,Role,Permission,Post
from flask_migrate import Migrate,upgrade

# Config
COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True,include='app/*')
    COV.start()

app = create_app(os.getenv('FLASK_ENV') or 'default')
migrate = Migrate(app,db)

@app.shell_context_processor
def make_shell_context() -> dict:
    return dict(db=db,User=User,Post=Post,Permission=Permission,Role=Role)


@app.cli.command()
@click.option('--coverage/--no-coverage',default=False,help='Enable coverage option to test')
@click.argument('test_names',nargs=-1)
def test(coverage:bool,test_names:str) -> None:
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import subprocess
        os.environ['FLASK_COVERAGE'] = '1'
        sys.exit(subprocess.call(sys.argv))
    
    if test_names:
        tests = unittest.TestLoader().loadTestsFromModule(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    
    unittest.TextTestRunner(verbosity=2).run(tests)
    
    if COV:
        COV.stop()
        COV.save()
        print('[*] Coverage Summary [*]')
        basedir = os.path.abspath(os.path.dirname(__file__))
        cov_dir = os.path.join(basedir,'temp/coverage')
        COV.html_report(directory=cov_dir)


@app.cli.command()
@click.option('--length',default=25,help='Number of fuctions include in report')
@click.option('--profile-dir',default=None,help='Directory to save profile data')
def profile_data(length:int,profile_dir:str) -> None:
    from werkzeug.middleware.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app,restrictions=[length],profile_dir=profile_dir)
    app.run()


@app.cli.command()
@click.option('--update-database/--no-update-database',default=False,help='Command to update database')
def deploy(update_database:bool) -> None:
    if update_database:
        upgrade()
        Role.insert_roles()
    
from fabric import task

@task
def setup(c):
    # c.run('pip3 install -r requirements.txt')
    c.run("python3 manage.py collectstatic --noinput")

@task
def run(c):
    c.run("gunicorn webapp.wsgi:application --bind 0.0.0.0:8000 -D --pid pid.txt", replace_env=False, pty=False)

@task
def kill(c):
    c.run("kill -9 `cat pid.txt`")

@task
def reset(c):
    c.run("rm -r db.sqlite3")
    c.run("python3 manage.py migrate")
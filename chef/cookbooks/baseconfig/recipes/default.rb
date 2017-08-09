# Make sure the Apt package lists are up to date, so we're downloading versions that exist.
cookbook_file "apt-sources.list" do
  path "/etc/apt/sources.list"
end
execute 'apt_update' do
  command 'apt-get update'
end

# Setup Django Production Dependencies (nginx and postgresql)
package "nginx"
cookbook_file 'nginx-default' do
  path '/etc/nginx/sites-available/default'
end
package "postgresql"
package "postgresql-server-dev-all"
package "libpython-dev"
execute 'create_db' do
  command 'echo "CREATE DATABASE mydb; CREATE USER ubuntu; GRANT ALL PRIVILEGES ON DATABASE mydb TO ubuntu;" | sudo -u postgres psql'
end
execute "nginx_reload" do
  command "nginx -s reload"
end

# Setup Django Webserver
# psycopg2 is for communication between django and postgres database
# uwsgi is for communication between django and nginx
package "python3-pip"
execute 'dependencies_install' do
  command 'sudo pip3 install django psycopg2 uwsgi'
end

# Put rc.local file in the right place. Run it manually while provisioning since the vm has already started
# rc.local is for starting uwsgi upon vm start. This is done in rc.local instead of here in the chef script, because
# if you use 'vagrant halt' instead of 'vagrant destroy', your next 'vagrant up' will restart your previously provisioned
# vm without running the chef script, which means all the dependencies will be installed, but uwsgi won't be started
# starting uwsgi from rc.local ensures it's started upon every vm boot regardless of whether the machine is provisioned
cookbook_file 'rc.local' do
  path '/etc/rc.local'
end
execute 'init_uwsgi' do
  command 'sudo /etc/rc.local'
end
# There seems to be an issue with line endings in the git repository being converted to line endings that unix
# systems don't like, which causes the rc.local script to not run. Until this is solved, we will run the uwsgi
# startup command here to ensure the system actually starts
execute 'make-sure-uwsgi-starts' do
  command 'uwsgi --ini /home/ubuntu/project/uwsgi.ini  --daemonize /home/ubuntu/mysite.log'
end

execute 'django_init_dev_database' do
  cwd '/home/ubuntu/project/webroot/'
  user 'ubuntu'
  command 'python3 manage.py migrate'
end

# need to be ubuntu user for this command, because we configured the database to have privileges granted to the ubuntu user
execute 'load_initial_db_data' do
  cwd '/home/ubuntu/project/webroot'
  user 'ubuntu'
  command 'python3 manage.py loaddata accounts_initial_data.json && python3 manage.py loaddata textbook_app_initial_data.json'
end

# After django is all configured, collect static files
# TODO: check if this can be ran right after "init_static"
execute 'django_configure_static_files' do
  cwd '/home/ubuntu/project/webroot/'
  command 'python3 manage.py collectstatic --noinput'
end

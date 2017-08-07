# Make sure the Apt package lists are up to date, so we're downloading versions that exist.
cookbook_file "apt-sources.list" do
  path "/etc/apt/sources.list"
end
execute 'apt_update' do
  command 'apt-get update'
end

# Setup Django Production Dependencies (nginx and postgresql)
package "nginx"
execute "nginx-default" do
  # I think there's a better way to do this with chef instead of using cp, but I'm too lazy to figure it out
  command "cp /home/ubuntu/project/chef/cookbooks/baseconfig/files/default/nginx-default /etc/nginx/sites-available/default"
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

#need to be ubuntu user for this command, because we configured the database to have privileges granted to the ubuntu user
execute 'load_initial_db_data' do
  cwd '/home/ubuntu/project'
  user 'ubuntu'
  command 'psql mydb < initialdata.txt'
end

# Setup Django Webserver
# psycopg2 is for communication between django and postgres database
# uwsgi is for communication between django and nginx
package "python3-pip"
execute 'dependencies_install' do
  command 'sudo pip3 install django psycopg2 uwsgi'
end
execute 'init_uwsgi' do
  command 'uwsgi --ini /home/ubuntu/project/uwsgi.ini  --daemonize /home/ubuntu/mysite.log'
end

execute 'django_init_dev_database' do
  cwd '/home/ubuntu/project/webroot/'
  user 'ubuntu'
  command 'python3 manage.py migrate'
end

# After django is all configured, collect static files
# TODO: check if this can be ran right after "init_static"
execute 'django_configure_static_files' do
  cwd '/home/ubuntu/project/webroot/'
  command 'python3 manage.py collectstatic --noinput'
end

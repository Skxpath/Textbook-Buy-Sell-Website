# Make sure the Apt package lists are up to date, so we're downloading versions that exist.
cookbook_file "apt-sources.list" do
  path "/etc/apt/sources.list"
end
execute 'apt_update' do
  command 'apt-get update'
end

# Base configuration recipe in Chef.
package "wget"
package "ntp"

cookbook_file "ntp.conf" do
  path "/etc/ntp.conf"
end
execute 'ntp_restart' do
  command 'service ntp restart'
end

# Setup postgresql db
package "postgresql"
package "postgresql-server-dev-all"
package "libpython-dev"

execute 'create_db' do
  command 'echo "CREATE DATABASE mydb; CREATE USER ubuntu; GRANT ALL PRIVILEGES ON DATABASE mydb TO ubuntu;" | sudo -u postgres psql'
end

execute 'load_initial_db_data' do
  cwd '/home/ubuntu/project'
  user 'ubuntu'
  command 'psql mydb < initialdata.txt'
end

# Setup Django Webserver
package "python3-pip"
execute 'django_install' do
  command 'sudo pip3 install django psycopg2'
end
execute 'django_init_dev_database' do
  cwd '/home/ubuntu/project/webroot/'
  user 'ubuntu'
  command 'python3 manage.py migrate'
end
execute 'django_init_server' do
  user 'ubuntu'
  cwd '/home/ubuntu/project/webroot'
  command 'nohup python3 manage.py runserver 0.0.0.0:8080 &'
end


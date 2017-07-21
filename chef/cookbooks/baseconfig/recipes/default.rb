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

# Setup Django Webserver
package "python3-pip"
execute 'django_install' do
  command 'sudo pip3 install django'
end
execute 'django_init_dev_database' do
  cwd '/home/ubuntu/project/webroot/'
  command 'python3 manage.py migrate'
end
execute 'django_init_server' do
  user 'ubuntu'
  cwd '/home/ubuntu/project/webroot'
  command 'nohup python3 manage.py runserver 0.0.0.0:8080 &'
end
# execute 'django_populate_dev_database' do
#   cwd '/home/ubuntu/project/mysite'
#   command 'python3 manage.py loaddata initial_data.json'
# end

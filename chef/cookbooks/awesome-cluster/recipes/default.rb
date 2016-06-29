
template '/etc/yum.repos.d/datastax.repo' do
  source 'datastax.repo.erb'
  owner 'root'
  group 'root'
  mode '0755'
end

template '/tmp/structure.cql' do
  source 'structure.cql.erb'
  owner 'root'
  group 'root'
  mode '0755'
end

package ['java-1.8.0-openjdk', 'cassandra30']

package ['java-1.7.0-openjdk']  do
  action :remove
end

template '/etc/cassandra/conf/cassandra.yaml' do
  source 'cassandra.yaml.erb'
  owner 'root'
  group 'root'
  mode '0755'
end

# Gotta find a way to put the seed IP's on the conf

service "cassandra" do
  action :start
end

execute 'cassandra_structure' do
  command 'cqlsh cassandra1 -f /tmp/structure.cql'
  only_if 'cat /etc/hostname | grep cassandra1'
end


#only for the master
#cqlsh  172.31.29.111 -f test.cql
#


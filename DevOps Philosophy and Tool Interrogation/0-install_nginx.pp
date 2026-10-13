# Declarative configuration manifest: Defines the desired state of Nginx web server
# Demonstrates "WHAT" state the system should be in; Puppet handles the reconciliation loop

# 1. Package Resource: Ensure Nginx is installed
package { 'nginx':
  ensure => installed,
}

# 2. File Resource: Ensure default landing page has canonical content
file { '/var/www/html/index.html':
  ensure  => file,
  content => 'Holberton School',
  mode    => '0644',
  owner   => 'root',
  group   => 'root',
  require => Package['nginx'],
}

# 3. File Resource: Ensure Nginx default site configuration contains redirect rule
file_line { 'nginx_redirect_rule':
  path    => '/etc/nginx/sites-available/default',
  after   => 'server_name _;',
  line    => "\trewrite ^/redirect_me https://www.youtube.com permanent;",
  require => Package['nginx'],
  notify  => Service['nginx'],
}

# 4. Service Resource: Ensure Nginx is enabled and actively running
service { 'nginx':
  ensure    => running,
  enable    => true,
  hasstatus => true,
  restart   => '/usr/sbin/service nginx reload',
  require   => Package['nginx'],
  subscribe => [
    File['/var/www/html/index.html'],
  ],
}

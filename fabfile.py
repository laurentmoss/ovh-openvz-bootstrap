from fabric.api import env, roles, run

env.roledefs['host'] = ['root@%s' % env.host_ip]

@roles('host')
def nat_ip_output():
    run('iptables -t nat -A POSTROUTING -s 192.168.2.0/24 -o vmbr0 -j SNAT --to %s' % env.host_ip)

@roles('host')
def create_container(container_id):
    run('echo \'DISKINODES="1048576:1048576"\' > /etc/vz/conf/%s.conf' % container_id)
    run('vzctl create %s --ostemplate ubuntu-12.04-standard_12.04-1_i386 --layout simfs --diskspace 4194304' % container_id)
    run('vzctl set %s --ram 512M --swap 512M --save' % container_id)
    run('vzctl set %s --ipadd 192.168.2.%s --save' % (container_id, container_id) )
    run('vzctl set %s --searchdomain ip-192-99-3.net --save' % container_id)
    run('vzctl set %s --nameserver 127.0.0.1 --nameserver 213.186.33.99 --save' % container_id)

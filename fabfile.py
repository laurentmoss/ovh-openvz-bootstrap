from fabric.api import env, roles, run

env.roledefs['host'] = ['root@%s' % env.host_ip]

@roles('host')
def nat_ip_output():
    run('iptables -t nat -A POSTROUTING -s 192.168.2.0/24 -o vmbr0 -j SNAT --to %s' % env.host_ip)

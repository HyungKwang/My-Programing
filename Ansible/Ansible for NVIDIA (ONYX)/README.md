## Intro

 This script does OS/FW upgrade downgrade. 
 And it's for MLXN-OS, which is acuired by NVIDIA (a.k.a Mellanox Ethernet/IB OS)

 
 ### limitation = Improvement needed.
  1. There is a cycle. To run it continuously, you need to copy & paste as many as you need to run.
     So in Ansible script, if we are able to put 'do while loop statement', we can reduce the script volume.
     "OS_Up_downgrade_100times.yml"

  2. I don't know how to handle 'reset factory'. Because after 'reset factory', swtich is boot-up with Wizrd interactive mode.
     Handling interactive Wizrd is very hard.

## How to run

 ### Modify & Plance images under /root
  1. You need to modify 2things properly : OS_Up_Downgrade.yml and hosts.

> From "hosts"
     
```
[root@NVIDIA ~]# cat /etc/ansible/hosts 
[ONYX]
NVIDIA.test.labs     <==== modify properly.
[ONYX:vars]
ansible_network_os=onyx
ansible_become=yes
ansible_become_method=enable
ansible_ssh_user=admin
ansible_ssh_pass=admin
```

> From "OS_Up_Downgrade.yml", modify license properly.

```
# Add license

    - name: Add license
      onyx_config:
            lines:
              - license install XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX
      register: add_license
```

  2. Place images under /root/image-X86_64-3.6.2102.img, image-X86_64-3.6.6162.img, image-X86_64-3.6.8008.img, image-X86_64-3.6.8010.img
       
> From "OS_Up_downgrade.yml"     


```
      ansible_network_os: onyx
      user: admin
      password: admin
      transfer_protocol: scp
      source_file: "/root/image-X86_64-{{ version3 }}.img"  <==============
      destination_folder: /var/opt/tms/images/ 
    remote_user: admin

```
     

 ### How to run

```
[root@NVIDIA ~]# ansible-playbook OS_Up_downgrade.yml 
 For debugging
[root@NVIDIA ~]# ansible-playbook OS_Up_downgrade.yml -vvvv
```

# **SECURITY**
---

## __Configure SSH__

Good info from :
https://linux-audit.com/audit-and-harden-your-ssh-configuration/

i strongly recommand to setup this configuration for **/etc/ssh/sshd_config** file  

```
IgnoreRhosts yes  
PermitEmptyPasswords no  
MaxAuthTries 3  
PermitRootLogin no  
MaxSessions 1
```

Are you connected to the remote with SSH ?  
Yes: type this command to reload configuration  
```
systemctl reload ssh.service  
```

Check intrusion and attempt  
```
systemctl status ssh.service  
```
## __PAM__

Secure your ssh connexion by adding delay on failure on the file 'sshd' in pam.d
```
sudo nano /etc/pam.d/sshd
```
add the line below to add a delay of 10s on failure

```
auth  optional  pam_faildelay.so  delay=10000000
```


## __SYSLOG__

due to the huge amount of attack on ssh port i recommand
to remove auth log.

```
sudo nano /etc/rsyslog.conf
```
and comment the line :
```
#auth,authpriv.*               /var/log/auth.log
```
restart syslog
```
 sudo service rsyslog restart
```
